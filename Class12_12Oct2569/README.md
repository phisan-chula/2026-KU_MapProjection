# Lab Assignment 12 : Comparative Metric Distortion in Cylindrical & Web Projections

**Course:** Advanced Geomatics & Mathematical Cartography  
**Instructor:** Cartography & Geodesy Division  
**Model Parameters:** Spherical Earth ($R = 6371\text{ km}$, $e = 0$)  

---

## 1. Overview & Objectives

In modern geospatial analysis and web GIS, coordinates are regularly transformed between raw angular systems and projected planar spaces. This laboratory assignment investigates the mathematical foundation, coordinate bounds, and metric distortions of three cylindrical representations:

1. **Plate Carrée / Equirectangular** (Planar projection of angular geographic coordinates, often denoted loosely as Cartesian EPSG:4326)
2. **True Spherical Mercator** (Analytic conformal cylindrical projection)
3. **Pseudo / Web Mercator** (Spherical conformal formulation constrained to a square map canvas for quadtree tiling)

Central Meridian :  Longitude (λ): 101.0° E
Starting Parallel :  Latitude (φ): 0.0° 

### Learning Outcomes
By completing this assignment, students will be able to:
- Formulate forward equations and inverse cutoff equations for cylindrical projections.
- Derive local scale factors along meridians ($h$) and parallels ($k$), as well as local areal inflation factors ($s$).
- Compute numerical distortion values across key latitudes.
- Graphically illustrate the geometric behavior of Tissot's Indicatrix for conformal vs. non-conformal projections.

---

## 2. Mathematical Formulations

Let $(\varphi, \lambda)$ denote spherical geodetic latitude and longitude in radians, where $\lambda_0 = 0$ is the central meridian, and $R = 6371\text{ km}$.

### 2.1 Projection 1: Plate Carrée (Equirectangular)
The simplest cylindrical projection where angular coordinates map linearly onto a Cartesian plane with the Equator as the standard parallel ($\varphi_1 = 0$):

$$X = R \cdot \lambda$$

$$Y = R \cdot \varphi$$

#### Scale Factors & Distortions:
* **Meridional scale factor:** 
  $$h = \frac{1}{R} \frac{\partial Y}{\partial \varphi} = 1$$
* **Parallel scale factor:** 
  $$k = \frac{1}{R \cos\varphi} \frac{\partial X}{\partial \lambda} = \frac{1}{\cos\varphi} = \sec\varphi$$
* **Areal scale factor ($s = h \cdot k$):** 
  $$s = 1 \cdot \sec\varphi = \sec\varphi$$
* **Angular deformation:** Non-conformal for all $\varphi \neq 0$. Circles of infinitesimal radius deform into ellipses elongated along the east-west parallel axis.

---

### 2.2 Projection 2: True Spherical Mercator
Conformal cylindrical projection preserving local shapes and angles ($h = k$ at every point):



---

### 2.3 Projection 3: Pseudo / Web Mercator
Web mapping platforms (OpenStreetMap, Google Maps, Mapbox) adopt a modified Mercator scheme designed around a square planar coordinate space ($2\pi R \times 2\pi R$) for pyramidal tile partitioning ($256 \times 256$ pixels per tile).



---

## 3. Laboratory Tasks

- Plot Thailand and its neighbours boundaries
- Plot graticule @1 degree or appropriate
- Plot Tissot Indicatrix R@20km or appropriate
- Annotate all necessaries

- Using the assigned geographic coordinates of the beginning and end of a runway in your province, calculate their projected coordinates using the three map projections. Determine the runway length in each projection and compare the differences, using Mercator as the reference projection.


---



---

## 5. Submission Requirements

- **File 1:** `Lab_Report.pdf` (Calculations, filled comparative table, generated plots, and answers to Section 4).
- **File 2:** `distortion_analysis.py` (Reproducible script generating the figures and table values).
