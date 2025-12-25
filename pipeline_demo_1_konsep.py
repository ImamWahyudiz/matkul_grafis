"""
Demo 1: Penjelasan Konsep Graphics Pipeline
============================================
File ini mendemonstrasikan penjelasan konsep graphics pipeline
secara interaktif menggunakan modul pipeline.
"""

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from core.pipeline import PipelineVisualizer, ShaderPipelineExplainer


def main():
    """
    Menjalankan demo penjelasan graphics pipeline.
    """
    print("\n")
    print("╔" + "═" * 70 + "╗")
    print("║" + " " * 15 + "DEMO GRAPHICS PIPELINE - PENJELASAN KONSEP" + " " * 13 + "║")
    print("╚" + "═" * 70 + "╝")
    print()
    print("Demo ini akan menjelaskan setiap tahapan dalam graphics pipeline")
    print("dari vertex data hingga pixel di layar.")
    print()
    
    choice = input("Pilih demo:\n1. Pipeline Lengkap\n2. Shader Pipeline\n\nPilihan (1/2): ")
    
    if choice == "1":
        # Demo pipeline lengkap
        PipelineVisualizer.explain_full_pipeline()
    elif choice == "2":
        # Demo shader pipeline
        ShaderPipelineExplainer.explain_shader_pipeline()
    else:
        print("Pilihan tidak valid. Menjalankan pipeline lengkap...")
        PipelineVisualizer.explain_full_pipeline()
    
    print("\n")
    print("=" * 72)
    print("Demo konsep selesai!")
    print("=" * 72)
    
    # Auto-launch demo 2
    import subprocess
    import time
    print("\nMeluncurkan Demo 2 (Transform & MVP Matrix) dalam 2 detik...")
    time.sleep(2)
    subprocess.Popen([sys.executable, "pipeline_demo_2_transform.py"])


if __name__ == "__main__":
    main()
