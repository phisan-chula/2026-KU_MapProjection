# 1_read_BM.py

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from pyproj import CRS, Proj, Transformer
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


class MultiCRSProjectExtent:

    R = 6_371_000.0
    BASE_EPSG = 32648

    TARGET_POINTS = {
        "L0BM08",
        "CBM15", "CBM16", "CBM30", "CBM40",
        "RBM03", "CBM31", "CBM50*", "RBM04*",
        "CBM21", "CBM25", "CBM33",
    }

    # ======================================================
    # INIT / CRS
    # ======================================================

    def __init__(self, gpkg, layer="BenchMark", name_col="Point"):

        self.name_col = name_col
        self.crs = {}

        self.gdf = gpd.read_file(gpkg, layer=layer)

        if self.gdf.crs is None:
            self.gdf = self.gdf.set_crs(self.BASE_EPSG)
        else:
            self.gdf = self.gdf.to_crs(self.BASE_EPSG)

        logging.info(
            f"Loaded {len(self.gdf)} benchmarks"
        )


    def add_epsg(self, name, epsg):
        self.crs[name] = CRS.from_epsg(epsg)


    def add_wkt(self, name, filename):

        p = Path(filename)

        if not p.exists():
            logging.warning(f"WKT not found: {filename}")
            return

        self.crs[name] = CRS.from_wkt(
            p.read_text(encoding="utf-8")
        )


    # ======================================================
    # BASIC VALUES
    # ======================================================

    def _name(self, row):
        return str(
            row.get(self.name_col, "")
        ).strip()


    @staticmethod
    def _h(row):
        """Return ellipsoidal height."""

        for field in ("h_Ellipsoid_m", "h"):

            v = row.get(field)

            if pd.notna(v):
                return float(v)

        return None


    # ======================================================
    # CSF
    # ======================================================

    def _csf(self, row, proj, transformer, dh=0.0):
        """
        Combined Scale Factor in ppm.

        dh =   0 -> h
        dh = 150 -> h - 150 m
        dh = 300 -> h - 300 m
        """

        h = self._h(row)

        if h is None:
            return None

        x = row.geometry.x
        y = row.geometry.y

        lon, lat = transformer.transform(x, y)

        psf = proj.get_factors(
            lon, lat
        ).meridional_scale

        h_relative = h - dh

        hsf = self.R / (
            self.R + h_relative
        )

        return (
            psf * hsf - 1.0
        ) * 1_000_000.0


    @staticmethod
    def _proj_objects(crs):

        return (
            Proj(crs),
            Transformer.from_crs(
                crs,
                4326,
                always_xy=True
            )
        )


    # ======================================================
    # PROJECT EXTENT
    # ======================================================

    @staticmethod
    def _plot_extent(ax, gdf, buffer_m):

        hull = (
            gdf.geometry
            .union_all()
            .convex_hull
        )

        gpd.GeoSeries(
            [hull.buffer(buffer_m)],
            crs=gdf.crs
        ).plot(
            ax=ax,
            color="lightgreen",
            edgecolor="none",
            alpha=0.30
        )

        if 0:
            gpd.GeoSeries( [hull], crs=gdf.crs).plot(
                ax=ax,
                facecolor="none",
                edgecolor="blue",
                linestyle="--",
                linewidth=1.5
            )


    # ======================================================
    # MSL CONTOURS
    # ======================================================

    def _plot_contours(
        self,
        ax,
        crs,
        gpkg,
        layer,
        ci,
        sigma
    ):

        if not gpkg or not Path(gpkg).exists():
            logging.warning(
                f"Contour file not found: {gpkg}"
            )
            return

        pts = gpd.read_file(
            gpkg,
            layer=layer
        )

        if pts.crs is None:
            pts = pts.set_crs(
                self.BASE_EPSG
            )

        pts = pts.to_crs(crs)

        if "MSL" not in pts.columns:
            logging.warning(
                "Contour layer has no 'MSL' field"
            )
            return

        pts = pts.copy()

        pts["z"] = pd.to_numeric(
            pts["MSL"],
            errors="coerce"
        )

        pts = pts.dropna(
            subset=["z", "geometry"]
        )

        if len(pts) < 3:
            return

        x = pts.geometry.x.to_numpy()
        y = pts.geometry.y.to_numpy()
        z = pts["z"].to_numpy()

        gx, gy = np.mgrid[
            x.min():x.max():300j,
            y.min():y.max():300j
        ]

        # interpolation area
        mask = griddata(
            (x, y),
            z,
            (gx, gy),
            method="linear"
        )

        # complete surface for smoothing
        gz = griddata(
            (x, y),
            z,
            (gx, gy),
            method="nearest"
        )

        if sigma > 0:
            gz = gaussian_filter(
                gz,
                sigma=sigma
            )

        # suppress extrapolation
        gz[np.isnan(mask)] = np.nan

        if np.all(np.isnan(gz)):
            return

        zmin = (
            np.floor(
                np.nanmin(gz) / ci
            ) * ci
        )

        zmax = (
            np.ceil(
                np.nanmax(gz) / ci
            ) * ci
        )

        levels = np.arange(
            zmin,
            zmax + ci,
            ci
        )

        #ax.contour( gx, gy, gz, levels=levels, colors="purple", linewidths=1.0)
        cs = ax.contour(
                gx,
                gy,
                gz,
                levels=levels,
                colors="0.25",       # dark gray
                linewidths=0.8,
                linestyles="-",
                alpha=0.85,
                zorder=5
            )

        ax.clabel(
                cs,
                inline=True,
                fontsize=8,
                fmt="%.1f",
                colors="0.20"
            )
        # intentionally:
        # NO ax.clabel()


    # ======================================================
    # TARGET POINTS
    # ======================================================

    def _plot_targets(
        self,
        ax,
        gdf,
        mode,
        proj=None,
        transformer=None
    ):

        for _, row in gdf.iterrows():

            if self._name(row) not in self.TARGET_POINTS:
                continue

            x = row.geometry.x
            y = row.geometry.y

            ax.plot(
                x,
                y,
                "o",
                color="darkred",
                markersize=5
            )

            # ----------------------------------------------
            # CSF
            # ----------------------------------------------

            if mode == "CSF":

                v = self._csf(
                    row,
                    proj,
                    transformer,
                    dh=0
                )

                label = (
                    f"{v:+.0f}"
                    if v is not None
                    else None
                )

            # ----------------------------------------------
            # MSL directly from BenchMark.MSL_m
            # ----------------------------------------------

            else:

                v = row.get("MSL_m")

                label = (
                    f"{float(v):.0f} m"
                    if pd.notna(v)
                    else None
                )

            if label:

                ax.annotate(
                    label,
                    (x, y),
                    xytext=(0, 6),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    fontstyle="italic",
                    weight="normal"
                )


    # ======================================================
    # GENERIC SUBPLOT
    # ======================================================

    def _panel(
        self,
        ax,
        crs_name,
        mode,
        buffer_m,
        contour=None
    ):

        crs = self.crs[crs_name]
        gdf = self.gdf.to_crs(crs)

        self._plot_extent(
            ax,
            gdf,
            buffer_m
        )

        # MSL contour
        if mode == "MSL":

            self._plot_contours(
                ax,
                crs,
                contour["gpkg"],
                contour["layer"],
                contour["ci"],
                contour["sigma"]
            )

        # all benchmarks
        gdf.plot(
            ax=ax,
            color="red",
            markersize=3,
            alpha=0.7
        )

        # TARGET_POINTS
        if mode == "CSF":

            proj, transformer = self._proj_objects(
                crs
            )

            self._plot_targets(
                ax,
                gdf,
                "CSF",
                proj,
                transformer
            )

        else:

            self._plot_targets(
                ax,
                gdf,
                "MSL"
            )

        # formatting
        parameter = (
            "CSF_ppm"
            if mode == "CSF"
            else "MSL"
        )

        ax.set_title(
            f"{parameter} — {crs_name}",
            weight="bold"
        )

        ax.set_xlabel("Easting (m)")
        ax.set_ylabel("Northing (m)")

        fmt = ticker.StrMethodFormatter(
            "{x:,.0f}"
        )

        ax.xaxis.set_major_formatter(fmt)
        ax.yaxis.set_major_formatter(fmt)

        if crs_name in {
            "TH_UN_LDP",
            "TH_UN_Potash_South"
        }:

            ax.xaxis.set_major_locator(
                ticker.MultipleLocator(5000)
            )

            ax.yaxis.set_major_locator(
                ticker.MultipleLocator(5000)
            )

        ax.tick_params(
            axis="x",
            labelrotation=45
        )

        ax.grid(
            True,
            linestyle=":",
            alpha=0.6
        )


    # ======================================================
    # REPORT — ALL BENCHMARKS
    # ======================================================

    def print_summary(
        self,
        crs_name="TH_UN_Potash_South"
    ):

        crs = self.crs[crs_name]
        gdf = self.gdf.to_crs(crs)

        proj, transformer = self._proj_objects(
            crs
        )

        rows = []

        for _, row in gdf.iterrows():

            h = self._h(row)

            csf0 = self._csf(
                row,
                proj,
                transformer,
                dh=0
            )

            csf150 = self._csf(
                row,
                proj,
                transformer,
                dh=150
            )

            csf300 = self._csf(
                row,
                proj,
                transformer,
                dh=300
            )

            msl = row.get("MSL_m")

            rows.append({

                "Point":
                    self._name(row),

                "Easting_m":
                    f"{row.geometry.x:,.3f}",

                "Northing_m":
                    f"{row.geometry.y:,.3f}",

                "MSL_m":
                    (
                        f"{float(msl):.0f}"
                        if pd.notna(msl)
                        else "N/A"
                    ),

                "h_Ellipsoid_m":
                    (
                        f"{h:.3f}"
                        if h is not None
                        else "N/A"
                    ),

                "CSF_ppm@+0m":
                    (
                        f"{csf0:+.0f}"
                        if csf0 is not None
                        else "N/A"
                    ),

                "CSF_ppm@-150m":
                    (
                        f"{csf150:+.0f}"
                        if csf150 is not None
                        else "N/A"
                    ),

                "CSF_ppm@-300m":
                    (
                        f"{csf300:+.0f}"
                        if csf300 is not None
                        else "N/A"
                    ),
            })

        df = pd.DataFrame(rows)

        print(
            f"\n## CSF REPORT — "
            f"ALL {len(df)} BENCHMARKS\n"
        )

        print(
            f"**CRS:** `{crs_name}`\n"
        )

        print(
            "**Relative vertical levels:**\n"
            "- `@+0m = h`\n"
            "- `@-150m = h - 150 m`\n"
            "- `@-300m = h - 300 m`\n"
        )

        print(
            df.to_markdown(
                index=False
            )
        )

        # final statistics
        self.print_statistics(
            report_crs=crs_name
        )


    # ======================================================
    # STATISTICS
    # ======================================================

    def print_statistics(
        self,
        report_crs="TH_UN_Potash_South"
    ):
        """
        4 subplot statistics
        + CSF @ -150 m
        + CSF @ -300 m
        """

        definitions = [

            # 4 subplots
            (
                "Top-Left",
                "UTM Zone 48N",
                "CSF_ppm",
                "CSF",
                0
            ),

            (
                "Top-Right",
                "UTM Zone 48N",
                "MSL_m",
                "MSL",
                0
            ),

            (
                "Bottom-Left",
                "TH_UN_LDP",
                "CSF_ppm",
                "CSF",
                0
            ),

            (
                "Bottom-Right",
                "TH_UN_Potash_South",
                "CSF_ppm",
                "CSF",
                0
            ),

            # additional report statistics
            (
                "-",
                report_crs,
                "CSF_ppm@-150m",
                "CSF",
                150
            ),

            (
                "-",
                report_crs,
                "CSF_ppm@-300m",
                "CSF",
                300
            ),
        ]

        rows = []

        for (
            subplot,
            crs_name,
            parameter,
            mode,
            dh
        ) in definitions:

            crs = self.crs[crs_name]
            gdf = self.gdf.to_crs(crs)

            # ----------------------------------------------
            # MSL
            # ----------------------------------------------

            if mode == "MSL":

                values = pd.to_numeric(
                    gdf["MSL_m"],
                    errors="coerce"
                ).to_numpy(dtype=float)

            # ----------------------------------------------
            # CSF
            # ----------------------------------------------

            else:

                proj, transformer = (
                    self._proj_objects(crs)
                )

                values = np.array(
                    [
                        self._csf(
                            row,
                            proj,
                            transformer,
                            dh=dh
                        )
                        for _, row in gdf.iterrows()
                    ],
                    dtype=float
                )

            values = values[
                np.isfinite(values)
            ]

            rows.append({

                "Subplot":
                    subplot,

                "CRS":
                    crs_name,

                "Parameter":
                    parameter,

                "Count":
                    len(values),

                "Min":
                    np.min(values)
                    if len(values)
                    else np.nan,

                "Mean":
                    np.mean(values)
                    if len(values)
                    else np.nan,

                "Max":
                    np.max(values)
                    if len(values)
                    else np.nan,
            })

        df = pd.DataFrame(rows)

        for col in (
            "Min",
            "Mean",
            "Max"
        ):

            df[col] = df[col].map(
                lambda x:
                    f"{x:.1f}"
                    if np.isfinite(x)
                    else "N/A"
            )

        print(
            "\n\n## STATISTICS — "
            "4 SUBPLOTS + RELATIVE LEVELS\n"
        )

        print(
            df.to_markdown(
                index=False
            )
        )


    # ======================================================
    # FIGURE
    # ======================================================

    def plot(
        self,
        buffer_m=3000,
        ci=5,
        contour_gpkg=None,
        contour_layer="Point",
        sigma=1,
        out_base="BM_CSF_MSL"
    ):

        if ci <= 0:
            raise ValueError(
                "Contour interval must be > 0"
            )

        fig = plt.figure(
            figsize=(16, 20)
        )

        gs = fig.add_gridspec(
            3,
            2,
            height_ratios=[
                1,
                0.15,
                1
            ],
            wspace=0.25
        )

        axes = [
            fig.add_subplot(gs[0, 0]),
            fig.add_subplot(gs[0, 1]),
            fig.add_subplot(gs[2, 0]),
            fig.add_subplot(gs[2, 1]),
        ]

        panels = [
            ("UTM Zone 48N",       "CSF"),
            ("UTM Zone 48N",       "MSL"),
            ("TH_UN_LDP",          "CSF"),
            ("TH_UN_Potash_South", "CSF"),
        ]

        contour = {
            "gpkg": contour_gpkg,
            "layer": contour_layer,
            "ci": ci,
            "sigma": sigma,
        }

        for ax, (
            crs_name,
            mode
        ) in zip(
            axes,
            panels
        ):

            self._panel(
                ax,
                crs_name,
                mode,
                buffer_m,
                contour
                if mode == "MSL"
                else None
            )

        # identical UTM extent
        axes[1].set_xlim(
            axes[0].get_xlim()
        )

        axes[1].set_ylim(
            axes[0].get_ylim()
        )

        # --------------------------------------------------
        # SAVE PNG + SVG
        # --------------------------------------------------

        png = f"{out_base}.png"
        svg = f"{out_base}.svg"

        fig.savefig(
            png,
            dpi=300,
            bbox_inches="tight"
        )

        fig.savefig(
            svg,
            bbox_inches="tight"
        )

        print(f"\nSaved: {png}")
        print(f"Saved: {svg}")

        plt.show()


# ==========================================================
# MAIN
# ==========================================================

def main():

    p = argparse.ArgumentParser(
        description=(
            "Benchmark CSF, MSL and "
            "LDP comparison plots"
        )
    )

    p.add_argument(
        "-i",
        "--input",
        default="DATA/1_BM_PotashUdon.gpkg"
    )

    p.add_argument(
        "-l",
        "--layer",
        default="BenchMark"
    )

    p.add_argument(
        "--CI",
        type=float,
        default=5
    )

    p.add_argument(
        "--cgpkg",
        default="TH_UN/TH_UN_LDP.gpkg"
    )

    p.add_argument(
        "--clayer",
        default="Point"
    )

    p.add_argument(
        "--sigma",
        type=float,
        default=1
    )

    p.add_argument(
        "--out",
        default="BM_CSF_MSL"
    )

    args = p.parse_args()

    project = MultiCRSProjectExtent(
        args.input,
        args.layer
    )

    # ------------------------------------------------------
    # CRSs
    # ------------------------------------------------------

    project.add_epsg(
        "UTM Zone 48N",
        32648
    )

    project.add_wkt(
        "TH_UN_LDP",
        "TH_UN/TH_UN_LDP_CRS.WKT"
    )

    project.add_wkt(
        "TH_UN_Potash_South",
        "DATA/TH_UN_LDP_POTASH_South.WKT"
    )

    # ------------------------------------------------------
    # Markdown report
    # ------------------------------------------------------

    project.print_summary(
        "TH_UN_Potash_South"
    )

    # ------------------------------------------------------
    # Figure
    # ------------------------------------------------------

    project.plot(
        buffer_m=3000,
        ci=args.CI,
        contour_gpkg=args.cgpkg,
        contour_layer=args.clayer,
        sigma=args.sigma,
        out_base=args.out
    )


if __name__ == "__main__":
    main()
