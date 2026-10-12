# Lab Assignment: Comparative Metric Distortion in Cylindrical & Web Projections

**Course:** Advanced Geomatics & Mathematical Cartography  
**Instructor:** Cartography & Geodesy Division  
**Model Parameters:** Spherical Earth ($R = 6371\text{ km}$, $e = 0$)  

---

## 1. Overview & Objectives

In modern geospatial analysis and web GIS, coordinates are regularly transformed between raw angular systems and projected planar spaces. This laboratory assignment investigates the mathematical foundation, coordinate bounds, and metric distortions of three cylindrical representations:

1. **Plate Carrée / Equirectangular** (Planar projection of angular geographic coordinates, often denoted loosely as Cartesian EPSG:4326)
2. **True Spherical Mercator** (Analytic conformal cylindrical projection)
3. **Pseudo / Web Mercator** (Spherical conformal formulation constrained to a square map canvas for quadtree tiling)

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

$$X = R \cdot \lambda$$

$$Y = R \ln\left[ \tan\left(\frac{\pi}{4} + \frac{\varphi}{2}\right) \right] = R \operatorname{gd}^{-1}(\varphi)$$

*(where $\operatorname{gd}^{-1}(\varphi)$ is the inverse Gudermannian function)*

#### Scale Factors & Distortions:
* **Meridional scale factor:** 
  $$h = \sec\varphi$$
* **Parallel scale factor:** 
  $$k = \sec\varphi$$
* **Areal scale factor ($s = h \cdot k$):** 
  $$s = \sec^2\varphi$$
* **Singularity:** As $\varphi \to \pm\frac{\pi}{2}$ ($\pm 90^\circ$), $Y \to \pm\infty$ and $s \to \infty$.

---

### 2.3 Projection 3: Pseudo / Web Mercator
Web mapping platforms (OpenStreetMap, Google Maps, Mapbox) adopt a modified Mercator scheme designed around a square planar coordinate space ($2\pi R \times 2\pi R$) for pyramidal tile partitioning ($256 \times 256$ pixels per tile).

#### Forward Equations:
$$X = R \cdot \lambda$$

$$Y = R \ln\left[ \tan\left(\frac{\pi}{4} + \frac{\varphi}{2}\right) \right]$$

#### Domain and Cutoff:
To enforce an exact $1:1$ square aspect ratio where $X_{\max} = Y_{\max} = \pi R$:

$$\ln\left[ \tan\left(\frac{\pi}{4} + \frac{\varphi_{\max}}{2}\right) \right] = \pi$$

$$\tan\left(\frac{\pi}{4} + \frac{\varphi_{\max}}{2}\right) = e^{\pi}$$

$$\varphi_{\max} = 2 \left( \arctan(e^\pi) - \frac{\pi}{4} \right) \approx 1.4844222\text{ rad} \approx 85.051129^\circ$$

* Domain: $\lambda \in [-\pi, \pi]$, $\varphi \in [-\varphi_{\max}, +\varphi_{\max}]$
* Projected Range: $X, Y \in [-\pi R, +\pi R]$

---

## 3. Laboratory Tasks

### Task 1: Analytical Derivations
1. Prove step-by-step that the condition $Y(\varphi_{\max}) = \pi R$ yields $\varphi_{\max} \approx 85.051129^\circ$.
2. Derive the expression for the differential surface area on a sphere $dA_{\text{sphere}} = R^2 \cos\varphi \, d\varphi \, d\lambda$, and verify that the ratio $\frac{dA_{\text{proj}}}{dA_{\text{sphere}}}$ matches the areal distortion $s = \sec^2\varphi$ for Spherical Mercator.

---

### Task 2: Distortion Analysis & Tabulation
Given $R = 6371\text{ km}$, evaluate $Y$, scale factor $k$, and areal factor $s$ at the latitudes specified in the table below.

| Latitude ($\varphi$) | Plate Carrée $Y$ (km) | Mercator $Y$ (km) | Plate Carrée $k$ | Mercator $k$ | Plate Carrée Area Factor ($s$) | Mercator Area Factor ($s$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $0^\circ$ (Equator) | `0.0` | `0.0` | `1.000` | `1.000` | `1.000` | `1.000` |
| $15^\circ$ (Low Latitude) | | | | | | |
| $45^\circ$ (Mid Latitude) | | | | | | |
| $60^\circ$ (Sub-polar) | | | | | | |
| $85.051129^\circ$ (Cutoff) | | | | | | |

*Complete the blank entries in your lab submission.*

---

### Task 3: Computational Modeling & Tissot Indicatrices

Create a Python script (`distortion_analysis.py`) to reproduce the quantitative metrics and plot the distortions.

```python
import numpy as np
import matplotlib.pyplot as plt

# Constants
R = 6371.0  # Earth radius in km

lat_deg = np.linspace(0, 85.051129, 500)
lat_rad = np.radians(lat_deg)

# Plate Carrée
y_plate_carree = R * lat_rad
s_plate_carree = 1.0 / np.cos(lat_rad)

# Web / Spherical Mercator
y_mercator = R * np.log(np.tan(np.pi / 4.0 + lat_rad / 2.0))
s_mercator = 1.0 / (np.cos(lat_rad) ** 2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot Projected Y coordinate
ax1.plot(lat_deg, y_plate_carree, label="Plate Carrée", color="blue", lw=2)
ax1.plot(lat_deg, y_mercator, label="Web Mercator", color="crimson", lw=2)
ax1.set_xlabel("Latitude (degrees)")
ax1.set_ylabel("Projected Y (km)")
ax1.set_title("Meridional Distance from Equator")
ax1.grid(True, linestyle="--", alpha=0.6)
ax1.legend()

# Plot Areal Distortion (Logarithmic Scale)
ax2.semilogy(lat_deg, s_plate_carree, label="Plate Carrée ($s = \sec\phi$)", color="blue", lw=2)
ax2.semilogy(lat_deg, s_mercator, label="Mercator ($s = \sec^2\phi$)", color="crimson", lw=2)
ax2.set_xlabel("Latitude (degrees)")
ax2.set_ylabel("Areal Distortion Factor $s$ (log scale)")
ax2.set_title("Areal Exaggeration Ratio ($dA / dA_0$)")
ax2.grid(True, which="both", linestyle="--", alpha=0.6)
ax2.legend()

plt.tight_layout()
plt.savefig("projection_comparison.png", dpi=300)
plt.show()
```

---

## 4. Discussion & Critique Questions

Address the following questions in your final report:

1. **The Ellipsoidal Compromise:**
   Web Mercator (`EPSG:3857`) takes WGS 84 ellipsoidal coordinates $(\varphi, \lambda)$ but projects them onto a sphere of radius $R = 6378137\text{ m}$ using spherical equations. Explain why this results in a non-conformal mapping on the true reference ellipsoid, and discuss why this trade-off was accepted by web cartographers.

2. **Distance and Area Miscalculations:**
   If a GIS user executes a planar buffer operation $\Delta D = \sqrt{\Delta X^2 + \Delta Y^2} = 100\text{ km}$ at $\varphi = 60^\circ$ in Web Mercator coordinates:
   * What is the true ground distance of this buffer on the Earth's surface?
   * By what percentage does the nominal buffer area exceed the true ground area?

3. **Tissot's Indicatrix Comparison:**
   Contrast the behavior of an infinitesimal unit circle placed at $\varphi = 60^\circ$ under:
   * Plate Carrée: Semimajor axis $a$, semiminor axis $b$, and orientation.
   * Mercator: Semimajor axis $a$, semiminor axis $b$, and orientation.

---

## 5. Submission Requirements

- **File 1:** `Lab_Report.pdf` (Calculations, filled comparative table, generated plots, and answers to Section 4).
- **File 2:** `distortion_analysis.py` (Reproducible script generating the figures and table values).
