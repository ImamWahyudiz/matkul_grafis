# Penjelasan: 10_light-shadow-2.py - Bloom Effect & Post-Processing

## 📋 Deskripsi Program

Program ini mendemonstrasikan teknik **Post-Processing** dalam grafis komputer, khususnya untuk membuat efek **Light Bloom** (cahaya bercahaya). Bloom effect membuat area terang dalam scene memancarkan cahaya yang lembut dan menyebar, menciptakan efek visual yang lebih realistis dan dramatis.

## 🎯 Tujuan Pembelajaran

1. Memahami konsep **Post-Processing** dalam graphics pipeline
2. Mempelajari cara kerja **Bloom Effect**
3. Memahami **Multi-Pass Rendering**
4. Mempelajari teknik **Gaussian Blur**
5. Memahami **Additive Blending** untuk menggabungkan efek

---

## 🔧 Komponen Utama

### 1. Scene Components

#### Sky (Langit)
```python
skyGeometry = SphereGeometry(radius=50)
earthTexture = Texture("images/sky-earth.png")
skyMaterial = TextureMaterial(earthTexture)
sky = Mesh(skyGeometry, skyMaterial)
```

**Penjelasan:**
- Menggunakan **sphere besar** (radius=50) sebagai skybox
- Texture dibungkus di bagian dalam sphere
- Camera berada di dalam sphere sehingga melihat langit di semua arah
- Teknik ini disebut **skybox** atau **skydome**

#### Grass (Rumput)
```python
grassGeometry = RectangleGeometry(width=100, height=100)
grassTexture = Texture("images/grass.png")
grassMaterial = TextureMaterial(grassTexture, {"repeatUV":[50,50]})
grass = Mesh(grassGeometry, grassMaterial)
grass.rotateX(-3.14*0.5)  # Rotasi 90° untuk horizontal
```

**Penjelasan:**
- Rectangle besar (100x100) sebagai ground plane
- Texture diulang 50x50 kali (`repeatUV`) untuk detail
- Dirotasi 90° agar horizontal (tanah)

#### Sphere (Objek Utama)
```python
sphereGeometry = SphereGeometry()
sphereTexture = Texture("images/grid.png")
sphereMaterial = TextureMaterial(sphereTexture)
self.sphere = Mesh(sphereGeometry, sphereMaterial)
self.sphere.setPosition([0,1,0])
```

**Penjelasan:**
- Sphere dengan texture grid
- Posisi di ketinggian 1 unit (melayang di atas tanah)
- Objek fokus yang akan mendapat bloom effect

---

## 🌟 Post-Processing Pipeline

### Apa itu Post-Processing?

**Post-Processing** adalah teknik rendering dimana scene di-render dulu ke texture (bukan langsung ke screen), kemudian texture tersebut diproses dengan berbagai efek sebelum ditampilkan di layar.

### Alur Post-Processing:

```
┌─────────────────────────────────────────────────────────┐
│                POST-PROCESSING PIPELINE                 │
└─────────────────────────────────────────────────────────┘

    ┌──────────────────────────┐
    │  1. RENDER SCENE         │ → Render ke texture (off-screen)
    │     to Render Target     │
    └──────────┬───────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │  2. BRIGHT FILTER        │ → Extract bagian terang (bright)
    │     (threshold = 2.4)    │   Hanya area > threshold yang lolos
    └──────────┬───────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │  3. HORIZONTAL BLUR      │ → Blur horizontal (spread cahaya)
    │     (radius = 50 pixels) │
    └──────────┬───────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │  4. VERTICAL BLUR        │ → Blur vertical (spread cahaya)
    │     (radius = 50 pixels) │
    └──────────┬───────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │  5. ADDITIVE BLEND       │ → Gabung scene asli + bloom
    │     (combine results)    │   originalStrength=2, blendStrength=1
    └──────────┬───────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │  FINAL IMAGE to Screen   │ → Output ke layar
    └──────────────────────────┘
```

---

## 📊 Detail Setiap Effect

### Effect 1: Bright Filter Effect

**Kode:**
```python
self.postprocessor.addEffect(BrightFilterEffect(2.4))
```

**Cara Kerja:**
- Menganalisis setiap pixel dalam scene
- Hanya pixel dengan brightness > threshold (2.4) yang dilewatkan
- Pixel yang kurang terang menjadi hitam
- Menghasilkan texture yang hanya berisi area terang

**Formula:**
```glsl
// Pseudo-code fragment shader
vec3 color = texture2D(mainTexture, uv).rgb;
float brightness = dot(color, vec3(0.2126, 0.7152, 0.0722)); // Luminance
if (brightness > threshold) {
    gl_FragColor = vec4(color, 1.0);
} else {
    gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
}
```

**Parameter:**
- `threshold = 2.4`: Nilai ambang brightness (lebih tinggi = lebih selektif)

---

### Effect 2: Horizontal Blur Effect

**Kode:**
```python
self.postprocessor.addEffect(HorizontalBlurEffect(
    textureSize=[800,600],
    blurRadius=50
))
```

**Cara Kerja:**
- Mengaplikasikan **Gaussian blur** secara horizontal
- Setiap pixel di-blend dengan pixel tetangganya di kiri-kanan
- Menciptakan efek "spreading" cahaya ke horizontal

**Gaussian Blur Formula:**
```
result = Σ (pixel[i] × weight[i])

Contoh untuk radius 3:
weights = [0.06, 0.24, 0.40, 0.24, 0.06]
result = pixel[-2]×0.06 + pixel[-1]×0.24 + pixel[0]×0.40 + 
         pixel[1]×0.24 + pixel[2]×0.06
```

**Parameter:**
- `textureSize=[800,600]`: Resolusi texture untuk menghitung step
- `blurRadius=50`: Jarak blur dalam pixels (lebih besar = blur lebih jauh)

---

### Effect 3: Vertical Blur Effect

**Kode:**
```python
self.postprocessor.addEffect(VerticalBlurEffect(
    textureSize=[800,600],
    blurRadius=50
))
```

**Cara Kerja:**
- Sama seperti horizontal blur, tapi arah vertikal (atas-bawah)
- Mengaplikasikan Gaussian blur pada hasil horizontal blur
- **2-Pass Blur** (horizontal + vertical) = blur 2D yang efisien

**Mengapa 2-Pass?**
- 1-Pass blur 2D: Kompleksitas O(n²) → sangat lambat
- 2-Pass blur (H+V): Kompleksitas O(2n) → jauh lebih cepat
- Hasil visual hampir identik!

**Ilustrasi:**
```
Original      → Horizontal Blur  → Vertical Blur
■■■■■■■■■        ▓▓▓▓▓▓▓▓▓         ░░░░░░░░░
■■■██■■■■   →    ▓▓████▓▓▓    →    ░░░██░░░░
■■■■■■■■■        ▓▓▓▓▓▓▓▓▓         ░░░░░░░░░
```

**Parameter:**
- `textureSize=[800,600]`: Resolusi texture
- `blurRadius=50`: Jarak blur vertical

---

### Effect 4: Additive Blend Effect

**Kode:**
```python
mainScene = self.postprocessor.renderTargetList[0].texture
self.postprocessor.addEffect(AdditiveBlendEffect(
    mainScene,
    originalStrength=2,
    blendStrength=1
))
```

**Cara Kerja:**
- Menggabungkan **scene original** dengan **blurred bright areas**
- Menggunakan **additive blending** (penjumlahan warna)
- Menciptakan efek bloom akhir

**Formula:**
```glsl
vec3 originalColor = texture2D(originalTexture, uv).rgb;
vec3 bloomColor = texture2D(blurredTexture, uv).rgb;

vec3 finalColor = (originalColor * originalStrength) + 
                  (bloomColor * blendStrength);

gl_FragColor = vec4(finalColor, 1.0);
```

**Parameter:**
- `mainScene`: Texture scene original (sebelum effect)
- `originalStrength=2`: Multiplier untuk scene original (lebih terang)
- `blendStrength=1`: Multiplier untuk bloom effect

**Hasil:**
- Area terang memancarkan cahaya lembut (glow)
- Scene overall menjadi lebih dramatis dan cinematic

---

## 🎮 Controls (Kontrol Kamera)

```python
self.rig = MovementRig()
self.rig.add(self.camera)
self.rig.update(self.input, self.deltaTime)
```

**Kontrol:**
- **W/A/S/D**: Gerak kamera (depan/kiri/belakang/kanan)
- **Q/E**: Naik/turun
- **Mouse**: Rotasi kamera (look around)

---

## 🔬 Konsep Teknis

### 1. Render Target
**Apa itu?**
- Off-screen buffer untuk rendering
- Scene di-render ke texture, bukan langsung ke screen
- Texture ini kemudian bisa diproses lebih lanjut

**Keuntungan:**
- Memungkinkan post-processing effects
- Multi-pass rendering
- Dapat disimpan untuk keperluan lain

### 2. Multi-Pass Rendering
**Konsep:**
```
Pass 1: Render scene → Render Target 1
Pass 2: Apply Effect 1 → Render Target 2
Pass 3: Apply Effect 2 → Render Target 3
Pass 4: Apply Effect 3 → Render Target 4
Pass 5: Combine & output → Screen
```

**Dalam program ini:**
- Pass 1: Scene rendering
- Pass 2: Bright filter
- Pass 3: Horizontal blur
- Pass 4: Vertical blur
- Pass 5: Additive blend → Screen

### 3. Bloom Effect Components

**Komponen Bloom:**
1. **Threshold**: Menentukan area mana yang "glow"
2. **Blur**: Menyebarkan cahaya (create glow)
3. **Blend**: Menggabungkan dengan scene original

**Formula Lengkap:**
```
Bloom = AdditiveBlend(
    OriginalScene,
    VerticalBlur(
        HorizontalBlur(
            BrightFilter(OriginalScene)
        )
    )
)
```

---

## 📈 Parameter Tuning Guide

### Bright Filter Threshold
```python
BrightFilterEffect(threshold)
```
- **Lebih kecil (1.0-2.0)**: Lebih banyak area yang glow
- **Default (2.4)**: Balance yang baik
- **Lebih besar (3.0+)**: Hanya area sangat terang yang glow

### Blur Radius
```python
HorizontalBlurEffect(blurRadius=50)
VerticalBlurEffect(blurRadius=50)
```
- **Kecil (10-30)**: Glow tajam, subtle
- **Medium (40-60)**: Glow balanced
- **Besar (70+)**: Glow sangat luas, dreamy

### Blend Strengths
```python
AdditiveBlendEffect(originalStrength=2, blendStrength=1)
```

**Original Strength:**
- **< 1.0**: Scene gelap
- **1.0**: Scene normal
- **> 1.0**: Scene lebih terang

**Blend Strength:**
- **< 0.5**: Bloom subtle
- **1.0**: Bloom balanced
- **> 1.5**: Bloom sangat kuat

---

## 🎨 Variasi Effect (Commented Code)

Program menyediakan efek lain yang bisa diaktifkan:

### 1. Brightness Only
```python
self.postprocessor.addEffect(BrightFilterEffect())
```
Hasil: Hanya area terang (tanpa blur)

### 2. Vertical Blur Only
```python
self.postprocessor.addEffect(VerticalBlurEffect())
```
Hasil: Blur vertikal pada seluruh scene

### 3. Horizontal Blur Only
```python
self.postprocessor.addEffect(HorizontalBlurEffect())
```
Hasil: Blur horizontal pada seluruh scene

---

## 💡 Tips & Best Practices

### Performance
1. **Blur Radius**: Lebih besar = lebih lambat
2. **Texture Size**: Gunakan resolusi lebih kecil untuk blur pass
3. **Effect Chain**: Lebih sedikit effect = lebih cepat

### Visual Quality
1. **Balance**: Jangan over-bloom (terlalu terang)
2. **Threshold**: Sesuaikan dengan lighting scene
3. **Blur Radius**: Sesuaikan dengan resolusi screen

### Troubleshooting
- **Bloom terlalu kuat**: Kurangi `blendStrength`
- **Bloom tidak terlihat**: Turunkan `threshold` atau tingkatkan `blurRadius`
- **Performance lambat**: Kurangi `blurRadius` atau texture size

---

## 🔗 Efek Tambahan yang Tersedia

Program ini mengimpor berbagai effect lain yang bisa digunakan:

1. **InvertEffect**: Membalik warna
2. **PixelateEffect**: Efek pixelated/retro
3. **TintEffect**: Memberikan tint warna
4. **VignetteEffect**: Gelap di tepi layar
5. **ColorReduceEffect**: Mengurangi jumlah warna (posterize)

**Contoh penggunaan:**
```python
# Tambahkan vignette untuk efek cinematic
self.postprocessor.addEffect(VignetteEffect(intensity=0.5))

# Atau pixelate untuk efek retro
self.postprocessor.addEffect(PixelateEffect(pixelSize=4))
```

---

## 📚 Referensi & Bacaan Lebih Lanjut

### Bloom Effect
- [Learn OpenGL - Bloom](https://learnopengl.com/Advanced-Lighting/Bloom)
- [GPU Gems - Bloom](https://developer.nvidia.com/gpugems/gpugems/part-iv-image-processing/chapter-21-real-time-glow)

### Post-Processing
- [Post-Processing Effects](https://en.wikipedia.org/wiki/Video_post-processing)
- [Real-Time Rendering Chapter on Post-Processing](http://www.realtimerendering.com/)

### Gaussian Blur
- [Gaussian Blur Explanation](https://en.wikipedia.org/wiki/Gaussian_blur)
- [Separable Filters](https://www.rastergrid.com/blog/2010/09/efficient-gaussian-blur-with-linear-sampling/)

---

## 🎓 Latihan & Eksperimen

### Latihan 1: Tune Parameters
Coba ubah parameter berikut dan amati hasilnya:
```python
# Eksperimen dengan threshold
BrightFilterEffect(1.5)  # atau 2.0, 3.0, 4.0

# Eksperimen dengan blur radius
HorizontalBlurEffect(blurRadius=20)  # atau 40, 80, 100

# Eksperimen dengan strength
AdditiveBlendEffect(mainScene, originalStrength=1.5, blendStrength=0.5)
```

### Latihan 2: Tambahkan Efek Lain
```python
# Sebelum bloom
self.postprocessor.addEffect(VignetteEffect())

# Atau setelah bloom
# ... bloom effects ...
self.postprocessor.addEffect(TintEffect(tintColor=[1.0, 0.9, 0.8]))
```

### Latihan 3: Buat Objek Lebih Banyak
Tambahkan lebih banyak sphere dengan berbagai warna:
```python
# Sphere merah terang (akan glow)
redSphere = Mesh(sphereGeometry, brightRedMaterial)
redSphere.setPosition([2, 1, 0])
self.scene.add(redSphere)
```

---

## 🎬 Kesimpulan

Program ini mendemonstrasikan:

1. ✅ **Post-Processing Pipeline** - Multi-pass rendering
2. ✅ **Bloom Effect** - Light glow yang realistis
3. ✅ **Gaussian Blur** - Efficient 2-pass blur
4. ✅ **Additive Blending** - Menggabungkan hasil
5. ✅ **Real-time Effects** - Semua berjalan real-time

**Key Takeaways:**
- Post-processing adalah teknik powerful untuk visual effects
- Bloom membuat scene lebih cinematic dan realistic
- 2-Pass blur (H+V) lebih efisien dari 1-pass 2D blur
- Parameter tuning sangat penting untuk hasil optimal
- Effect chaining memungkinkan kombinasi kompleks

Selamat bereksperimen dengan bloom effect! ✨
