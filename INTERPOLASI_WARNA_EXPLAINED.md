# Penjelasan: Kenapa 6 Warna Menjadi Banyak Gradasi Warna?

## 📌 Pertanyaan
Dalam file [`5_interpolasi.py`](5_interpolasi.py), kita hanya mendefinisikan **6 warna** untuk 6 vertex hexagon:

```python
colorData = [ 
    [1.0, 0.0, 0.0],  # Merah
    [1.0, 0.5, 0.0],  # Orange
    [1.0, 1.0, 0.0],  # Kuning
    [0.0, 1.0, 0.0],  # Hijau
    [0.0, 0.0, 1.0],  # Biru
    [0.5, 0.0, 1.0]   # Ungu
]
```

Tapi kenapa hasilnya muncul **ribuan warna** dengan gradasi halus di antara vertex-vertex tersebut?

---

## 🎨 Jawaban Singkat

**INTERPOLASI OTOMATIS** oleh GPU!

GPU secara otomatis menghitung warna untuk setiap pixel di antara vertex menggunakan teknik bernama **"interpolation"** atau **"smooth shading"**.

---

## 📖 Penjelasan Detail

### 1️⃣ Yang Kita Definisikan (Vertex Colors)

Kita hanya mendefinisikan warna di **6 titik vertex** (sudut hexagon):

```
     Vertex 2 (Kuning)
          ●
         ╱ ╲
        ╱   ╲
V1(O) ●     ● V3 (Hijau)
       ╲   ╱
        ╲ ╱
         ●
    Vertex 4 (Biru)
```

**Hanya 6 warna yang kita tentukan!**

---

### 2️⃣ Proses di GPU (Pipeline Grafis)

#### **Vertex Shader** (Berjalan per Vertex)
```glsl
in vec3 vertexColor;    // Input: warna dari CPU (6 warna)
out vec3 color;         // Output: dikirim ke Fragment Shader

void main(){
    gl_Position = vec4(position.x, position.y, position.z, 1.0);
    color = vertexColor;  // ✅ Warna vertex diteruskan
}
```

**Output Vertex Shader:**
- Vertex 1: `color = (1.0, 0.0, 0.0)` → Merah
- Vertex 2: `color = (1.0, 0.5, 0.0)` → Orange  
- Vertex 3: `color = (1.0, 1.0, 0.0)` → Kuning
- ... dst

---

#### **Rasterization Stage** (Magic Happens Here! ✨)

Setelah Vertex Shader, GPU melakukan **Rasterization**:

1. **Membentuk Segitiga** dari vertex
   - Dengan `GL_TRIANGLE_FAN`, hexagon dibagi jadi 4 segitiga
   
2. **Mengisi Pixel di Dalam Segitiga**
   - GPU menghitung warna untuk **SETIAP PIXEL** di dalam segitiga
   
3. **INTERPOLASI LINEAR**
   - Untuk setiap pixel, GPU menghitung warna dengan **mencampur warna vertex terdekat**

**Contoh Interpolasi:**

```
Vertex A (Merah: 1,0,0)
    ●
    |\
    | \
    |  \     ← Pixel di tengah ini dapat warna CAMPURAN
    |   \
    |    \
    ●─────●
Vertex B      Vertex C
(Hijau: 0,1,0) (Biru: 0,0,1)
```

Untuk pixel di **tengah segitiga**:
- Jarak ke A = 33%
- Jarak ke B = 33%
- Jarak ke C = 34%

**Warna pixel = (0.33×Merah) + (0.33×Hijau) + (0.34×Biru)**
```
= (0.33, 0.33, 0.34) → Warna abu-abu kecoklatan
```

---

#### **Fragment Shader** (Berjalan per Pixel)
```glsl
in vec3 color;           // ✅ Sudah di-interpolasi oleh GPU!
out vec4 fragColor;

void main(){
    fragColor = vec4(color.r, color.g, color.b, 1.0);
}
```

**Input Fragment Shader:**
- Pixel 1: `color = (1.0, 0.0, 0.0)` → Merah murni (di vertex)
- Pixel 2: `color = (0.95, 0.05, 0.0)` → Merah-orange (interpolasi)
- Pixel 3: `color = (0.9, 0.1, 0.0)` → Orange kemerahan (interpolasi)
- Pixel 4: `color = (0.85, 0.15, 0.0)` → Orange (interpolasi)
- ... **RIBUAN PIXEL LAINNYA dengan warna ter-interpolasi!**

---

### 3️⃣ Formula Interpolasi (Barycentric Coordinates)

GPU menggunakan **Barycentric Coordinates** untuk interpolasi:

```
ColorPixel = (w1 × Color1) + (w2 × Color2) + (w3 × Color3)

Dimana:
- w1, w2, w3 = bobot berdasarkan jarak ke masing-masing vertex
- w1 + w2 + w3 = 1.0 (total 100%)
```

**Contoh Konkrit:**

Segitiga dengan vertex:
- V1 (0, 0): Merah `(1, 0, 0)`
- V2 (1, 0): Hijau `(0, 1, 0)`  
- V3 (0.5, 1): Biru `(0, 0, 1)`

Pixel di koordinat `(0.5, 0.3)`:
```
w1 = 0.4  (40% ke V1)
w2 = 0.3  (30% ke V2)
w3 = 0.3  (30% ke V3)

ColorPixel = 0.4×(1,0,0) + 0.3×(0,1,0) + 0.3×(0,0,1)
           = (0.4, 0.3, 0.3)
           = Orange kecoklatan
```

---

## 🔢 Berapa Banyak Warna yang Dihasilkan?

Misalkan resolusi layar **800×600 pixel**:

1. **Total pixel dalam hexagon** ≈ 200,000 pixel (tergantung ukuran)

2. **Setiap pixel mendapat warna unik** hasil interpolasi

3. **Total warna berbeda** = **200,000 warna**! (dari 6 warna awal)

---

## 🎯 Analogi Sederhana

Bayangkan kamu punya **3 cat warna**:
- 🔴 Merah
- 🟢 Hijau  
- 🔵 Biru

Jika kamu **mencampur** cat tersebut dengan proporsi berbeda-beda:

| Merah | Hijau | Biru | Hasil                      |
|-------|-------|------|----------------------------|
| 100%  | 0%    | 0%   | 🔴 Merah murni            |
| 70%   | 30%   | 0%   | 🟠 Orange                  |
| 50%   | 50%   | 0%   | 🟡 Kuning                  |
| 30%   | 70%   | 0%   | 🟢 Hijau kekuningan       |
| 0%    | 100%  | 0%   | 🟢 Hijau murni            |
| 0%    | 50%   | 50%  | 🟦 Cyan (biru kehijauan)  |
| 33%   | 33%   | 34%  | ⚫ Abu-abu                 |

Dari **3 warna dasar**, kamu bisa buat **JUTAAN kombinasi warna**!

Itulah yang dilakukan GPU dengan interpolasi.

---

## 📊 Visualisasi Pipeline

```
┌──────────────────────────────────────────────────────────┐
│               PROSES INTERPOLASI WARNA                   │
└──────────────────────────────────────────────────────────┘

1. CPU mengirim data:
   ┌─────────────────┐
   │ 6 Vertex Colors │  ← Hanya 6 warna!
   │ [Merah, Orange, │
   │  Kuning, Hijau, │
   │  Biru, Ungu]    │
   └────────┬────────┘
            │
            ▼
2. Vertex Shader:
   ┌─────────────────┐
   │  Proses 6 kali  │  ← Sekali per vertex
   │ (untuk 6 vertex)│
   └────────┬────────┘
            │
            ▼
3. Rasterization:
   ┌─────────────────────────┐
   │   INTERPOLASI OTOMATIS  │  ← Magic happens!
   │                         │
   │  GPU menghitung warna   │
   │  untuk SETIAP PIXEL     │
   │  di dalam segitiga      │
   │                         │
   │  Menggunakan:           │
   │  - Barycentric coords   │
   │  - Linear interpolation │
   └────────┬────────────────┘
            │
            ▼
4. Fragment Shader:
   ┌─────────────────────┐
   │ Proses 200,000 kali │  ← Sekali per pixel!
   │ (untuk 200k pixel)  │
   │                     │
   │ Setiap pixel dapat  │
   │ warna ter-interpolasi│
   └────────┬────────────┘
            │
            ▼
5. Framebuffer:
   ┌─────────────────────┐
   │  200,000 warna unik │  ← Hasil akhir!
   │  dengan gradasi     │
   │  halus dan smooth   │
   └─────────────────────┘
```

---

## 💡 Poin Penting

### ✅ Yang Dilakukan GPU (Otomatis)
1. **Interpolasi Linear** antar vertex
2. **Smooth Shading** (gradasi halus)
3. **Per-pixel color calculation**
4. **Barycentric coordinate blending**

### ❌ Yang TIDAK Kita Lakukan Manual
1. ❌ Tidak perlu menghitung warna setiap pixel
2. ❌ Tidak perlu definisikan ribuan warna
3. ❌ Tidak perlu kode untuk blending
4. ❌ Tidak perlu loop untuk interpolasi

**Semua dilakukan OTOMATIS oleh hardware GPU!**

---

## 🔬 Eksperimen

### Test 1: Ganti ke Flat Shading
Tambahkan keyword `flat` di shader:

```glsl
// Vertex Shader
out flat vec3 color;  // ← Tambahkan "flat"

// Fragment Shader  
in flat vec3 color;   // ← Tambahkan "flat"
```

**Hasil:**
- ❌ Tidak ada interpolasi
- Setiap segitiga hanya punya **1 warna solid**
- Terlihat **tidak smooth**, ada batasan jelas antar warna

---

### Test 2: Kurangi Jumlah Vertex
Ubah hexagon jadi segitiga (3 vertex, 3 warna):

```python
positionData = [ 
    [0.0, 0.8, 0.0],   # Atas
    [-0.8, -0.8, 0.0], # Kiri bawah
    [0.8, -0.8, 0.0]   # Kanan bawah
]

colorData = [ 
    [1.0, 0.0, 0.0],  # Merah
    [0.0, 1.0, 0.0],  # Hijau
    [0.0, 0.0, 1.0]   # Biru
]
```

**Hasil:**
- Tetap mendapat **gradasi warna smooth**
- Di tengah segitiga: campuran merah+hijau+biru = abu-abu
- Di tepi: gradasi dari merah ke hijau, hijau ke biru, biru ke merah

---

## 📚 Kesimpulan

### Kenapa 6 Warna Jadi Ribuan Warna?

1. **GPU melakukan interpolasi otomatis** antar vertex
2. **Setiap pixel** mendapat warna hasil **blending** dari vertex terdekat
3. **Barycentric coordinates** digunakan untuk menghitung bobot blending
4. **Rasterization stage** yang melakukan perhitungan ini
5. **Fragment Shader menerima** warna yang **sudah ter-interpolasi**

### Formula Sederhana:
```
Warna Input    → 6 warna di vertex
Proses         → Interpolasi linear GPU (otomatis)
Warna Output   → 200,000+ warna unik
```

---

## 🎓 Istilah Penting

- **Vertex Color**: Warna yang didefinisikan di titik vertex
- **Interpolation**: Proses menghitung nilai di antara 2+ nilai
- **Rasterization**: Konversi geometri vektor ke pixel raster
- **Fragment**: Pixel kandidat (sebelum jadi pixel final)
- **Smooth Shading**: Shading dengan interpolasi (default)
- **Flat Shading**: Shading tanpa interpolasi (solid color)
- **Barycentric Coordinates**: Sistem koordinat untuk posisi dalam segitiga

---

## 🔗 Referensi

- Pipeline Demo: [`pipeline_demo_4_rasterization.py`](pipeline_demo_4_rasterization.py)
- Core Implementation: [`core/pipeline.py`](core/pipeline.py)
- OpenGL Spec: Rasterization & Fragment Interpolation

---

**Dibuat:** 25 Desember 2025  
**File Terkait:** [`5_interpolasi.py`](5_interpolasi.py)
