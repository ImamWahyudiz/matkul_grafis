# Urutan Pembelajaran Graphics Pipeline
## Dari Vertex Sampai Rendering Lengkap

Dokumen ini menjelaskan urutan logis untuk mempelajari graphics pipeline menggunakan file-file yang tersedia, dari konsep paling dasar hingga teknik rendering advanced.

---

## 📚 TAHAP 0: Persiapan dan Konsep Dasar Pipeline

### **Demo Interaktif Pipeline (MULAI DI SINI)**
Jalankan demo interaktif untuk memahami konsep pipeline secara visual:

```bash
python pipeline_demo_00_pervertex.py
```

**Apa yang dipelajari:**
- ✅ Visualisasi vertex individual (step-by-step)
- ✅ Primitive assembly (titik → garis → segitiga)
- ✅ Proses rasterization
- ✅ Transisi otomatis ke demo berikutnya

Demo ini akan melanjutkan secara otomatis ke:pygame.error: File is not a Windows BMP file
- `pipeline_demo_1_konsep.py` - Penjelasan konsep lengkap
- `pipeline_demo_2_transform.py` - MVP transformation
- `pipeline_demo_3_shaders.py` - Vertex & Fragment shaders
- `pipeline_demo_4_rasterization.py` - Depth testing

---

## 🎯 TAHAP 1: Foundation - Setup Window & OpenGL Context

### **1_buat-window.py** - Membuat Window Kosong
```bash
python 1_buat-window.py
```

**Konsep Graphics Pipeline:**
- ⚙️ **Initialization Phase**: Setup OpenGL context
- 🖥️ **Display System**: Membuat surface untuk rendering
- 🔄 **Game Loop**: Update loop untuk rendering continuous

**Yang dipelajari:**
- Inisialisasi Pygame dan OpenGL
- Membuat window dengan OpenGL context
- Game loop dasar (initialize → update loop)
- Framebuffer sebagai target rendering

**Posisi di Pipeline:**
```
┌─────────────────────────────────────────┐
│  OUTPUT: Framebuffer (Window kosong)   │ ← Kita di sini
└─────────────────────────────────────────┘
```

---

## 🔺 TAHAP 2: Vertex Specification - Data Mentah

### **2_buat-titik.py** - Render Titik Pertama
```bash
python 2_buat-titik.py
```

**Konsep Graphics Pipeline:**
- 📍 **Vertex Specification**: Mendefinisikan vertex di hardcode
- 📝 **Vertex Shader**: Program paling sederhana (position fix)
- 🎨 **Fragment Shader**: Warna solid
- 🔢 **VAO (Vertex Array Object)**: Container untuk vertex config

**Yang dipelajari:**
- Vertex hardcoded di shader: `vec4(0.9, 0.9, 0, 1.0)`
- Vertex Shader minimal (tanpa input attribute)
- Fragment Shader dengan warna fix
- VAO dan GL_POINTS rendering
- `glPointSize()` untuk ukuran titik

**Posisi di Pipeline:**
```
┌──────────────────┐
│ Vertex Shader    │ ← Vertex hardcoded di shader
│ gl_Position = .. │
└──────────────────┘
         ↓
┌──────────────────┐
│ Primitive Asm.   │ (GL_POINTS)
└──────────────────┘
         ↓
┌──────────────────┐
│ Fragment Shader  │ ← Warna fix
└──────────────────┘
         ↓
┌──────────────────┐
│ Framebuffer      │
└──────────────────┘
```

---

### **3_buat-hexagonal.py** - Vertex dari CPU ke GPU
```bash
python 3_buat-hexagonal.py
```

**Konsep Graphics Pipeline:**
- 📤 **Vertex Buffer**: Data dari CPU → GPU
- 🔗 **Vertex Attribute**: Binding position data
- 📏 **Primitive Type**: GL_LINE_LOOP untuk wireframe
- 🎯 **Attribute Pointer**: Konfigurasi data layout

**Yang dipelajari:**
- Vertex data dari Python array (CPU) → GPU buffer
- `Attribute` class untuk manage vertex buffer
- Vertex shader dengan `in vec3 position`
- `associateVariable()` untuk binding shader input
- GL_LINE_LOOP untuk menggambar outline

**Posisi di Pipeline:**
```
CPU Memory                          GPU Memory
┌──────────────┐                   ┌──────────────┐
│ Python Array │ ─────upload────→  │ VBO (Buffer) │
│ [x, y, z]    │                   │              │
└──────────────┘                   └──────────────┘
                                          ↓
                                   ┌──────────────┐
                                   │ Vertex Shader│ ← Terima via 'in'
                                   │ in vec3 pos  │
                                   └──────────────┘
```

---

### **4_buat-dua-bentuk.py** - Multiple Objects
```bash
python 4_buat-dua-bentuk.py
```

**Yang dipelajari:**
- Render multiple primitives
- Multiple VAO untuk object terpisah
- Draw call per object (`glDrawArrays` multiple kali)

---

## 🎨 TAHAP 3: Vertex Attributes & Interpolation

### **5_interpolasi.py** - Vertex Color & Interpolation
```bash
python 5_interpolasi.py
```

**Konsep Graphics Pipeline:**
- 🌈 **Vertex Attributes**: Position + Color per vertex
- 🔄 **Varying Variables**: Data dari vertex → fragment shader
- 🎨 **Rasterization**: Interpolasi otomatis antara vertex
- 🖌️ **Fragment Shader**: Terima color yang sudah di-interpolasi

**Yang dipelajari:**
- Multiple attributes per vertex (position + color)
- Vertex shader output: `out vec3 color`
- Fragment shader input: `in vec3 color`
- Rasterizer secara otomatis interpolasi color antar vertex
- Barycentric interpolation (dijelaskan otomatis oleh GPU)

**Posisi di Pipeline:**
```
Vertex Data (CPU)
┌──────────────────────┐
│ Position   Color     │
│ [x,y,z]   [r,g,b]   │ ← Multiple attributes
└──────────────────────┘
         ↓ upload
┌──────────────────────┐
│ Vertex Shader        │
│ in vec3 position;    │
│ in vec3 vertexColor; │
│ out vec3 color;      │ ← Pass ke fragment
└──────────────────────┘
         ↓
┌──────────────────────┐
│ Rasterizer           │ ← INTERPOLASI TERJADI DI SINI!
│ • Triangle pixels    │    Warna di-interpolasi smooth
│ • Interpolate color  │    dari 3 vertex ke setiap pixel
└──────────────────────┘
         ↓
┌──────────────────────┐
│ Fragment Shader      │
│ in vec3 color;       │ ← Terima hasil interpolasi
│ fragColor = vec4(..);│    per fragment/pixel
└──────────────────────┘
```

**Konsep Penting - Interpolation:**
- Jika vertex A = merah, B = hijau, C = biru
- Pixel di tengah akan otomatis dapat campuran warna
- Ini dilakukan oleh rasterizer, bukan programmer
- Disebut "perspective-correct interpolation"

---

## 🔧 TAHAP 4: Uniform Variables & Animation

### **6_uniform.py** - Uniform Variables
```bash
python 6_uniform.py
```

**Konsep Graphics Pipeline:**
- 🌍 **Uniform Variables**: Data global untuk semua vertex
- ⏱️ **Time-based Animation**: Update uniform per frame
- 🔄 **Dynamic Updates**: `glUniform*` untuk update nilai

**Yang dipelajari:**
- Uniform untuk data yang sama untuk semua vertex
- `uniform vec3 translation` untuk geser semua vertex
- Update uniform tiap frame untuk animasi
- Perbedaan attribute (per-vertex) vs uniform (global)

**Posisi di Pipeline:**
```
CPU (Python)                    GPU (Shader)
┌──────────────┐                ┌──────────────┐
│ time += dt   │                │ uniform float│ ← Global untuk
│ translation  │ ─glUniform→    │ time;        │   SEMUA vertex
└──────────────┘                └──────────────┘
                                       ↓
Per-vertex data                 ┌──────────────┐
┌──────────────┐                │ Vertex Shader│
│ position     │ ─attribute→    │ in vec3 pos; │
│ color        │                │ + translation│
└──────────────┘                └──────────────┘
```

**Attribute vs Uniform:**
- **Attribute**: Berbeda tiap vertex (posisi, warna)
- **Uniform**: Sama untuk semua vertex (waktu, transform matrix)

---

### **7_gerak.py** - Animation & Movement
```bash
python 7_gerak.py
```

**Yang dipelajari:**
- Animasi dengan uniform
- Sine wave untuk smooth motion
- Update shader uniform setiap frame

---

## 📦 TAHAP 5: 3D Transformation & Camera

### **8_segitiga_balok.py** - 3D Objects & Camera
```bash
python 8_segitiga_balok.py
```

**Konsep Graphics Pipeline:**
- 📐 **3D Coordinates**: Vertex dalam 3D space (x, y, z)
- 🎥 **Camera System**: View transformation
- 📊 **Projection Matrix**: 3D → 2D projection
- 🎭 **Model Matrix**: Object transformation (local → world)
- 🌍 **MVP Matrix**: Model-View-Projection pipeline

**Yang dipelajari:**
- Sistem koordinat 3D
- Camera class untuk view matrix
- Renderer untuk projection matrix
- Mesh system (geometry + material)
- Scene graph untuk multiple objects

**Posisi di Pipeline:**
```
Object Space (Local)
┌──────────────┐
│ Vertex [x,y,z]│ Model matrix
└──────────────┘     ↓
        ↓
World Space
┌──────────────┐
│ World coords │ View matrix
└──────────────┘     ↓
        ↓
View Space (Camera)
┌──────────────┐
│ Camera space │ Projection matrix
└──────────────┘     ↓
        ↓
Clip Space
┌──────────────┐
│ NDC coords   │ Perspective divide
└──────────────┘     ↓
        ↓
Screen Space
┌──────────────┐
│ Pixels       │
└──────────────┘
```

**MVP Transformation:**
```glsl
// Vertex shader
uniform mat4 modelMatrix;      // Local → World
uniform mat4 viewMatrix;       // World → Camera
uniform mat4 projectionMatrix; // Camera → Clip

void main() {
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    //            └─────────────── MVP Matrix ─────────────┘
}
```

---

## 🖼️ TAHAP 6: Textures & Sampling

### **9_texture-1.py** - Basic Texture Mapping
```bash
python 9_texture-1.py
```

**Konsep Graphics Pipeline:**
- 🗺️ **UV Coordinates**: 2D texture coordinates (0-1 range)
- 🖼️ **Texture Object**: Image data di GPU
- 🎯 **Texture Sampling**: Ambil warna dari texture
- 📌 **Texture Coordinates**: Map vertex → texture position

**Yang dipelajari:**
- UV coordinates sebagai vertex attribute
- `sampler2D` uniform untuk texture
- `texture()` function di fragment shader
- Texture loading dari file image

**Posisi di Pipeline:**
```
Image File                      GPU Texture Memory
┌──────────────┐                ┌──────────────┐
│ grass.png    │ ──load──→      │ Texture Unit │
│ 512x512 RGBA │                │ sampler2D    │
└──────────────┘                └──────────────┘
                                       ↓
Vertex Data                     Vertex Shader
┌──────────────┐                ┌──────────────┐
│ position     │ ──→            │ in vec3 pos; │
│ UV coords    │ ──→            │ in vec2 uv;  │
│ [0-1, 0-1]   │                │ out vec2 UV; │ ← Pass ke fragment
└──────────────┘                └──────────────┘
                                       ↓
                                Rasterizer
                                (interpolate UV)
                                       ↓
                                Fragment Shader
                                ┌──────────────┐
                                │ in vec2 UV;  │
                                │ uniform      │
                                │ sampler2D tex│
                                │ color =      │
                                │ texture(tex, │ ← SAMPLING
                                │         UV); │
                                └──────────────┘
```

**Texture Coordinate System:**
```
(0,1) ────────── (1,1)   ← Top
  │                 │
  │     Texture     │
  │                 │
(0,0) ────────── (1,0)   ← Bottom
```

---

### **9_texture-2.py** - Multiple Textures
```bash
python 9_texture-2.py
```

**Yang dipelajari:**
- Multiple texture pada object berbeda
- Texture untuk skybox (sphere)
- Texture untuk ground plane

---

### **9_texture-3.py** - Texture Transformations
```bash
python 9_texture-3.py
```

**Yang dipelajari:**
- Repeat texture dengan wrap mode
- Texture coordinate manipulation
- UV scaling dan offset

---

### **9_texture-4.py sampai 9_texture-11.py** - Advanced Texturing
```bash
python 9_texture-4.py  # Texture blending
python 9_texture-5.py  # Multi-texturing
python 9_texture-7.py  # Text rendering
python 9_texture-8.py  # Sprite animation
python 9_texture-9.py  # Billboard sprites
```

**Konsep Advanced:**
- Multi-texture blending
- Procedural textures
- Text rendering dengan texture
- Sprite sheets dan animation
- Billboard technique (always face camera)

---

## 💡 TAHAP 7: Lighting & Shading

### **10_light-shadow-1.py** - Basic Lighting
```bash
python 10_light-shadow-1.py
```

**Konsep Graphics Pipeline:**
- 💡 **Light Sources**: Directional, Point, Ambient
- 📐 **Normal Vectors**: Surface orientation
- 🎨 **Shading Models**: Lambert, Phong
- 🔍 **Light Calculation**: Dilakukan di fragment shader

**Yang dipelajari:**
- Ambient light (constant)
- Directional light (sun-like)
- Point light (bulb-like)
- Normal vectors untuk lighting calculation
- Diffuse reflection (Lambert)
- Specular highlights (Phong)

**Posisi di Pipeline:**
```
Vertex Data                     Vertex Shader
┌──────────────┐                ┌──────────────┐
│ position     │ ──→            │ Calculate    │
│ normal       │ ──→            │ world normal │
│ UV           │                │ world pos    │
└──────────────┘                └──────────────┘
                                       ↓
Light Data (Uniforms)           Fragment Shader
┌──────────────┐                ┌──────────────┐
│ lightPos     │ ──→            │ • Normal     │
│ lightColor   │ ──→            │ • Light dir  │
│ cameraPos    │ ──→            │ • View dir   │
└──────────────┘                │              │
                                │ Calculate:   │
                                │ • Diffuse    │ ← N·L
                                │ • Specular   │ ← (R·V)^n
                                │ • Ambient    │
                                │              │
                                │ Final Color  │
                                └──────────────┘
```

**Lighting Calculation (Phong):**
```glsl
// Fragment shader
vec3 normal = normalize(worldNormal);
vec3 lightDir = normalize(lightPos - worldPos);
vec3 viewDir = normalize(cameraPos - worldPos);

// Ambient
vec3 ambient = ambientLight * materialColor;

// Diffuse
float diff = max(dot(normal, lightDir), 0.0);
vec3 diffuse = diff * lightColor * materialColor;

// Specular
vec3 reflectDir = reflect(-lightDir, normal);
float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
vec3 specular = spec * lightColor;

// Combine
vec3 finalColor = ambient + diffuse + specular;
```

---

### **10_light-shadow-2.py** - Advanced Effects (Bloom)
```bash
python 10_light-shadow-2.py
```

**Konsep Graphics Pipeline:**
- 🌟 **Post-Processing**: Render ke texture, lalu process
- ✨ **Bloom Effect**: Bright areas glow
- 🎭 **Multi-Pass Rendering**: Render → Process → Output
- 🔲 **Render Target**: Render ke texture instead of screen

**Yang dipelajari:**
- Framebuffer Objects (FBO) untuk render-to-texture
- Multi-pass rendering:
  1. Pass 1: Render scene → texture
  2. Pass 2: Extract bright areas
  3. Pass 3: Gaussian blur (horizontal)
  4. Pass 4: Gaussian blur (vertical)
  5. Pass 5: Combine original + blur (additive blend)
- Post-processing effects
- Gaussian blur implementation
- Additive blending

**Posisi di Pipeline:**
```
┌─────────────────────────────────────────────────────┐
│         POST-PROCESSING PIPELINE                    │
└─────────────────────────────────────────────────────┘
           
Pass 1: Scene Rendering
┌──────────────┐
│ Render Scene │ → Texture 1 (Full scene)
└──────────────┘
        ↓
Pass 2: Bright Filter
┌──────────────┐
│ Extract      │ → Texture 2 (Bright areas only)
│ Bright Areas │    if (brightness > threshold)
└──────────────┘
        ↓
Pass 3: Blur Horizontal
┌──────────────┐
│ Gaussian     │ → Texture 3 (Blurred horizontal)
│ Blur X       │    9-tap filter
└──────────────┘
        ↓
Pass 4: Blur Vertical
┌──────────────┐
│ Gaussian     │ → Texture 4 (Blurred both directions)
│ Blur Y       │    9-tap filter
└──────────────┘
        ↓
Pass 5: Combine
┌──────────────┐
│ Additive     │ → Screen
│ Blend:       │    original + blurred
│ scene + bloom│
└──────────────┘
```

**Bloom Effect:**
```glsl
// Pass 2: Bright Filter
vec3 color = texture(sceneTex, UV).rgb;
float brightness = dot(color, vec3(0.2126, 0.7152, 0.0722));
if (brightness > threshold)
    fragColor = vec4(color, 1.0);
else
    fragColor = vec4(0, 0, 0, 1.0);

// Pass 3/4: Gaussian Blur
vec3 result = vec3(0.0);
for (int i = -4; i <= 4; i++) {
    vec2 offset = vec2(i) * texelSize;
    result += texture(inputTex, UV + offset).rgb * weight[abs(i)];
}

// Pass 5: Combine
vec3 original = texture(sceneTex, UV).rgb;
vec3 bloom = texture(blurTex, UV).rgb;
fragColor = vec4(original + bloom * bloomStrength, 1.0);
```

---

## 📊 Ringkasan Pipeline Lengkap

```
┌─────────────────────────────────────────────────────────────┐
│                    GRAPHICS PIPELINE                        │
│                   (Lengkap dari Awal)                       │
└─────────────────────────────────────────────────────────────┘

File: 1_buat-window.py
├─ Initialize OpenGL Context
├─ Create Window & Framebuffer
└─ Setup Game Loop

File: 2_buat-titik.py
├─ Vertex Specification (hardcoded)
├─ Vertex Shader (minimal)
└─ Fragment Shader (fixed color)

File: 3_buat-hexagonal.py
├─ Vertex Buffer Object (VBO)
├─ Vertex Attribute Pointer
└─ Vertex Shader with Attributes

File: 5_interpolasi.py
├─ Multiple Vertex Attributes
├─ Varying Variables
└─ Automatic Interpolation

File: 6_uniform.py
├─ Uniform Variables
├─ Dynamic Updates
└─ Animation

File: 8_segitiga_balok.py
├─ 3D Coordinates
├─ MVP Transformation
│  ├─ Model Matrix
│  ├─ View Matrix
│  └─ Projection Matrix
└─ Camera System

File: 9_texture-*.py
├─ Texture Mapping
├─ UV Coordinates
├─ Texture Sampling
└─ Multi-texturing

File: 10_light-shadow-1.py
├─ Normal Vectors
├─ Light Sources
├─ Lighting Calculations
│  ├─ Ambient
│  ├─ Diffuse
│  └─ Specular
└─ Phong Shading

File: 10_light-shadow-2.py
├─ Render to Texture
├─ Multi-pass Rendering
├─ Post-processing
└─ Bloom Effect
```

---

## 🎓 Rekomendasi Urutan Belajar

### **Pemula (Graphics Pipeline Fundamentals)**
1. `pipeline_demo_00_pervertex.py` - Visual interaktif
2. `1_buat-window.py` - Setup dasar
3. `2_buat-titik.py` - Vertex & shader pertama
4. `3_buat-hexagonal.py` - Vertex buffer
5. `5_interpolasi.py` - Interpolation

### **Intermediate (3D Graphics)**
6. `6_uniform.py` - Animation
7. `8_segitiga_balok.py` - 3D & MVP
8. `9_texture-1.py` hingga `9_texture-3.py` - Texturing
9. `pipeline_demo_2_transform.py` - Transform visualisasi

### **Advanced (Lighting & Effects)**
10. `10_light-shadow-1.py` - Lighting
11. `9_texture-7.py` hingga `9_texture-11.py` - Advanced textures
12. `10_light-shadow-2.py` - Post-processing
13. `pipeline_demo_3_shaders.py` - Shader programming
14. `pipeline_demo_4_rasterization.py` - Depth testing

---

## 💡 Tips Pembelajaran

1. **Jalankan setiap file berurutan** - Jangan skip
2. **Baca kode sambil run** - Lihat hasil visual + kode
3. **Modifikasi nilai** - Ubah warna, posisi, ukuran untuk eksperimen
4. **Perhatikan console output** - Banyak penjelasan di print statements
5. **Gunakan pipeline demos** - Untuk visualisasi konsep

---

## 🔗 Hubungan Antar Konsep

```
Vertex Data (3_buat-hexagonal.py)
    ↓
+ Color Attribute (5_interpolasi.py)
    ↓
+ Uniform Animation (6_uniform.py)
    ↓
+ 3D Transform (8_segitiga_balok.py)
    ↓
+ Texture Mapping (9_texture-1.py)
    ↓
+ Lighting (10_light-shadow-1.py)
    ↓
+ Post-processing (10_light-shadow-2.py)
```

---

**Selamat belajar Graphics Pipeline! 🚀**

Mulai dengan `pipeline_demo_00_pervertex.py` untuk pengalaman interaktif terbaik!
