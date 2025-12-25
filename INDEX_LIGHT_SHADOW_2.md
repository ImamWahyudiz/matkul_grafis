# 📚 Index Dokumentasi - 10_light-shadow-2.py

## Daftar Lengkap Dokumentasi & Resources

Dokumentasi ini menjelaskan program **10_light-shadow-2.py** yang mendemonstrasikan **Bloom Effect** menggunakan **Post-Processing**.

---

## 📖 Dokumentasi Utama

### 1. 🚀 Quick Reference (Mulai di sini!)
**File:** [BLOOM_QUICK_REFERENCE.md](../BLOOM_QUICK_REFERENCE.md)

**Isi:**
- Bloom pipeline dalam 1 halaman
- Formula penting
- Parameter tuning guide
- Code templates
- Troubleshooting

**Kapan menggunakan:**
- Butuh referensi cepat
- Sudah familiar dengan konsep
- Ingin copy-paste code template

---

### 2. 📘 Complete Documentation
**File:** [LIGHT_SHADOW_2_README.md](../LIGHT_SHADOW_2_README.md)

**Isi:**
- Penjelasan lengkap setiap komponen
- Diagram ASCII art
- Contoh perhitungan detail
- Formula matematis
- Visual quality tips
- Performance optimization
- Latihan & eksperimen

**Kapan menggunakan:**
- Belajar dari awal
- Ingin pemahaman mendalam
- Butuh penjelasan detail setiap tahap

---

### 3. 🎓 Interactive Tutorial
**File:** [files/bloom_tutorial.py](bloom_tutorial.py)

**Cara menjalankan:**
```bash
python files/bloom_tutorial.py
```

**Isi:**
- Tutorial interaktif step-by-step
- Penjelasan konsep dengan diagram
- Contoh perhitungan
- Parameter tuning guide
- Progress dengan Enter key

**Kapan menggunakan:**
- Ingin belajar secara interaktif
- Lebih suka tutorial guided
- Ingin visualisasi ASCII

---

## 💻 Source Code

### 4. 🎯 Original Program
**File:** [10_light-shadow-2.py](../10_light-shadow-2.py)

**Status:** ✅ Telah ditambahkan komentar lengkap

**Cara menjalankan:**
```bash
python 10_light-shadow-2.py
```

**Isi:**
- Program utama dengan komentar
- Implementasi bloom effect
- Setup scene, camera, objects
- Post-processing pipeline

---

### 5. 📝 Heavily Commented Version
**File:** [files/10_light-shadow-2_commented.py](10_light-shadow-2_commented.py)

**Isi:**
- Versi dengan komentar sangat detail
- Penjelasan setiap baris code
- Docstrings lengkap
- Inline comments untuk logika kompleks

**Kapan menggunakan:**
- Membaca code sambil belajar
- Ingin pemahaman implementasi detail
- Reference saat coding sendiri

---

## 🎯 Panduan Penggunaan Berdasarkan Level

### 👶 Pemula (Belum tahu apa-apa tentang Bloom)
1. ✅ Baca [LIGHT_SHADOW_2_README.md](../LIGHT_SHADOW_2_README.md) (konsep dasar)
2. ✅ Jalankan [bloom_tutorial.py](bloom_tutorial.py) (interactive learning)
3. ✅ Jalankan [10_light-shadow-2.py](../10_light-shadow-2.py) (lihat hasilnya)
4. ✅ Baca [10_light-shadow-2_commented.py](10_light-shadow-2_commented.py) (pahami code)
5. ✅ Eksperimen dengan parameter (hands-on)

### 🧑 Menengah (Sudah familiar dengan post-processing)
1. ✅ Baca [BLOOM_QUICK_REFERENCE.md](../BLOOM_QUICK_REFERENCE.md) (refresh memory)
2. ✅ Jalankan [10_light-shadow-2.py](../10_light-shadow-2.py) (lihat implementasi)
3. ✅ Baca code di [10_light-shadow-2_commented.py](10_light-shadow-2_commented.py)
4. ✅ Lihat [LIGHT_SHADOW_2_README.md](../LIGHT_SHADOW_2_README.md) untuk detail tertentu
5. ✅ Eksperimen dengan variasi effect

### 👨‍💻 Advanced (Sudah expert, butuh reference)
1. ✅ [BLOOM_QUICK_REFERENCE.md](../BLOOM_QUICK_REFERENCE.md) (quick lookup)
2. ✅ [10_light-shadow-2.py](../10_light-shadow-2.py) (implementation reference)
3. ✅ [LIGHT_SHADOW_2_README.md](../LIGHT_SHADOW_2_README.md) (specific details)

---

## 📂 Struktur File

```
Grafis/
├── 10_light-shadow-2.py                      # Main program (commented)
├── LIGHT_SHADOW_2_README.md                  # Complete documentation
├── BLOOM_QUICK_REFERENCE.md                  # Quick reference card
├── files/
│   ├── 10_light-shadow-2_commented.py       # Heavily commented version
│   ├── bloom_tutorial.py                     # Interactive tutorial
│   └── INDEX_LIGHT_SHADOW_2.md              # This file!
└── ...
```

---

## 🎓 Topik yang Dijelaskan

### Core Concepts
- ✅ Post-Processing Pipeline
- ✅ Render to Texture (off-screen rendering)
- ✅ Multi-Pass Rendering
- ✅ Bloom Effect

### Techniques
- ✅ Bright Filter (threshold filtering)
- ✅ Gaussian Blur (2-pass: H+V)
- ✅ Additive Blending
- ✅ Color brightness calculation

### Implementation
- ✅ Postprocessor setup
- ✅ Effect chaining
- ✅ Render targets
- ✅ Parameter tuning

---

## 🎮 Cara Menjalankan

### Tutorial Interaktif
```bash
cd /home/Apachersa/Dokumen/Grafis
python files/bloom_tutorial.py
```

### Demo Visual
```bash
cd /home/Apachersa/Dokumen/Grafis
python 10_light-shadow-2.py
```

**Kontrol:**
- W/A/S/D: Move camera
- Q/E: Up/Down
- Mouse: Look around

---

## 🔧 Eksperimen yang Disarankan

### Eksperimen 1: Ubah Threshold
```python
# File: 10_light-shadow-2.py
self.postprocessor.addEffect(BrightFilterEffect(1.5))  # Coba 1.5, 2.0, 3.0, 4.0
```

### Eksperimen 2: Ubah Blur Radius
```python
# Coba: 20, 40, 60, 80, 100
self.postprocessor.addEffect(HorizontalBlurEffect(blurRadius=30))
self.postprocessor.addEffect(VerticalBlurEffect(blurRadius=30))
```

### Eksperimen 3: Ubah Blend Strength
```python
self.postprocessor.addEffect(AdditiveBlendEffect(
    mainScene,
    originalStrength=1.5,  # Coba: 1.0, 1.5, 2.0, 3.0
    blendStrength=0.5      # Coba: 0.3, 0.5, 1.0, 1.5, 2.0
))
```

### Eksperimen 4: Tambah Effect Lain
```python
# Sebelum bloom
self.postprocessor.addEffect(VignetteEffect(intensity=0.5))

# Atau setelah bloom
self.postprocessor.addEffect(TintEffect(tintColor=[1.0, 0.9, 0.8]))
```

---

## 📊 Perbandingan Dokumentasi

| File | Length | Detail | Interactive | Code | Best For |
|------|--------|--------|-------------|------|----------|
| Quick Reference | 1 page | Low | ❌ | ✅ | Quick lookup |
| Complete Doc | Long | High | ❌ | ✅ | Deep learning |
| Tutorial | Medium | Medium | ✅ | ❌ | Step-by-step |
| Original Program | Short | Medium | ✅ | ✅ | Running demo |
| Commented Version | Long | High | ✅ | ✅ | Code reading |

---

## 💡 Tips Belajar

1. **Mulai dengan Tutorial**: Pahami konsep dulu
2. **Lihat Demo**: Jalankan program, lihat hasilnya
3. **Baca Code**: Pahami implementasi
4. **Eksperimen**: Ubah parameter, lihat efeknya
5. **Buat Sendiri**: Implementasikan di project Anda

---

## 🔗 Related Topics

### File Lain dalam Project
- `PIPELINE_README.md` - Graphics Pipeline explanation
- `core/pipeline.py` - Pipeline visualization module
- `files/pipeline_demo_*.py` - Pipeline demos

### Konsep Terkait
- Render to Texture
- Framebuffer Objects (FBO)
- Shader Programming
- Post-Processing Effects
- Image Filtering

---

## ❓ FAQ

### Q: Bloom tidak terlihat?
**A:** Coba turunkan threshold atau tingkatkan blur radius.

### Q: Bloom terlalu kuat?
**A:** Kurangi `blendStrength` parameter.

### Q: Program lambat?
**A:** Kurangi `blurRadius` atau texture resolution.

### Q: Bagaimana membuat bloom hanya di objek tertentu?
**A:** Gunakan emission map atau render objek terpisah.

### Q: Bisa kombinasi dengan effect lain?
**A:** Ya! Tambahkan vignette, tint, atau effect lain di chain.

---

## 📞 Need Help?

Jika masih bingung:
1. Baca [LIGHT_SHADOW_2_README.md](../LIGHT_SHADOW_2_README.md) - Section Troubleshooting
2. Jalankan [bloom_tutorial.py](bloom_tutorial.py) - Tutorial interaktif
3. Lihat [BLOOM_QUICK_REFERENCE.md](../BLOOM_QUICK_REFERENCE.md) - Quick tips

---

## ✅ Checklist Pembelajaran

### Konsep
- [ ] Memahami apa itu post-processing
- [ ] Memahami bloom effect pipeline
- [ ] Memahami bright filter
- [ ] Memahami Gaussian blur (2-pass)
- [ ] Memahami additive blending

### Implementasi
- [ ] Bisa setup Postprocessor
- [ ] Bisa chain effects
- [ ] Bisa tune parameters
- [ ] Bisa eksperimen dengan variasi

### Praktik
- [ ] Sudah jalankan demo
- [ ] Sudah baca code
- [ ] Sudah eksperimen parameter
- [ ] Sudah coba kombinasi effect

---

**Selamat belajar! ✨**

Mulai dari file mana pun sesuai level Anda!
