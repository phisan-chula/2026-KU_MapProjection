# Hands-on 10 : UTM Zones 47N and 48N

**Platform:** Google Colab + Python/Cartopy
**Topic:** UTM projection and map distortion

## Part 1 — Visualize UTM Distortion

Using `python/cartopy`, create a map of Thailand.

Requirements:

* Thailand extent
* Graticule every **1°**
* Coastline and borders
* Tissot indicatrices at regular 1° grid points
* Tissot circle radius = **10 km**

### Map 1 — UTM Zone 47N

Use:

```python
ccrs.UTM(zone=47)
```

Draw Thailand and Tissot indicatrices.

Mark:

* Central Meridian = **99°E**
* Zone boundary = **102°E**

Observe how the Tissot circles change from west to east.

### Map 2 — UTM Zone 48N

Use:

```python
ccrs.UTM(zone=48)
```

Mark:

* Central Meridian = **105°E**
* Zone boundary = **102°E**

Compare the distortion pattern with Zone 47N.

### Questions

1. Where is distortion smallest?
2. What happens when moving away from the central meridian?
3. Why does Thailand require both UTM Zones 47N and 48N?
4. What happens if western Thailand is projected using Zone 48N?

---

## Part 2 — Individual 1-km Test Line

Each student selects one 1-km line from the provided dataset.

Using Python:

1. Read endpoints \(P_1,P_2\).
2. Calculate WGS84 geodesic distance using `pyproj.Geod`.
3. Transform the line to:

   * EPSG:32647
   * EPSG:32648
4. Calculate UTM grid distance:

$$
D_g=\sqrt{(\Delta E)^2+(\Delta N)^2}
$$

5. Calculate line scale:

$$
k=\frac{D_g}{D_{geodesic}}
$$

6. Calculate distortion:

$$
ppm=(k-1)\times10^6
$$

Report:

| CRS     | Grid Distance | Scale | Distortion |
| ------- | ------------: | ----: | ---------: |
| UTM 47N |               |       |        ppm |
| UTM 48N |               |       |        ppm |

---

## AI Prompt

> Write a Google Colab Python script using Cartopy and PyProj.
>
> First, create two maps of Thailand:
>
> 1. UTM Zone 47N
> 2. UTM Zone 48N
>
> Use 1-degree graticules and draw Tissot indicatrices with a 10-km radius at regular 1-degree locations.
>
> Show central meridians 99°E and 105°E and the UTM zone boundary at 102°E.
>
> Then read my assigned 1-km test line, calculate WGS84 geodesic distance, UTM grid distance in Zones 47N and 48N, scale factor, and distortion in ppm.
>
> Plot all results on screen and write clear commented Python code for Google Colab.

## Main Concept

$$
\boxed{\text{Geodesic distance} \neq \text{UTM grid distance}}
$$

and

$$
\boxed{\text{UTM distortion increases away from the central meridian}}
$$
