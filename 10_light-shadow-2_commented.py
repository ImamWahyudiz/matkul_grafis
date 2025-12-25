"""
10_light-shadow-2.py - Bloom Effect dengan Post-Processing
===========================================================

Program ini mendemonstrasikan penggunaan Post-Processing untuk membuat
efek Bloom (light glow). Bloom effect membuat area terang dalam scene
memancarkan cahaya yang lembut, menciptakan efek visual yang lebih
dramatis dan realistis.

Teknik yang digunakan:
1. Render to Texture (off-screen rendering)
2. Bright Filter (extract bright areas)
3. Gaussian Blur 2-pass (horizontal + vertical)
4. Additive Blending (combine with original)

Pipeline:
Scene → Bright Filter → H-Blur → V-Blur → Blend → Screen

Kontrol:
- W/A/S/D: Gerak kamera
- Q/E: Naik/turun
- Mouse: Rotasi kamera
"""

from core.base import Base
from core.camera import Camera
from core.mesh import Mesh
from core.renderer import Renderer
from core.scene import Scene
from core.texture import Texture
from effects.additiveBlendEffect import AdditiveBlendEffect
from effects.brightFilterEffect import BrightFilterEffect
from effects.colorReduceEffect import ColorReducerEffect
from effects.horizontalBlurEffect import HorizontalBlurEffect
from effects.invertEffect import InvertEffect
from effects.pixelateEffect import PixelateEffect
from effects.tintEffect import TintEffect
from effects.verticalBlurEffect import VerticalBlurEffect
from effects.vignetteEffect import VignetteEffect
from extras.movementRig import MovementRig
from extras.postprocessor import Postprocessor
from geometry.boxGeometry import BoxGeometry
from geometry.rectangleGeometry import RectangleGeometry
from geometry.sphereGeometry import SphereGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial


class Test(Base):
    """
    Kelas utama untuk demo Bloom Effect.
    
    Bloom Effect Pipeline:
    1. Render scene ke texture (off-screen)
    2. Extract bright areas (threshold filtering)
    3. Blur horizontal (spread light left-right)
    4. Blur vertical (spread light up-down)
    5. Blend with original scene (additive)
    """
    
    def initialize(self):
        """
        Inisialisasi scene, camera, objects, dan post-processing effects.
        """
        print("Initializing Bloom Effect Demo...")
        
        # ===================================================================
        # RENDERER SETUP
        # ===================================================================
        # Renderer dengan background hitam untuk kontras yang baik
        self.renderer = Renderer(clearColor=[0, 0, 0])
        
        # ===================================================================
        # SCENE & CAMERA SETUP
        # ===================================================================
        # Scene container untuk semua objek 3D
        self.scene = Scene()
        
        # Camera dengan aspect ratio 4:3 (800x600)
        self.camera = Camera(aspectRatio=800/600)
        self.camera.setPosition([0, 0, 4])
        
        # ===================================================================
        # MOVEMENT RIG (Camera Control)
        # ===================================================================
        # MovementRig memungkinkan kontrol kamera dengan keyboard & mouse
        # - W/A/S/D: Gerak kamera
        # - Q/E: Naik/turun
        # - Mouse: Look around
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.setPosition([0, 1, 4])  # Posisi awal kamera
        
        # ===================================================================
        # SKY (Langit) - Skybox menggunakan Sphere
        # ===================================================================
        # Sphere besar (radius=50) yang membungkus seluruh scene
        # Camera berada di dalam sphere, melihat texture dari dalam
        skyGeometry = SphereGeometry(radius=50)
        earthTexture = Texture("images/sky-earth.png")
        skyMaterial = TextureMaterial(earthTexture)
        sky = Mesh(skyGeometry, skyMaterial)
        self.scene.add(sky)
        
        # ===================================================================
        # GRASS (Rumput) - Ground Plane
        # ===================================================================
        # Rectangle besar sebagai tanah
        grassGeometry = RectangleGeometry(width=100, height=100)
        grassTexture = Texture("images/grass.png")
        
        # repeatUV=[50,50] membuat texture diulang 50x untuk detail
        grassMaterial = TextureMaterial(grassTexture, {"repeatUV": [50, 50]})
        grass = Mesh(grassGeometry, grassMaterial)
        
        # Rotasi -90° (atau -π/2) untuk membuat rectangle horizontal
        # Default rectangle menghadap ke kamera (vertical)
        grass.rotateX(-3.14 * 0.5)
        self.scene.add(grass)
        
        # ===================================================================
        # SPHERE (Objek Utama) - Demo Object
        # ===================================================================
        # Sphere dengan texture grid yang akan mendapat bloom effect
        sphereGeometry = SphereGeometry()
        sphereTexture = Texture("images/grid.png")
        sphereMaterial = TextureMaterial(sphereTexture)
        self.sphere = Mesh(sphereGeometry, sphereMaterial)
        self.sphere.setPosition([0, 1, 0])  # Posisi 1 unit di atas tanah
        self.scene.add(self.sphere)
        
        # ===================================================================
        # POST-PROCESSOR SETUP
        # ===================================================================
        # Postprocessor menangani rendering multi-pass dan effects
        # Scene di-render ke texture, lalu di-process dengan effects
        self.postprocessor = Postprocessor(self.renderer, self.scene, self.camera)
        
        # ===================================================================
        # POST-PROCESSING EFFECTS CHAIN
        # ===================================================================
        # Effects dijalankan secara sequential (berurutan)
        # Output dari effect sebelumnya menjadi input effect berikutnya
        
        # -------------------------------------------------------------------
        # EFFECT 1: BRIGHT FILTER
        # -------------------------------------------------------------------
        # Mengekstrak hanya area yang terang (bright areas)
        # Parameter: threshold = 2.4
        # - Pixel dengan brightness > 2.4 akan dilewatkan
        # - Pixel dengan brightness < 2.4 menjadi hitam
        # 
        # Formula: brightness = dot(color.rgb, vec3(0.2126, 0.7152, 0.0722))
        # Ini adalah formula luminance berdasarkan persepsi mata manusia
        #
        # Hasil: Texture yang hanya berisi area terang
        self.postprocessor.addEffect(BrightFilterEffect(2.4))
        
        # -------------------------------------------------------------------
        # EFFECT 2: HORIZONTAL BLUR
        # -------------------------------------------------------------------
        # Mengaplikasikan Gaussian blur secara horizontal (kiri-kanan)
        # 
        # Parameter:
        # - textureSize=[800,600]: Resolusi untuk menghitung UV step
        # - blurRadius=50: Jarak blur dalam pixels
        # 
        # Cara kerja:
        # Untuk setiap pixel, sample beberapa pixel di kiri dan kanan,
        # lalu weighted average berdasarkan Gaussian distribution
        # 
        # Gaussian weight: w(x) = exp(-(x²) / (2σ²))
        # σ (sigma) menentukan spread dari blur
        # 
        # Hasil: Bright areas menyebar ke horizontal
        self.postprocessor.addEffect(
            HorizontalBlurEffect(
                textureSize=[800, 600],
                blurRadius=30
            )
        )
        
        # -------------------------------------------------------------------
        # EFFECT 3: VERTICAL BLUR
        # -------------------------------------------------------------------
        # Mengaplikasikan Gaussian blur secara vertical (atas-bawah)
        # 
        # Parameter sama dengan horizontal blur
        # 
        # Mengapa 2-pass (H+V) daripada 1-pass 2D blur?
        # - 1-pass 2D blur: Sample (2r+1)² pixels → O(n²) → LAMBAT
        # - 2-pass blur: Sample 2×(2r+1) pixels → O(2n) → CEPAT
        # - Hasil visual hampir identik!
        # 
        # Contoh dengan radius=3:
        # - 1-pass: 7×7 = 49 samples per pixel
        # - 2-pass: 7+7 = 14 samples per pixel
        # 
        # Hasil: Bright areas menyebar ke semua arah (2D glow)
        self.postprocessor.addEffect(
            VerticalBlurEffect(
                textureSize=[800, 600],
                blurRadius=30
            )
        )
        
        # -------------------------------------------------------------------
        # EFFECT 4: ADDITIVE BLEND
        # -------------------------------------------------------------------
        # Menggabungkan scene original dengan blurred bright areas
        # 
        # Parameter:
        # - mainScene: Texture scene original (sebelum effects)
        # - originalStrength=2: Multiplier untuk scene (2x lebih terang)
        # - blendStrength=1: Multiplier untuk bloom
        # 
        # Formula:
        # finalColor = (originalColor × originalStrength) + 
        #              (bloomColor × blendStrength)
        # 
        # Additive blending berarti warna dijumlahkan, bukan di-replace
        # Ini membuat area terang "glow" dengan cahaya tambahan
        # 
        # renderTargetList[0] adalah render target pertama,
        # yaitu hasil render scene sebelum effects
        mainScene = self.postprocessor.renderTargetList[0].texture
        self.postprocessor.addEffect(
            AdditiveBlendEffect(
                mainScene,
                originalStrength=2,
                blendStrength=1
            )
        )
        
        # ===================================================================
        # ALTERNATIVE EFFECTS (Commented)
        # ===================================================================
        # Uncomment untuk mencoba effect lain:
        
        # Effect tunggal (tanpa bloom):
        # self.postprocessor.addEffect(BrightFilterEffect())  # Hanya bright
        # self.postprocessor.addEffect(VerticalBlurEffect())   # Blur vertical saja
        # self.postprocessor.addEffect(HorizontalBlurEffect()) # Blur horizontal saja
        
        # Effect tambahan untuk enhancement:
        # self.postprocessor.addEffect(VignetteEffect(intensity=0.5))
        # self.postprocessor.addEffect(TintEffect(tintColor=[1.0, 0.9, 0.8]))
        # self.postprocessor.addEffect(PixelateEffect(pixelSize=4))
        
        print("Bloom Effect initialized successfully!")
        print("\nPost-Processing Pipeline:")
        print("1. Render Scene → Texture")
        print("2. Bright Filter (threshold=2.4)")
        print("3. Horizontal Blur (radius=50)")
        print("4. Vertical Blur (radius=50)")
        print("5. Additive Blend (original + bloom)")
        print("\nControls:")
        print("- W/A/S/D: Move camera")
        print("- Q/E: Up/Down")
        print("- Mouse: Look around")
    
    def update(self):
        """
        Update loop yang dipanggil setiap frame.
        
        Urutan eksekusi:
        1. Update camera rig (process input)
        2. Render dengan post-processor (multi-pass rendering)
        """
        # Update movement rig dengan input dan deltaTime
        # deltaTime: waktu sejak frame terakhir (untuk movement yang smooth)
        self.rig.update(self.input, self.deltaTime)
        
        # Render scene dengan post-processing effects
        # Ini akan menjalankan seluruh pipeline:
        # Scene → RenderTarget → Effect1 → Effect2 → ... → Screen
        self.postprocessor.render()


# ===================================================================
# PROGRAM ENTRY POINT
# ===================================================================
# Instantiate class dan jalankan program
# screenSize=[800, 600]: Resolusi window 800x600 pixels
Test(screenSize=[800, 600]).run()
