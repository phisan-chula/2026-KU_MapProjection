# แบบฝึกหัด: Planar (Azimuthal) Map Projections และ Tissot Indicatrix

## วัตถุประสงค์

ให้นิสิตฝึกใช้ **Python** และ **Cartopy** เพื่อสร้างแผนที่ด้วยการฉายแบบ **Planar / Azimuthal Projection** และศึกษาความบิดเบือนของแผนที่จาก **Tissot Indicatrix**

เมื่อทำแบบฝึกหัดเสร็จ นิสิตควรสามารถ

1. สร้างแผนที่ด้วย Azimuthal Projection ได้
2. กำหนดจุดศูนย์กลางของการฉายแผนที่ได้
3. แสดงโลกเต็มใบด้วย `ax.set_global()`
4. วาด Graticule ทุก 10°
5. แสดง Tissot Indicatrix
6. อธิบายความแตกต่างระหว่าง **Conformal**, **Equal-area** และ **Equidistant projection** ได้

---

## 1. กำหนดค่าการทดลอง

กำหนดจุดศูนย์กลางของการฉายแผนที่เป็น

$$
\phi_0 = 15^\circ N
$$

$$
\lambda_0 = 100^\circ E
$$

ซึ่งอยู่บริเวณประเทศไทย

กำหนด Graticule ทุก

$$
10^\circ
$$

ทั้ง Longitude และ Latitude

---

# งานที่ 1: Stereographic Projection

สร้างแผนที่โลกเต็มใบด้วย

```python
ccrs.Stereographic()
```

กำหนด

```python
central_latitude = 15
central_longitude = 100
```

และใช้

```python
ax.set_global()
```

ให้แสดงองค์ประกอบต่อไปนี้

* Coastline
* Country boundary
* Graticule ทุก 10°
* Central Meridian = 100°E เป็นเส้นสีแดง
* Central Latitude = 15°N เป็นเส้นสีแดง
* Projection Center เป็นจุดสีแดง
* Tissot Indicatrix ทุก 10°

กำหนดรัศมีของ Tissot Indicatrix เช่น

```python
rad_km = 300
```

ให้สังเกตลักษณะของ Tissot Indicatrix เมื่ออยู่ห่างจาก Projection Center

---

# งานที่ 2: Lambert Azimuthal Equal-Area Projection

เปลี่ยน Projection เป็น

```python
ccrs.LambertAzimuthalEqualArea()
```

โดยยังคงใช้

```python
central_latitude = 15
central_longitude = 100
```

และแสดงโลกเต็มใบด้วย

```python
ax.set_global()
```

ใช้องค์ประกอบของแผนที่เหมือนกับงานที่ 1

ให้สังเกต

* รูปร่างของ Tissot Indicatrix
* ขนาดของ Tissot Indicatrix
* การเปลี่ยนแปลงเมื่ออยู่ห่างจาก Projection Center

---

# งานที่ 3: Azimuthal Equidistant Projection

เปลี่ยน Projection เป็น

```python
ccrs.AzimuthalEquidistant()
```

กำหนด

```python
central_latitude = 15
central_longitude = 100
```

และแสดงโลกเต็มใบด้วย

```python
ax.set_global()
```

ให้นิสิตเปรียบเทียบ Tissot Indicatrix กับ Projection สองชนิดก่อนหน้า

---

# ตารางเปรียบเทียบ Projection

| Projection                   | ลักษณะ Tissot Indicatrix | คุณสมบัติที่รักษา        |
| ---------------------------- | ------------------------ | ------------------------ |
| Stereographic                | วงกลม แต่ขนาดเปลี่ยน     | **Conformal**            |
| Lambert Azimuthal Equal-Area | วงรี แต่พื้นที่คงที่     | **Equal-area**           |
| Azimuthal Equidistant        | วงรี และขนาดเปลี่ยน      | **Distance from center** |

---

# งานที่ 4: เปรียบเทียบผล

ให้นิสิตจัดทำรูปจำนวน **3 รูป**

```text
01_Stereographic.png
02_Lambert_Azimuthal_EqualArea.png
03_Azimuthal_Equidistant.png
```

แต่ละรูปต้องมีองค์ประกอบดังต่อไปนี้

* แสดงโลกเต็มใบ
* ใช้ Projection Center เดียวกัน
* Graticule ทุก 10°
* Tissot Indicatrix ทุก 10°
* Central Meridian สีแดง
* Central Latitude สีแดง
* Projection Center
* ชื่อ Projection
* Legend

---

# คำถามท้ายแบบฝึกหัด

## ข้อ 1

จาก Tissot Indicatrix ของ **Stereographic Projection** เพราะเหตุใดวงกลมจึงยังคงเป็นวงกลม แม้ว่าขนาดจะเปลี่ยนไปเมื่ออยู่ห่างจาก Projection Center

---

## ข้อ 2

**Lambert Azimuthal Equal-Area Projection** ทำให้ Tissot Indicatrix เปลี่ยนจากวงกลมเป็นวงรี

อธิบายว่าเหตุใดพื้นที่ของ Tissot Indicatrix จึงยังคงสัมพันธ์กับพื้นที่เดิมบนผิวโลก

---

## ข้อ 3

สำหรับ **Azimuthal Equidistant Projection** ระยะทางประเภทใดที่ถูกต้อง

เลือกคำตอบที่ถูกต้องและอธิบาย

* a. ระยะทางระหว่างทุกคู่จุดบนแผนที่
* b. ระยะทางตามเส้น Latitude
* c. ระยะทางจาก Projection Center ไปยังจุดอื่น
* d. ระยะทางตาม Central Meridian เท่านั้น

---

## ข้อ 4

เปรียบเทียบ Shape Distortion ของ Projection ทั้งสามชนิด เมื่ออยู่ห่างจาก Projection Center มากขึ้น

อธิบายโดยใช้ลักษณะของ Tissot Indicatrix ประกอบ

---

## ข้อ 5

อธิบายความแตกต่างระหว่าง

* **Conformal**
* **Equal-area**
* **Equidistant**

โดยใช้ Tissot Indicatrix ประกอบคำอธิบาย





Tissot Indicatrix จะช่วยให้สามารถสังเกต

* Angular distortion
* Shape distortion
* Scale distortion
* Area distortion

ของ Projection แต่ละชนิดได้โดยตรง

---

# ผลที่คาดว่าจะสังเกตได้

## 1. Stereographic

Stereographic เป็น **Conformal Projection**

ดังนั้นที่ตำแหน่งใด ๆ

$$
k_1 = k_2
$$

หรือในรูป Tissot Indicatrix

$$
a=b
$$

ดังนั้น Tissot Indicatrix ยังคงเป็น **วงกลม**

อย่างไรก็ตาม ขนาดของวงกลมจะเปลี่ยนเมื่ออยู่ห่างจาก Projection Center

ดังนั้น

$$
\boxed{\text{Conformal}}
$$

---

## 2. Lambert Azimuthal Equal-Area

Tissot Indicatrix โดยทั่วไปจะเปลี่ยนจากวงกลมเป็นวงรี

$$
a \neq b
$$

แต่ผลคูณของ Scale Factors ยังคงรักษาพื้นที่

$$
k_1 k_2 = 1
$$

ดังนั้น

$$
\boxed{\text{Equal-area}}
$$

---

## 3. Azimuthal Equidistant

Azimuthal Equidistant Projection รักษาระยะทางจาก Projection Center

ในทิศทาง Radial

$$
k_r = 1
$$

แต่ในทิศทาง Tangential

$$
k_t \neq 1
$$

ดังนั้น Tissot Indicatrix จะเปลี่ยนเป็นวงรีมากขึ้นเมื่ออยู่ห่างจาก Projection Center

$$
\boxed{\text{Distance from Projection Center is preserved}}
$$

---

# สรุป

Projection ทั้งสามเป็น **Azimuthal / Planar Projections** แต่รักษาคุณสมบัติแตกต่างกัน

| Projection                   | Angle | Area | Distance from Center |
| ---------------------------- | :---: | :--: | :------------------: |
| Stereographic                |   ✓   |   ✗  |           ✗          |
| Lambert Azimuthal Equal-Area |   ✗   |   ✓  |           ✗          |
| Azimuthal Equidistant        |   ✗   |   ✗  |           ✓          |

Tissot Indicatrix เป็นเครื่องมือสำคัญที่ช่วยให้มองเห็นความแตกต่างของ Map Distortion ระหว่าง Projection ทั้งสามชนิดได้อย่างชัดเจน

---

# สิ่งที่ต้องส่ง

1. รูปผลลัพธ์จำนวน 3 รูป

```text
01_Stereographic.png
02_Lambert_Azimuthal_EqualArea.png
03_Azimuthal_Equidistant.png
**Tissot Indicatrix แสดง Map Distortion ของ Projection ทั้งสามชนิดอย่างไร**
```

