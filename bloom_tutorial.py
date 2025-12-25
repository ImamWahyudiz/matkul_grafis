"""
Bloom Effect - Interactive Tutorial
====================================
File ini adalah tutorial interaktif yang menjelaskan setiap komponen
dari bloom effect dengan visualisasi step-by-step.

Jalankan file ini untuk memahami bagaimana bloom effect bekerja.
"""

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))


def print_separator(char="=", length=70):
    """Print separator line."""
    print(char * length)


def print_header(title):
    """Print formatted header."""
    print("\n")
    print_separator()
    print(f"  {title}")
    print_separator()
    print()


def explain_bloom_concept():
    """Menjelaskan konsep bloom effect."""
    print_header("APA ITU BLOOM EFFECT?")
    
    print("Bloom effect adalah teknik post-processing yang membuat area terang")
    print("dalam scene memancarkan cahaya lembut (glow).")
    print()
    print("Contoh penggunaan:")
    print("  • Cahaya matahari yang terang")
    print("  • Lampu neon yang menyala")
    print("  • Pantulan cahaya di permukaan metal")
    print("  • Efek magic/fantasy (glow sihir)")
    print()
    print("Bloom membuat scene lebih cinematic dan realistis!")


def explain_post_processing():
    """Menjelaskan konsep post-processing."""
    print_header("POST-PROCESSING PIPELINE")
    
    print("Post-processing adalah teknik dimana scene di-render dulu ke texture")
    print("(off-screen), lalu texture tersebut diproses dengan effects sebelum")
    print("ditampilkan di layar.")
    print()
    print("Perbedaan dengan rendering biasa:")
    print()
    print("NORMAL RENDERING:")
    print("  Scene → GPU → Screen (direct)")
    print()
    print("POST-PROCESSING:")
    print("  Scene → GPU → Texture → Effects → Screen")
    print("         └────────┘       └─────────┘")
    print("       (off-screen)     (processing)")
    print()
    print("Keuntungan:")
    print("  ✓ Dapat apply berbagai efek visual")
    print("  ✓ Multi-pass rendering")
    print("  ✓ Efek yang tidak bisa dilakukan langsung saat render")


def explain_bloom_pipeline():
    """Menjelaskan pipeline bloom effect."""
    print_header("BLOOM EFFECT PIPELINE")
    
    print("Bloom effect terdiri dari 5 tahapan:")
    print()
    print("┌─────────────────────────────────────────────────────┐")
    print("│              BLOOM EFFECT PIPELINE                  │")
    print("└─────────────────────────────────────────────────────┘")
    print()
    print("  ┌────────────────────┐")
    print("  │  1. RENDER SCENE   │  Scene di-render ke texture")
    print("  │     to Texture     │  (off-screen rendering)")
    print("  └─────────┬──────────┘")
    print("            │")
    print("            ▼")
    print("  ┌────────────────────┐")
    print("  │  2. BRIGHT FILTER  │  Extract hanya area terang")
    print("  │  (threshold=2.4)   │  brightness > 2.4 → lewat")
    print("  └─────────┬──────────┘  brightness < 2.4 → hitam")
    print("            │")
    print("            ▼")
    print("  ┌────────────────────┐")
    print("  │ 3. HORIZONTAL BLUR │  Gaussian blur horizontal")
    print("  │   (radius=50px)    │  Spread cahaya ke kiri-kanan")
    print("  └─────────┬──────────┘")
    print("            │")
    print("            ▼")
    print("  ┌────────────────────┐")
    print("  │  4. VERTICAL BLUR  │  Gaussian blur vertical")
    print("  │   (radius=50px)    │  Spread cahaya ke atas-bawah")
    print("  └─────────┬──────────┘")
    print("            │")
    print("            ▼")
    print("  ┌────────────────────┐")
    print("  │ 5. ADDITIVE BLEND  │  Gabung scene + bloom")
    print("  │   (combine)        │  final = (orig×2) + (bloom×1)")
    print("  └─────────┬──────────┘")
    print("            │")
    print("            ▼")
    print("  ┌────────────────────┐")
    print("  │   FINAL OUTPUT     │  Hasil ditampilkan ke layar")
    print("  │    to Screen       │")
    print("  └────────────────────┘")


def explain_bright_filter():
    """Menjelaskan bright filter."""
    print_header("TAHAP 1: BRIGHT FILTER")
    
    print("Bright filter mengekstrak hanya area yang sangat terang.")
    print()
    print("Cara Kerja:")
    print("  1. Hitung brightness setiap pixel")
    print("     Formula: brightness = 0.2126×R + 0.7152×G + 0.0722×B")
    print()
    print("  2. Bandingkan dengan threshold (2.4)")
    print()
    print("  3. Keputusan:")
    print("     • brightness > threshold → keep pixel")
    print("     • brightness < threshold → make black")
    print()
    print("Contoh dengan threshold=2.4:")
    print()
    print("  Input Pixel          Brightness    Output")
    print("  ─────────────────────────────────────────────")
    print("  (1.0, 1.0, 1.0)  →    1.0      →  (0, 0, 0) BLACK")
    print("  (2.0, 2.0, 2.0)  →    2.0      →  (0, 0, 0) BLACK")
    print("  (3.0, 3.0, 3.0)  →    3.0      →  (3, 3, 3) KEEP!")
    print("  (5.0, 4.0, 3.0)  →    4.3      →  (5, 4, 3) KEEP!")
    print()
    print("Hasil: Texture yang hanya berisi area sangat terang")


def explain_gaussian_blur():
    """Menjelaskan Gaussian blur."""
    print_header("TAHAP 2 & 3: GAUSSIAN BLUR")
    
    print("Gaussian blur membuat cahaya menyebar dengan lembut.")
    print()
    print("Mengapa 2-Pass Blur (Horizontal + Vertical)?")
    print()
    print("1-Pass 2D Blur:")
    print("  • Sample (2r+1)² pixels per pixel")
    print("  • Untuk radius=50: 101×101 = 10,201 samples!")
    print("  • Kompleksitas: O(n²) → SANGAT LAMBAT")
    print()
    print("2-Pass Blur (H + V):")
    print("  • Sample 2×(2r+1) pixels per pixel")
    print("  • Untuk radius=50: 101+101 = 202 samples")
    print("  • Kompleksitas: O(2n) → JAUH LEBIH CEPAT")
    print("  • Hasil visual hampir identik!")
    print()
    print("Perbandingan:")
    print("  Radius    1-Pass       2-Pass      Speed Up")
    print("  ───────────────────────────────────────────")
    print("    3       7×7=49      7+7=14       3.5x")
    print("   10      21×21=441   21+21=42     10.5x")
    print("   25      51×51=2601  51+51=102    25.5x")
    print("   50     101×101=10201 101+101=202  50.5x")
    print()
    print("Gaussian Weight Distribution:")
    print()
    print("              ▁▂▃▅▇█▇▅▃▂▁")
    print("       ←──────────┼──────────→")
    print("        -r    center    +r")
    print()
    print("Pixel di center mendapat weight tertinggi,")
    print("pixel di tepi mendapat weight terendah.")


def explain_additive_blend():
    """Menjelaskan additive blending."""
    print_header("TAHAP 4: ADDITIVE BLENDING")
    
    print("Additive blending menggabungkan scene original dengan bloom.")
    print()
    print("Formula:")
    print()
    print("  finalColor = (originalColor × originalStrength) +")
    print("               (bloomColor × blendStrength)")
    print()
    print("Dalam program:")
    print("  originalStrength = 2.0")
    print("  blendStrength = 1.0")
    print()
    print("Contoh perhitungan:")
    print()
    print("  Pixel di area terang:")
    print("  ─────────────────────────────────────────")
    print("  originalColor = (1.0, 0.8, 0.6)")
    print("  bloomColor    = (0.5, 0.4, 0.3)")
    print()
    print("  final = (1.0×2.0, 0.8×2.0, 0.6×2.0) + (0.5×1.0, 0.4×1.0, 0.3×1.0)")
    print("        = (2.0, 1.6, 1.2) + (0.5, 0.4, 0.3)")
    print("        = (2.5, 2.0, 1.5)  ← Extra bright dengan glow!")
    print()
    print("  Pixel di area gelap:")
    print("  ─────────────────────────────────────────")
    print("  originalColor = (0.2, 0.2, 0.2)")
    print("  bloomColor    = (0.0, 0.0, 0.0)  ← filtered out")
    print()
    print("  final = (0.2×2.0, 0.2×2.0, 0.2×2.0) + (0.0, 0.0, 0.0)")
    print("        = (0.4, 0.4, 0.4)")
    print("        = Sedikit lebih terang, tapi tidak glow")
    print()
    print("Hasil: Scene dengan bloom glow effect!")


def explain_parameters():
    """Menjelaskan parameter tuning."""
    print_header("PARAMETER TUNING GUIDE")
    
    print("Anda bisa menyesuaikan bloom effect dengan mengubah parameter:")
    print()
    print("1. BRIGHT FILTER THRESHOLD")
    print("   BrightFilterEffect(threshold)")
    print()
    print("   threshold  │  Effect")
    print("   ───────────┼────────────────────────────────")
    print("   1.0 - 2.0  │  Banyak area glow (luas)")
    print("   2.4 (def)  │  Balance yang baik")
    print("   3.0 - 5.0  │  Hanya area sangat terang glow")
    print()
    print("2. BLUR RADIUS")
    print("   HorizontalBlurEffect(blurRadius=...)")
    print("   VerticalBlurEffect(blurRadius=...)")
    print()
    print("   radius     │  Effect")
    print("   ───────────┼────────────────────────────────")
    print("   10 - 30    │  Glow tajam, subtle")
    print("   40 - 60    │  Glow balanced (default=50)")
    print("   70 - 100   │  Glow sangat luas, dreamy")
    print()
    print("3. BLEND STRENGTHS")
    print("   AdditiveBlendEffect(originalStrength=..., blendStrength=...)")
    print()
    print("   originalStrength │  Effect")
    print("   ─────────────────┼────────────────────")
    print("   < 1.0            │  Scene gelap")
    print("   1.0              │  Scene normal")
    print("   2.0 (default)    │  Scene lebih terang")
    print("   > 2.0            │  Scene sangat terang")
    print()
    print("   blendStrength    │  Effect")
    print("   ─────────────────┼────────────────────")
    print("   < 0.5            │  Bloom subtle")
    print("   1.0 (default)    │  Bloom balanced")
    print("   > 1.5            │  Bloom sangat kuat")


def main():
    """Main tutorial function."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "BLOOM EFFECT - TUTORIAL INTERAKTIF" + " " * 19 + "║")
    print("╚" + "═" * 68 + "╝")
    
    explain_bloom_concept()
    input("\n[Tekan Enter untuk lanjut...]")
    
    explain_post_processing()
    input("\n[Tekan Enter untuk lanjut...]")
    
    explain_bloom_pipeline()
    input("\n[Tekan Enter untuk lanjut...]")
    
    explain_bright_filter()
    input("\n[Tekan Enter untuk lanjut...]")
    
    explain_gaussian_blur()
    input("\n[Tekan Enter untuk lanjut...]")
    
    explain_additive_blend()
    input("\n[Tekan Enter untuk lanjut...]")
    
    explain_parameters()
    
    print_header("TUTORIAL SELESAI!")
    print("Sekarang Anda siap untuk:")
    print()
    print("1. Menjalankan demo:")
    print("   python 10_light-shadow-2.py")
    print()
    print("2. Membaca kode dengan komentar:")
    print("   files/10_light-shadow-2_commented.py")
    print()
    print("3. Membaca dokumentasi lengkap:")
    print("   LIGHT_SHADOW_2_README.md")
    print()
    print("4. Eksperimen dengan parameter!")
    print()
    print_separator()
    print("Selamat belajar! ✨")
    print_separator()
    print()


if __name__ == "__main__":
    main()
