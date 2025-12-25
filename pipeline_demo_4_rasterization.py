"""
Demo 4: Visualisasi Pipeline - Rasterization dan Depth Buffer
==============================================================
Demo ini menunjukkan tahapan rasterization dan depth testing
dalam graphics pipeline.

Demonstrasi:
- Primitive assembly (points, lines, triangles)
- Rasterization (konversi geometri ke fragments)
- Depth testing (Z-buffer)
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
from geometry.sphereGeometry import SphereGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.lineMaterial import LineMaterial
from extras.axesHelper import AxesHelper
from extras.gridHelper import GridHelper
from extras.movementRig import MovementRig
from OpenGL.GL import *
from math import sin


class RasterizationDemo(Base):
    """
    Demo rasterization dan depth testing.
    """
    
    def initialize(self):
        print("\n" + "=" * 60)
        print("DEMO: RASTERIZATION DAN DEPTH TESTING")
        print("=" * 60)
        print()
        print("Demo ini menunjukkan:")
        print()
        print("1. PRIMITIVE TYPES:")
        print("   - Points (titik)")
        print("   - Lines (garis)")
        print("   - Triangles (filled)")
        print()
        print("2. RASTERIZATION:")
        print("   - Konversi primitif ke fragments (pixels)")
        print()
        print("3. DEPTH TESTING:")
        print("   - Z-buffer untuk menentukan objek mana yang di depan")
        print("   - Objek overlap untuk mendemonstrasikan depth test")
        print()
        print("Kontrol:")
        print("- W/A/S/D: Gerak kamera (depan/kiri/belakang/kanan)")
        print("- R/F: Naik/turun (kontrol tinggi/Y-axis)")
        print("- Q/E: Rotasi kiri/kanan (keyboard)")
        print("- Mouse: Klik kiri + drag untuk rotasi kamera")
        print("- 1/2/3: Toggle mode render (filled/wireframe/points)")
        print("=" * 60)
        print()
        
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800/600)
        
        # Setup camera
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0, 2, 6])
        self.scene.add(self.rig)
        
        # Grid
        grid = GridHelper(size=20, gridColor=[0.5, 0.5, 0.5])
        grid.rotateX(-3.14159 / 2)
        self.scene.add(grid)
        
        # Axes
        axes = AxesHelper(axisLength=2)
        self.scene.add(axes)
        
        # Objek 1: Box dengan triangles (filled)
        geometry1 = BoxGeometry()
        material1 = SurfaceMaterial(
            properties={
                "useVertexColors": True,
                "wireframe": False
            }
        )
        self.box1 = Mesh(geometry1, material1)
        self.box1.setPosition([-2, 1, 0])
        self.scene.add(self.box1)
        
        # Objek 2: Box dengan wireframe (lines)
        geometry2 = BoxGeometry()
        material2 = SurfaceMaterial(
            properties={
                "useVertexColors": True,
                "wireframe": True
            }
        )
        self.box2 = Mesh(geometry2, material2)
        self.box2.setPosition([0, 1, 0])
        self.scene.add(self.box2)
        
        # Objek 3: Sphere untuk depth testing
        geometry3 = SphereGeometry(radius=0.7)
        material3 = SurfaceMaterial(
            properties={
                "useVertexColors": False,
                "baseColor": [0.2, 0.8, 0.2],
                "wireframe": False
            }
        )
        self.sphere = Mesh(geometry3, material3)
        self.sphere.setPosition([2, 1, 0])
        self.scene.add(self.sphere)
        
        # Objek 4: Box yang overlap dengan sphere (untuk depth test demo)
        geometry4 = BoxGeometry(width=0.8, height=0.8, depth=0.8)
        material4 = SurfaceMaterial(
            properties={
                "useVertexColors": False,
                "baseColor": [0.8, 0.2, 0.2],
                "wireframe": False
            }
        )
        self.box3 = Mesh(geometry4, material4)
        self.box3.setPosition([2, 1, 0.5])
        self.scene.add(self.box3)
        
        self.time = 0
        self.render_mode = 0  # 0: filled, 1: wireframe, 2: points
        self.frame_count = 0  # Counter untuk print posisi kamera
    
    def update(self):
        # Update rig
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
        
        # Check for mode toggle
        if self.input.isKeyPressed("1"):
            self.render_mode = 0
            print("Mode: FILLED (Triangles)")
            self._update_render_mode()
        elif self.input.isKeyPressed("2"):
            self.render_mode = 1
            print("Mode: WIREFRAME (Lines)")
            self._update_render_mode()
        elif self.input.isKeyPressed("3"):
            self.render_mode = 2
            print("Mode: POINTS (Vertices)")
            self._update_render_mode()
        
        self.time += self.deltaTime
        
        # Animasi rotasi
        self.box1.rotateY(0.7 * self.deltaTime)
        self.box1.rotateX(0.4 * self.deltaTime)
        
        self.box2.rotateY(-0.5 * self.deltaTime)
        self.box2.rotateZ(0.3 * self.deltaTime)
        
        # Animasi sphere dan box overlap (depth test demo)
        self.sphere.rotateY(0.8 * self.deltaTime)
        self.box3.rotateY(-0.6 * self.deltaTime)
        self.box3.rotateX(0.4 * self.deltaTime)
        
        # Animate overlap
        offset = sin(self.time) * 0.5
        self.box3.setPosition([2, 1, 0.5 + offset])
        
        # Render
        self.renderer.render(self.scene, self.camera)
    
    def _update_render_mode(self):
        """Update render mode untuk semua objek"""
        if self.render_mode == 0:
            # Filled mode
            self.box1.material.settings["wireframe"] = False
            self.box2.material.settings["wireframe"] = False
            self.sphere.material.settings["wireframe"] = False
            self.box3.material.settings["wireframe"] = False
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glDisable(GL_PROGRAM_POINT_SIZE)
        elif self.render_mode == 1:
            # Wireframe mode
            self.box1.material.settings["wireframe"] = True
            self.box2.material.settings["wireframe"] = True
            self.sphere.material.settings["wireframe"] = True
            self.box3.material.settings["wireframe"] = True
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glDisable(GL_PROGRAM_POINT_SIZE)
        elif self.render_mode == 2:
            # Points mode
            glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)
            glEnable(GL_PROGRAM_POINT_SIZE)
            glPointSize(5.0)


# Instantiate and run
if __name__ == "__main__":
    print("\nMemulai demo rasterization...")
    demo = RasterizationDemo(screenSize=[800, 600])
    demo.run()
    
    # Demo terakhir
    print("\n" + "=" * 70)
    print("SEMUA DEMO SELESAI!")
    print("=" * 70)
    print("\nAnda telah mempelajari:")
    print("  ✓ Demo 0: Vertex dan Primitive Assembly (Step-by-Step)")
    print("  ✓ Demo 1: Konsep Graphics Pipeline")
    print("  ✓ Demo 2: MVP Transformation")
    print("  ✓ Demo 3: Vertex & Fragment Shaders")
    print("  ✓ Demo 4: Rasterization & Depth Testing")
    print("\nTerima kasih telah menggunakan tutorial Graphics Pipeline!")
    print("=" * 70)
