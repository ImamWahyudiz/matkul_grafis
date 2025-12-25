# Graphics Pipeline - Panduan Lengkap

## Apa itu Graphics Pipeline?

**Graphics Pipeline** adalah serangkaian tahapan yang dilalui data geometri 3D untuk ditransformasi menjadi gambar 2D pada layar. Pipeline ini adalah jantung dari rendering grafis 3D modern dan diimplementasikan di GPU (Graphics Processing Unit).

---

## Diagram Graphics Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                      GRAPHICS PIPELINE                          │
└─────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────┐
    │  1. VERTEX SPECIFICATION         │ ← Input: Vertex Data
    │  (Define vertices, attributes)   │   (position, color, normal)
    └────────────┬─────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────┐
    │  2. VERTEX SHADER                │ ← Programmable!
    │  (Transform vertices, MVP)       │   (Model-View-Projection)
    └────────────┬─────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────┐
    │  3. PRIMITIVE ASSEMBLY           │
    │  (Group vertices into primitives)│   (Triangles, Lines, Points)
    └────────────┬─────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────┐
    │  4. RASTERIZATION                │
    │  (Convert primitives to fragments)│
    └────────────┬─────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────┐
    │  5. FRAGMENT SHADER              │ ← Programmable!
    │  (Calculate pixel colors)        │   (Lighting, Texturing)
    └────────────┬─────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────┐
    │  6. PER-SAMPLE OPERATIONS        │
    │  (Depth test, blending)          │
    └────────────┬─────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────┐
    │     FRAMEBUFFER (Screen)         │ ← Output: Pixels!
    └──────────────────────────────────┘
```

---

## Tahapan Detail Graphics Pipeline

### 1. Vertex Specification
**Apa yang terjadi?**
- Mendefinisikan data vertex yang akan dirender
- Setiap vertex memiliki atribut (position, color, normal, texture coordinates)
- Data vertex disimpan di Vertex Buffer Object (VBO)

**Contoh Data:**
```python
vertices = [
    # Position          Color
    [-0.5, -0.5, 0.0,   1.0, 0.0, 0.0],  # Vertex 1 (merah)
    [ 0.5, -0.5, 0.0,   0.0, 1.0, 0.0],  # Vertex 2 (hijau)
    [ 0.0,  0.5, 0.0,   0.0, 0.0, 1.0]   # Vertex 3 (biru)
]
```

**File Demo:** `pipeline_demo_1_konsep.py`

---

### 2. Vertex Shader (Programmable)
**Apa yang terjadi?**
- Program yang berjalan **sekali per vertex**
- Mentransformasi posisi vertex dari object space ke clip space
- Menggunakan Model-View-Projection (MVP) matrices

**Transformasi Coordinate Spaces:**

```
Object Space (Local)
    ↓ Model Matrix (scaling, rotation, translation)
World Space
    ↓ View Matrix (camera position & orientation)
View Space (Camera Space)
    ↓ Projection Matrix (perspective/orthographic)
Clip Space
    ↓ Perspective Division (divide by w)
Normalized Device Coordinates (NDC)
    ↓ Viewport Transform
Screen Space (Pixels)
```

**Contoh Vertex Shader (GLSL):**
```glsl
// Input (per-vertex attributes)
attribute vec3 vertexPosition;
attribute vec3 vertexColor;

// Uniforms (same for all vertices)
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;

// Output (to fragment shader)
varying vec3 color;

void main() {
    // Transformasi posisi vertex
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
    
    // Pass color to fragment shader
    color = vertexColor;
}
```

**Tanggung Jawab Vertex Shader:**
- ✅ Transformasi posisi vertex (WAJIB: set `gl_Position`)
- ✅ Perhitungan lighting per-vertex (optional)
- ✅ Meneruskan data ke fragment shader via `varying`

**File Demo:** `pipeline_demo_2_transform.py`

---

### 3. Primitive Assembly
**Apa yang terjadi?**
- Menggabungkan vertices menjadi primitif geometri
- Melakukan clipping (membuang geometri di luar view frustum)
- Melakukan face culling (membuang back-facing triangles)

**Jenis Primitif:**
- `GL_POINTS`: Setiap vertex = 1 titik
- `GL_LINES`: Setiap 2 vertices = 1 garis
- `GL_LINE_STRIP`: Vertices membentuk garis connected
- `GL_TRIANGLES`: Setiap 3 vertices = 1 segitiga
- `GL_TRIANGLE_STRIP`: Vertices membentuk strip segitiga
- `GL_TRIANGLE_FAN`: Vertices membentuk fan segitiga

**Contoh:**
```
Vertices: [V0, V1, V2, V3, V4, V5]

GL_TRIANGLES:
  Triangle 1: V0, V1, V2
  Triangle 2: V3, V4, V5

GL_TRIANGLE_STRIP:
  Triangle 1: V0, V1, V2
  Triangle 2: V1, V2, V3
  Triangle 3: V2, V3, V4
```

---

### 4. Rasterization
**Apa yang terjadi?**
- Mengkonversi primitif geometri menjadi **fragments**
- Fragment = "pixel candidate" (belum tentu jadi pixel)
- Setiap fragment berisi:
  - Posisi layar (x, y)
  - Depth value (z)
  - Atribut yang di-interpolasi dari vertices

**Proses Interpolasi:**
Atribut dari vertices (warna, texture coords) di-interpolasi untuk setiap fragment di dalam primitif.

**Contoh:**
```
Segitiga dengan 3 vertices:
  V1: posisi=(0,0), warna=(1,0,0) merah
  V2: posisi=(10,0), warna=(0,1,0) hijau
  V3: posisi=(5,10), warna=(0,0,1) biru

Fragment di tengah segitiga akan mendapat warna campuran:
  warna = (0.33, 0.33, 0.33) - keabuan
```

**File Demo:** `pipeline_demo_4_rasterization.py`

---

### 5. Fragment Shader (Programmable)
**Apa yang terjadi?**
- Program yang berjalan **sekali per fragment** (per pixel candidate)
- Menghitung warna final untuk setiap fragment
- Dapat melakukan texture sampling, lighting calculations, effects

**Contoh Fragment Shader (GLSL):**
```glsl
// Input (interpolated from vertex shader)
varying vec3 color;

// Uniforms
uniform sampler2D textureSampler;
uniform float brightness;

void main() {
    // Hitung warna final
    vec3 finalColor = color * brightness;
    
    // Atau sample dari texture:
    // vec4 texColor = texture2D(textureSampler, texCoords);
    
    // Output warna (WAJIB)
    gl_FragColor = vec4(finalColor, 1.0);
}
```

**Tanggung Jawab Fragment Shader:**
- ✅ Menghitung warna final (WAJIB: set `gl_FragColor`)
- ✅ Texture sampling
- ✅ Lighting calculations (Phong, Lambert)
- ✅ Special effects (fog, bloom, etc)

**File Demo:** `pipeline_demo_3_shaders.py`

---

### 6. Per-Sample Operations
**Apa yang terjadi?**
Serangkaian tests untuk menentukan apakah fragment akan ditulis ke framebuffer:

#### a) **Depth Test (Z-buffering)**
- Membandingkan depth fragment dengan depth buffer
- Hanya fragment terdekat yang lolos
- Mengatasi masalah objek yang overlap

```
if (fragment_depth < depth_buffer[x,y]) {
    depth_buffer[x,y] = fragment_depth;
    framebuffer[x,y] = fragment_color;
}
```

#### b) **Stencil Test**
- Masking area tertentu di layar
- Untuk efek seperti refleksi, shadows, portals

#### c) **Blending**
- Mencampur warna fragment dengan warna di framebuffer
- Untuk transparansi dan efek komposisi

**Blending Equation:**
```
final_color = (src_color * src_factor) + (dst_color * dst_factor)
```

**Contoh Transparansi:**
```
src_factor = src_alpha
dst_factor = (1 - src_alpha)
```

#### d) **Output ke Framebuffer**
- Fragment yang lolos semua test ditulis ke framebuffer
- Framebuffer = buffer yang berisi pixel yang akan ditampilkan

---

## Model-View-Projection (MVP) Transformation

### Matriks Transformasi

#### 1. Model Matrix
Mentransformasi dari **Object Space** ke **World Space**

```python
# Scaling
model = Matrix.makeScale(2.0)  # 2x lebih besar

# Rotation
model = Matrix.makeRotationY(angle)  # Rotasi sumbu Y

# Translation
model = Matrix.makeTranslation(x, y, z)  # Pindah posisi

# Kombinasi (SRT order: Scale -> Rotate -> Translate)
model = translation @ rotation @ scale
```

#### 2. View Matrix
Mentransformasi dari **World Space** ke **View Space** (Camera Space)

```python
# Kamera di posisi (0, 5, 10), melihat ke origin
view = Matrix.makeLookAt(
    cameraPosition=[0, 5, 10],
    targetPosition=[0, 0, 0],
    upDirection=[0, 1, 0]
)
```

#### 3. Projection Matrix
Mentransformasi dari **View Space** ke **Clip Space**

```python
# Perspective projection
projection = Matrix.makePerspective(
    angleOfView=60,      # FOV in degrees
    aspectRatio=16/9,    # width/height
    near=0.1,            # Near clipping plane
    far=100.0            # Far clipping plane
)

# Orthographic projection
projection = Matrix.makeOrthographic(
    left=-10, right=10,
    bottom=-10, top=10,
    near=0.1, far=100.0
)
```

#### MVP Matrix (Combined)
```python
mvp = projection @ view @ model
transformed_vertex = mvp @ vertex
```

---

## Vertex Shader vs Fragment Shader

| Aspek | Vertex Shader | Fragment Shader |
|-------|---------------|-----------------|
| **Execution** | Sekali per vertex | Sekali per fragment (pixel candidate) |
| **Input** | Vertex attributes (position, color, etc) | Interpolated data dari vertices |
| **Output** | `gl_Position` (clip space), varying variables | `gl_FragColor` (RGBA color) |
| **Tanggung Jawab** | Transformasi geometri | Perhitungan warna |
| **Dapat Mengubah** | Posisi vertex, geometri | Warna pixel |
| **Contoh Penggunaan** | MVP transform, vertex animation, skinning | Lighting, texturing, post-effects |
| **Jumlah Eksekusi** | Sedikit (per vertex) | Banyak (per pixel) |

**Ilustrasi:**
```
Segitiga dengan 3 vertices, tampil di layar 100x100 pixels

Vertex Shader:   Berjalan 3 kali (untuk 3 vertices)
Fragment Shader: Berjalan ~5000 kali (untuk ~5000 pixels dalam segitiga)
```

---

## Demo Files

### 1. `pipeline_demo_1_konsep.py`
**Penjelasan konsep interaktif** tentang setiap tahapan pipeline
- Menjelaskan setiap tahapan dengan teks
- Menunjukkan data yang mengalir melalui pipeline
- Interaktif dengan prompt untuk melanjutkan

**Cara menjalankan:**
```bash
python files/pipeline_demo_1_konsep.py
```

### 2. `pipeline_demo_2_transform.py`
**Visualisasi transformasi vertex** (MVP transformation)
- 3 kubus mendemonstrasikan berbagai transformasi
- Kubus 1: Static (object space reference)
- Kubus 2: Rotasi (model transformation)
- Kubus 3: Rotasi + scale (multiple transformations)

**Cara menjalankan:**
```bash
python files/pipeline_demo_2_transform.py
```

### 3. `pipeline_demo_3_shaders.py`
**Demonstrasi Vertex Shader vs Fragment Shader**
- Sphere kiri: Vertex shader effect (wave animation)
- Sphere kanan: Fragment shader effect (color animation)
- Menunjukkan perbedaan antara vertex processing dan fragment processing

**Cara menjalankan:**
```bash
python files/pipeline_demo_3_shaders.py
```

### 4. `pipeline_demo_4_rasterization.py`
**Demonstrasi Rasterization dan Depth Testing**
- Toggle render mode: Filled / Wireframe / Points
- Objek yang overlap untuk demo depth testing
- Visualisasi primitive types

**Cara menjalankan:**
```bash
python files/pipeline_demo_4_rasterization.py
```

**Kontrol:**
- `W/A/S/D`: Gerak kamera
- `Q/E`: Naik/turun
- Mouse: Rotasi kamera
- `1/2/3`: Toggle render mode (demo 4)

---

## Module: `core/pipeline.py`

Module ini berisi kelas-kelas untuk menjelaskan dan mendemonstrasikan pipeline:

### Class: `PipelineVisualizer`
Menjelaskan setiap tahapan pipeline dengan teks dan contoh data.

**Methods:**
- `explain_vertex_specification()` - Tahap 1
- `explain_vertex_processing()` - Tahap 2
- `explain_primitive_assembly()` - Tahap 3
- `explain_rasterization()` - Tahap 4
- `explain_fragment_processing()` - Tahap 5
- `explain_output_operations()` - Tahap 6
- `explain_full_pipeline()` - Menjalankan semua tahapan

### Class: `ShaderPipelineExplainer`
Menjelaskan peran shader dalam pipeline.

**Methods:**
- `explain_vertex_shader()` - Penjelasan vertex shader
- `explain_fragment_shader()` - Penjelasan fragment shader
- `explain_shader_pipeline()` - Alur data dalam shader

**Contoh penggunaan:**
```python
from core.pipeline import PipelineVisualizer, ShaderPipelineExplainer

# Explain full pipeline
PipelineVisualizer.explain_full_pipeline()

# Explain shaders
ShaderPipelineExplainer.explain_shader_pipeline()
```

---

## Konsep Penting

### 1. Coordinate Spaces
- **Object Space**: Koordinat lokal objek (relatif terhadap pivot point)
- **World Space**: Koordinat dalam dunia 3D global
- **View Space**: Koordinat relatif terhadap kamera
- **Clip Space**: Koordinat setelah projection, sebelum perspective division
- **NDC (Normalized Device Coordinates)**: Koordinat normalized [-1, 1]
- **Screen Space**: Koordinat pixel di layar

### 2. Homogeneous Coordinates
Vertex menggunakan 4 komponen (x, y, z, w) untuk transformasi:
- w = 1: Point (dipengaruhi translation)
- w = 0: Vector (tidak dipengaruhi translation)

### 3. Perspective Division
Setelah MVP transformation, divide by w:
```
x' = x / w
y' = y / w
z' = z / w
```

### 4. Interpolation
Atribut vertex di-interpolasi linear untuk setiap fragment:
```
fragment_attr = α * v1_attr + β * v2_attr + γ * v3_attr
(α + β + γ = 1, barycentric coordinates)
```

### 5. Depth Buffer (Z-buffer)
Array 2D yang menyimpan depth value untuk setiap pixel:
```
depth_buffer[width][height]
```
Mencegah objek jauh menimpa objek dekat.

---

## Tips Optimasi

### Vertex Shader
- Hitung sebanyak mungkin di vertex shader (lebih sedikit eksekusi)
- Pindahkan perhitungan konstan ke CPU (uniform)
- Gunakan built-in functions (faster)

### Fragment Shader
- Hindari operasi mahal (sqrt, pow, trigonometry)
- Batasi texture lookups
- Gunakan mipmapping untuk texture
- Early fragment test (discard)

### General
- Minimize vertex count (LOD - Level of Detail)
- Batch rendering (less draw calls)
- Frustum culling (jangan render yang tidak terlihat)
- Backface culling (jangan render back faces)

---

## Troubleshooting

### Objek tidak muncul
- ✅ Check MVP matrices
- ✅ Check vertex positions dalam range [-1, 1] di NDC
- ✅ Check depth test enabled
- ✅ Check face culling

### Warna salah
- ✅ Check fragment shader output
- ✅ Check attribute interpolation
- ✅ Check uniform values

### Z-fighting (flickering)
- ✅ Increase near/far plane ratio di projection matrix
- ✅ Use higher precision depth buffer
- ✅ Separate overlapping objects

---

## Resources & References

### OpenGL Documentation
- [OpenGL Wiki - Rendering Pipeline](https://www.khronos.org/opengl/wiki/Rendering_Pipeline_Overview)
- [learnopengl.com](https://learnopengl.com/)

### Buku
- "OpenGL Programming Guide" (Red Book)
- "Real-Time Rendering" by Akenine-Möller

### Online Courses
- [OpenGL Tutorial](http://www.opengl-tutorial.org/)
- [3D Graphics Fundamentals](https://www.scratchapixel.com/)

---

## Kesimpulan

Graphics Pipeline adalah proses kompleks yang mentransformasi data 3D menjadi gambar 2D di layar. Memahami setiap tahapan pipeline sangat penting untuk:

1. **Debugging** - Mengetahui dimana masalah terjadi
2. **Optimasi** - Mengidentifikasi bottleneck
3. **Efek Visual** - Membuat shader dan efek custom
4. **Performance** - Membuat aplikasi grafis yang efisien

**Key Takeaways:**
- Vertex Shader: Transform geometry
- Fragment Shader: Calculate colors
- Pipeline adalah fixed-function + programmable stages
- GPU menjalankan shader secara parallel (sangat cepat!)
- Memahami coordinate spaces sangat penting
- Depth testing mengatasi overlapping objects

Selamat belajar! 🚀
