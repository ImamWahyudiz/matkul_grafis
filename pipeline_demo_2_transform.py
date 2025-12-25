"""
Demo 2: Visualisasi Graphics Pipeline - Transformasi Vertex
===========================================================
Demo ini menunjukkan tahapan transformasi vertex dalam graphics pipeline
dengan visualisasi 3D interaktif.

Tahapan yang didemonstrasikan:
1. Object Space (local coordinates)
2. World Space (setelah model matrix)
3. View Space (setelah view matrix)
4. Clip Space (setelah projection matrix)
"""

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.boxGeometry import BoxGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.lineMaterial import LineMaterial
from extras.axesHelper import AxesHelper
from extras.gridHelper import GridHelper
from extras.movementRig import MovementRig
from core.matrix import Matrix
from math import sin


class PipelineTransformDemo(Base):
    """
    Demo transformasi vertex dalam graphics pipeline.
    """
    
    def initialize(self):
        print("\n" + "=" * 60)
        print("DEMO: TRANSFORMASI VERTEX DALAM GRAPHICS PIPELINE")
        print("=" * 60)
        print()
        print("Demo ini menunjukkan bagaimana vertex ditransformasi")
        print("melalui berbagai coordinate spaces:")
        print()
        print("1. OBJECT SPACE - koordinat lokal objek")
        print("2. WORLD SPACE - koordinat dalam dunia 3D")
        print("3. VIEW SPACE - koordinat relatif terhadap kamera")
        print("4. CLIP SPACE - koordinat setelah proyeksi")
        print()
        print("Kontrol:")
        print("- W/A/S/D: Gerak kamera (depan/kiri/belakang/kanan)")
        print("- R/F: Naik/turun (kontrol tinggi/Y-axis)")
        print("- Q/E: Rotasi kiri/kanan (keyboard)")
        print("- Mouse: Klik kiri + drag untuk rotasi kamera")
        print("=" * 60)
        print()
        
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800/600)
        
        # Setup camera rig untuk kontrol
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0, 1, 5])
        self.scene.add(self.rig)
        
        # Tambahkan grid dan axes helper
        grid = GridHelper(
            size=20,
            gridColor=[0.5, 0.5, 0.5],
            centerColor=[1, 1, 1]
        )
        grid.rotateX(-3.14159 / 2)
        self.scene.add(grid)
        
        axes = AxesHelper(axisLength=2)
        self.scene.add(axes)
        
        # Objek 1: Kubus di object space (lokal)
        geometry1 = BoxGeometry(width=1, height=1, depth=1)
        material1 = SurfaceMaterial(
            properties={"useVertexColors": True, "wireframe": False}
        )
        self.cube1 = Mesh(geometry1, material1)
        self.cube1.setPosition([-3, 1, 0])
        self.scene.add(self.cube1)
        
        # Objek 2: Kubus di world space (dengan transformasi)
        geometry2 = BoxGeometry(width=1, height=1, depth=1)
        material2 = SurfaceMaterial(
            properties={"useVertexColors": True, "wireframe": False}
        )
        self.cube2 = Mesh(geometry2, material2)
        self.cube2.setPosition([0, 1, 0])
        self.scene.add(self.cube2)
        
        # Objek 3: Kubus dengan rotasi dan skala
        geometry3 = BoxGeometry(width=1, height=1, depth=1)
        material3 = SurfaceMaterial(
            properties={"useVertexColors": True, "wireframe": False}
        )
        self.cube3 = Mesh(geometry3, material3)
        self.cube3.setPosition([3, 1, 0])
        self.scene.add(self.cube3)
        
        self.time = 0
        self.frame_count = 0  # Counter untuk print posisi kamera
    
    def update(self):
        # Update movement rig
        self.rig.update(self.input, self.deltaTime)
        
        # Print posisi kamera setiap 30 frame (sekitar 0.5 detik)
        self.frame_count += 1
        if self.frame_count % 30 == 0:
            cam_pos = self.rig.getPosition()
            # Dapatkan rotasi dari transform matrix
            import math
            # Yaw (rotasi horizontal Y-axis) dari rig
            rig_transform = self.rig.transform
            yaw = math.atan2(rig_transform[0, 2], rig_transform[2, 2]) * 180 / math.pi
            # Pitch (rotasi vertical X-axis) dari lookAttachment
            look_transform = self.rig.lookAttachment.transform
            pitch = math.asin(-look_transform[1, 2]) * 180 / math.pi
            
            print(f"Kamera → Pos: X={cam_pos[0]:6.2f} Y={cam_pos[1]:6.2f} Z={cam_pos[2]:6.2f} | Rot: Yaw={yaw:6.1f}° Pitch={pitch:6.1f}°")
        
        # Animasi transformasi
        self.time += self.deltaTime
        
        # Cube 1: Static (object space reference)
        
        # Cube 2: Rotasi (model transformation)
        self.cube2.rotateY(0.5 * self.deltaTime)
        self.cube2.rotateX(0.3 * self.deltaTime)
        
        # Cube 3: Rotasi dan scale (multiple transformations)
        self.cube3.rotateY(-0.7 * self.deltaTime)
        scale_factor = 1.0 + 0.3 * sin(self.time * 2)
        self.cube3.scale(scale_factor)
        
        # Render scene
        self.renderer.render(self.scene, self.camera)


# Instantiate and run the program
if __name__ == "__main__":
    print("\nMemulai demo transformasi pipeline...")
    demo = PipelineTransformDemo(screenSize=[800, 600])
    demo.run()
    
    # Auto-launch demo 3
    print("\n" + "=" * 70)
    print("Demo 2 selesai! Meluncurkan Demo 3 (Shaders)...")
    print("=" * 70)
    import subprocess
    subprocess.Popen([sys.executable, "pipeline_demo_3_shaders.py"])
