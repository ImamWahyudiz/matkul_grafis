# Bloom Effect - Quick Reference Card

## 🎯 Bloom Effect dalam Satu Halaman

### Apa itu Bloom?
Teknik post-processing yang membuat area terang memancarkan cahaya lembut (glow).

---

## 🔄 Pipeline (5 Tahapan)

```
Scene → Bright Filter → H-Blur → V-Blur → Blend → Screen
```

| Tahap | Fungsi | Parameter Key |
|-------|--------|---------------|
| **1. Render** | Scene ke texture | - |
| **2. Bright Filter** | Extract bright areas | `threshold=2.4` |
| **3. H-Blur** | Blur horizontal | `blurRadius=50` |
| **4. V-Blur** | Blur vertical | `blurRadius=50` |
| **5. Blend** | Combine results | `originalStrength=2`, `blendStrength=1` |

---

## 📊 Formula Penting

### Brightness Calculation
```python
brightness = 0.2126×R + 0.7152×G + 0.0722×B
```

### Bright Filter Decision
```python
if brightness > threshold:
    output = input_color
else:
    output = (0, 0, 0)  # black
```

### Gaussian Blur (per pixel)
```python
result = Σ(pixel[i] × weight[i])
# weight = Gaussian distribution
```

### Additive Blend
```python
final = (original × originalStrength) + (bloom × blendStrength)
```

---

## ⚙️ Parameter Tuning

### Bright Filter Threshold
- **1.0-2.0**: Banyak area glow
- **2.4**: Default (balanced)
- **3.0+**: Hanya area sangat terang

### Blur Radius
- **10-30**: Glow tajam
- **40-60**: Balanced (default=50)
- **70+**: Glow luas

### Original Strength
- **< 1.0**: Scene gelap
- **1.0**: Normal
- **2.0**: Default (lebih terang)
- **> 2.0**: Sangat terang

### Blend Strength
- **< 0.5**: Bloom subtle
- **1.0**: Default (balanced)
- **> 1.5**: Bloom kuat

---

## 💻 Code Template

### Setup
```python
self.postprocessor = Postprocessor(renderer, scene, camera)
```

### Basic Bloom
```python
self.postprocessor.addEffect(BrightFilterEffect(2.4))
self.postprocessor.addEffect(HorizontalBlurEffect(
    textureSize=[800, 600], blurRadius=50
))
self.postprocessor.addEffect(VerticalBlurEffect(
    textureSize=[800, 600], blurRadius=50
))
mainScene = self.postprocessor.renderTargetList[0].texture
self.postprocessor.addEffect(AdditiveBlendEffect(
    mainScene, originalStrength=2, blendStrength=1
))
```

### Render
```python
self.postprocessor.render()
```

---

## 🎨 Variasi Effect

### Subtle Bloom
```python
BrightFilterEffect(3.0)  # High threshold
HorizontalBlurEffect(blurRadius=30)  # Less blur
VerticalBlurEffect(blurRadius=30)
AdditiveBlendEffect(..., blendStrength=0.5)  # Less intense
```

### Strong Bloom
```python
BrightFilterEffect(1.5)  # Low threshold
HorizontalBlurEffect(blurRadius=80)  # More blur
VerticalBlurEffect(blurRadius=80)
AdditiveBlendEffect(..., blendStrength=2.0)  # Very intense
```

### Dreamy Bloom
```python
BrightFilterEffect(2.0)
HorizontalBlurEffect(blurRadius=100)  # Very large
VerticalBlurEffect(blurRadius=100)
AdditiveBlendEffect(..., originalStrength=1.5, blendStrength=1.5)
```

---

## 🚀 Performance Tips

### Optimizations
1. **Reduce blur radius** → Faster
2. **Lower resolution for blur passes** → Much faster
3. **Use separable filters** (H+V) → Already optimal!
4. **Minimize effect chain** → Less overhead

### Comparison
- 1-Pass 2D Blur: O(n²) → Slow
- 2-Pass Blur: O(2n) → Fast ✓

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Bloom too strong | Decrease `blendStrength` |
| Bloom not visible | Lower `threshold` or increase `blurRadius` |
| Too slow | Reduce `blurRadius` |
| Scene too bright | Decrease `originalStrength` |
| Scene too dark | Increase `originalStrength` |
| Glow too sharp | Increase `blurRadius` |
| Glow too spread | Decrease `blurRadius` |

---

## 📁 File References

| File | Purpose |
|------|---------|
| `10_light-shadow-2.py` | Main demo (with comments) |
| `files/10_light-shadow-2_commented.py` | Heavily commented version |
| `LIGHT_SHADOW_2_README.md` | Complete documentation |
| `files/bloom_tutorial.py` | Interactive tutorial |

---

## 🎮 Controls

- **W/A/S/D**: Move camera
- **Q/E**: Up/Down
- **Mouse**: Look around

---

## 💡 Key Concepts

1. **Post-Processing**: Render to texture, then process
2. **Multi-Pass Rendering**: Multiple rendering passes
3. **Separable Filters**: 2-pass blur (H+V) is efficient
4. **Additive Blending**: Colors are added, not replaced
5. **Threshold Filtering**: Extract bright areas only

---

## 📚 Learn More

Run:
```bash
python files/bloom_tutorial.py          # Interactive tutorial
python 10_light-shadow-2.py             # Visual demo
```

Read:
- `LIGHT_SHADOW_2_README.md` - Full documentation
- `files/10_light-shadow-2_commented.py` - Annotated code

---

**Quick Start:**
```python
# Minimal bloom effect
postprocessor.addEffect(BrightFilterEffect(2.4))
postprocessor.addEffect(HorizontalBlurEffect(blurRadius=50))
postprocessor.addEffect(VerticalBlurEffect(blurRadius=50))
postprocessor.addEffect(AdditiveBlendEffect(originalScene, 2, 1))
postprocessor.render()
```

**That's it! 🌟**
