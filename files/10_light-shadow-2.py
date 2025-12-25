"""
Bloom Effect Demo - Post-Processing untuk Light Glow
====================================================
Program ini mendemonstrasikan efek Bloom menggunakan post-processing.
Bloom membuat area terang memancarkan cahaya lembut yang realistis.

Pipeline: Scene → Bright Filter → H-Blur → V-Blur → Blend → Screen
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
    Kelas demo untuk Bloom Effect.
    Menggunakan multi-pass rendering dengan post-processing.
    """
    def initialize(self):
        """Inisialisasi scene, camera, objects, dan post-processing."""
        print("Initializing Bloom Effect Demo...")
        
        # Renderer dengan background hitam untuk kontras
        self.renderer = Renderer(clearColor=[0, 0, 0])
        
        # Setup scene dan camera
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800/600)
        self.camera.setPosition([0, 0, 4])
        
        # Movement rig untuk kontrol kamera (W/A/S/D, Q/E, Mouse)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.setPosition([0, 1, 4])
        
        # SKY - Sphere besar (radius=50) sebagai skybox
        # Camera berada di dalam sphere, melihat texture dari dalam
        skyGeometry = SphereGeometry(radius=50)
        earthTexture = Texture("images/sky-earth.png")
        skyMaterial = TextureMaterial(earthTexture)
        sky = Mesh(skyGeometry, skyMaterial)
        self.scene.add(sky)
        
        # GRASS - Rectangle sebagai tanah dengan texture berulang
        # repeatUV=[50,50] untuk detail texture
        grassGeometry = RectangleGeometry(width=100, height=100)
        grassTexture = Texture("images/grass.png")
        grassMaterial = TextureMaterial(grassTexture, {"repeatUV": [50, 50]})
        grass = Mesh(grassGeometry, grassMaterial)
        grass.rotateX(-3.14 * 0.5)  # Rotasi 90° untuk horizontal
        self.scene.add(grass)

        # SPHERE - Objek utama yang akan mendapat bloom effect
        sphereGeometry = SphereGeometry()
        sphereTexture = Texture("images/grid.png")
        sphereMaterial = TextureMaterial(sphereTexture)
        self.sphere = Mesh(sphereGeometry, sphereMaterial)
        self.sphere.setPosition([0, 1, 0])  # 1 unit di atas tanah
        self.scene.add(self.sphere)

        # POST-PROCESSOR - Multi-pass rendering dengan effects
        # Scene di-render ke texture, lalu di-process dengan effects
        self.postprocessor = Postprocessor(self.renderer, self.scene, self.camera)
        
        # ===================================================================
        # POST-PROCESSING EFFECTS - Bloom Pipeline
        # ===================================================================
        # Effects dijalankan secara sequential (berurutan)
        # Output effect sebelumnya → input effect berikutnya
        
        # Alternative: Uncomment untuk mencoba effect tunggal
        # self.postprocessor.addEffect(BrightFilterEffect())      # Hanya bright areas
        # self.postprocessor.addEffect(VerticalBlurEffect())      # Blur vertical saja
        # self.postprocessor.addEffect(HorizontalBlurEffect())    # Blur horizontal saja

        # BLOOM EFFECT CHAIN:
        
        # 1. BRIGHT FILTER - Extract bright areas (threshold=2.4)
        #    Hanya pixel dengan brightness > 2.4 yang dilewatkan
        #    Hasil: Texture dengan hanya area terang
        self.postprocessor.addEffect(BrightFilterEffect(2.4))
        
        # 2. HORIZONTAL BLUR - Gaussian blur horizontal (radius=50 pixels)
        #    Menyebarkan cahaya ke kiri-kanan
        #    Hasil: Bright areas menyebar horizontal
        self.postprocessor.addEffect(
            HorizontalBlurEffect(textureSize=[800, 600], blurRadius=50)
        )
        
        # 3. VERTICAL BLUR - Gaussian blur vertical (radius=50 pixels)
        #    Menyebarkan cahaya ke atas-bawah
        #    2-pass blur (H+V) lebih efisien dari 1-pass 2D blur
        #    Hasil: Bright areas menyebar ke semua arah (glow 2D)
        self.postprocessor.addEffect(
            VerticalBlurEffect(textureSize=[800, 600], blurRadius=50)
        )
        
        # 4. ADDITIVE BLEND - Gabung scene original + bloom
        #    Formula: final = (original × 2) + (bloom × 1)
        #    renderTargetList[0] = scene original sebelum effects
        #    Hasil: Scene dengan bloom glow effect
        mainScene = self.postprocessor.renderTargetList[0].texture
        self.postprocessor.addEffect(
            AdditiveBlendEffect(mainScene, originalStrength=2, blendStrength=1)
        )
        
        print("\nBloom Effect Pipeline:")
        print("Scene → Bright Filter → H-Blur → V-Blur → Blend → Screen")
        print("\nControls: W/A/S/D (move), Q/E (up/down), Mouse (look)")


    
    def update(self):
        """
        Update loop - dipanggil setiap frame.
        1. Update camera rig (process input)
        2. Render dengan post-processor (multi-pass)
        """
        # Update movement rig dengan input dan deltaTime
        self.rig.update(self.input, self.deltaTime)
        
        # Render scene dengan post-processing effects
        # Pipeline: Scene → Effect1 → Effect2 → ... → Screen
        self.postprocessor.render()


# ===================================================================
# PROGRAM ENTRY POINT
# ===================================================================
# Instantiate dan jalankan program dengan resolusi 800x600
Test(screenSize=[800, 600]).run()
