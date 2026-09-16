# 2_compareLDP.py
#
# Compare coordinates transformed using:
#   1) PROJ4 definition
#   2) WKT definition
#
# Input:
#   DATA/1_BM_PotashUdon.gpkg
#   layer = BenchMark
#
# CRS definitions:
#   DATA/TH_UN_LDP_Potash_South.PJ4
#   DATA/TH_UN_LDP_POTASH_South.WKT

from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
from pyproj import CRS, Transformer


GPKG = Path("DATA/1_BM_PotashUdon.gpkg")
LAYER = "BenchMark"

PJ4_FILE = Path("DATA/TH_UN_LDP_Potash_South.PJ4")
WKT_FILE = Path("DATA/TH_UN_LDP_POTASH_South.WKT")

OUTPUT_CSV = Path("OUTPUT_compare_LDP.csv")

# Report differences larger than this value
TOL_M = 1e-6


# ============================================================
# Read CRS definitions
# ============================================================

def read_proj4(filename):
    """Read PROJ4 definition from text file."""

    lines = filename.read_text(
        encoding="utf-8"
    ).splitlines()

    # Ignore blank lines and comments
    proj4 = " ".join(
        line.strip()
        for line in lines
        if line.strip()
        and not line.strip().startswith("#")
    )

    return CRS.from_user_input(proj4)


def read_wkt(filename):
    """Read WKT CRS definition."""

    return CRS.from_wkt(
        filename.read_text(encoding="utf-8")
    )


# ============================================================
# Transform all points
# ============================================================

def transform_points(gdf, target_crs):

    transformer = Transformer.from_crs(
        gdf.crs,
        target_crs,
        always_xy=True
    )

    x = gdf.geometry.x.to_numpy()
    y = gdf.geometry.y.to_numpy()

    E, N = transformer.transform(x, y)

    return np.asarray(E), np.asarray(N)


# ============================================================
# Main
# ============================================================

def main():

    # --------------------------------------------------------
    # Read BenchMark
    # --------------------------------------------------------

    gdf = gpd.read_file(
        GPKG,
        layer=LAYER
    )

    if gdf.crs is None:
        raise ValueError(
            "BenchMark layer has no source CRS."
        )

    print()
    print("=" * 72)
    print("LDP CRS COMPARISON")
    print("=" * 72)

    print(f"Input       : {GPKG}")
    print(f"Layer       : {LAYER}")
    print(f"Points      : {len(gdf)}")
    print(f"Source CRS  : {gdf.crs}")
    print()

    # --------------------------------------------------------
    # Read LDP definitions
    # --------------------------------------------------------

    crs_pj4 = read_proj4(PJ4_FILE)
    crs_wkt = read_wkt(WKT_FILE)

    print(f"LDP1 PJ4 : {PJ4_FILE}")
    print(f"LDP2 WKT : {WKT_FILE}")

    print()
    print("CRS equivalent:", crs_pj4.equals(crs_wkt))
    print()

    # --------------------------------------------------------
    # Transform
    # --------------------------------------------------------

    E1, N1 = transform_points(
        gdf,
        crs_pj4
    )

    E2, N2 = transform_points(
        gdf,
        crs_wkt
    )

    # --------------------------------------------------------
    # Differences
    # --------------------------------------------------------

    dE = E2 - E1
    dN = N2 - N1

    d2D = np.hypot(
        dE,
        dN
    )

    # --------------------------------------------------------
    # Result table
    # --------------------------------------------------------

    if "Point" in gdf.columns:
        point_names = gdf["Point"].astype(str)
    else:
        point_names = [
            f"P{i + 1}"
            for i in range(len(gdf))
        ]

    df = pd.DataFrame({
        "Point": point_names,

        "LDP1_E_PJ4_m": E1,
        "LDP1_N_PJ4_m": N1,

        "LDP2_E_WKT_m": E2,
        "LDP2_N_WKT_m": N2,

        "dE_m": dE,
        "dN_m": dN,
        "d2D_m": d2D,
    })

    # --------------------------------------------------------
    # Print ALL points
    # --------------------------------------------------------

    pd.set_option(
        "display.max_rows",
        None
    )

    pd.set_option(
        "display.width",
        200
    )

    print(
        df.to_string(
            index=False,
            formatters={
                "LDP1_E_PJ4_m": "{:.4f}".format,
                "LDP1_N_PJ4_m": "{:.4f}".format,

                "LDP2_E_WKT_m": "{:.4f}".format,
                "LDP2_N_WKT_m": "{:.4f}".format,

                "dE_m": "{:+.9f}".format,
                "dN_m": "{:+.9f}".format,
                "d2D_m": "{:.9f}".format,
            }
        )
    )

    # ========================================================
    # Statistics
    # ========================================================

    print()
    print("=" * 72)
    print("DIFFERENCE SUMMARY")
    print("=" * 72)

    print(
        f"Maximum |dE|  : "
        f"{np.max(np.abs(dE)):.9f} m"
    )

    print(
        f"Maximum |dN|  : "
        f"{np.max(np.abs(dN)):.9f} m"
    )

    print(
        f"Maximum d2D   : "
        f"{np.max(d2D):.9f} m"
    )

    print(
        f"Mean d2D      : "
        f"{np.mean(d2D):.9f} m"
    )

    print(
        f"RMS d2D       : "
        f"{np.sqrt(np.mean(d2D ** 2)):.9f} m"
    )

    # --------------------------------------------------------
    # Find points that differ
    # --------------------------------------------------------

    different = df[
        df["d2D_m"] > TOL_M
    ]

    print()
    print(
        f"Tolerance     : {TOL_M:g} m"
    )

    print(
        f"Different pts : "
        f"{len(different)} / {len(df)}"
    )

    if len(different) == 0:

        print()
        print(
            "RESULT: PJ4 and WKT give "
            "IDENTICAL coordinates within tolerance."
        )

    else:

        print()
        print(
            "RESULT: Coordinate differences detected."
        )

        print()
        print(
            different[
                [
                    "Point",
                    "dE_m",
                    "dN_m",
                    "d2D_m"
                ]
            ].to_string(
                index=False,
                formatters={
                    "dE_m": "{:+.9f}".format,
                    "dN_m": "{:+.9f}".format,
                    "d2D_m": "{:.9f}".format,
                }
            )
        )

    # --------------------------------------------------------
    # Worst point
    # --------------------------------------------------------

    i = np.argmax(d2D)

    print()
    print("Worst point")
    print("-" * 40)

    print(
        f"Point : {df.iloc[i]['Point']}"
    )

    print(
        f"dE    : {dE[i]:+.9f} m"
    )

    print(
        f"dN    : {dN[i]:+.9f} m"
    )

    print(
        f"d2D   : {d2D[i]:.9f} m"
    )

    # --------------------------------------------------------
    # CSV
    # --------------------------------------------------------

    df.to_csv(
        OUTPUT_CSV,
        index=False,
        float_format="%.9f"
    )

    print()
    print(
        f"Saved: {OUTPUT_CSV}"
    )


if __name__ == "__main__":
    main()
