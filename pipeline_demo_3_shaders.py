"""
Demo 3: Visualisasi Pipeline - Vertex vs Fragment Shader
=========================================================
Demo ini menunjukkan perbedaan antara vertex shader dan fragment shader
dalam graphics pipeline dengan animasi dan efek visual.

Demonstrasi:
- Vertex shader: Transformasi geometri, animasi vertex
- Fragment shader: Perhitungan warna, lighting, texture
"""

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.sphereGeometry import SphereGeometry
from geometry.boxGeometry import BoxGeometry
from material.surfaceMaterial import SurfaceMaterial
from extras.axesHelper import AxesHelper
from extras.gridHelper import GridHelper
from extras.movementRig import MovementRig
from light.ambientLight import AmbientLight
from light.directionalLight import DirectionalLight
from math import sqrt, sin


class ShaderPipelineDemo(Base):
    """
    Demo yang menunjukkan peran vertex shader dan fragment shader.
    """
    
    def initialize(self):
        print("\n" + "=" * 60)
        print("DEMO: VERTEX SHADER vs FRAGMENT SHADER")
        print("=" * 60)
        print()
        print("Demo ini menunjukkan perbedaan antara:")
        print()
        print("VERTEX SHADER (Kiri):")
        print("- Berjalan sekali per vertex")
        print("- Mentransformasi posisi vertex")
        print("- Animasi geometri (wave effect)")
        print()
        print("FRAGMENT SHADER (Kanan):")
        print("- Berjalan sekali per pixel")
        print("- Menghitung warna final")
        print("- Efek visual (gradient, lighting)")
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
        
        # Setup camera
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0, 2, 8])
        self.scene.add(self.rig)
        
        # Lighting
        ambient = AmbientLight(color=[0.3, 0.3, 0.3])
        self.scene.add(ambient)
        
        directional = DirectionalLight(color=[0.7, 0.7, 0.7], direction=[-1, -1, -2])
        self.scene.add(directional)
        
        # Grid helper
        grid = GridHelper(size=20, gridColor=[0.5, 0.5, 0.5])
        grid.rotateX(-3.14159 / 2)
        self.scene.add(grid)
        
        # Axes helper
        axes = AxesHelper(axisLength=2)
        self.scene.add(axes)
        
        # Sphere kiri - demonstrasi vertex shader
        # (animasi wave pada vertices)
        geometry_left = SphereGeometry(radius=1, radiusSegments=32, heightSements=16)
        material_left = SurfaceMaterial(
            properties={"useVertexColors": False, "baseColor": [0.2, 0.6, 1.0]}
        )
        self.sphere_left = Mesh(geometry_left, material_left)
        self.sphere_left.setPosition([-3, 1.5, 0])
        self.scene.add(self.sphere_left)
        
        # Simpan posisi vertex original untuk animasi
        position_attribute = geometry_left.attributes["vertexPosition"]
        self.original_positions = position_attribute.data.copy()
        
        # Sphere kanan - demonstrasi fragment shader
        # (warna dan lighting)
        geometry_right = SphereGeometry(radius=1, radiusSegments=32, heightSements=16)
        material_right = SurfaceMaterial(
            properties={"useVertexColors": False, "baseColor": [1.0, 0.6, 0.2]}
        )
        self.sphere_right = Mesh(geometry_right, material_right)
        self.sphere_right.setPosition([3, 1.5, 0])
        self.scene.add(self.sphere_right)
        
        self.time = 0
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
        
        self.time += self.deltaTime
        
        # Animasi sphere kiri - simulasi vertex shader animation
        # Setiap vertex bergerak berdasarkan posisinya (wave effect)
        position_attribute = self.sphere_left.geometry.attributes["vertexPosition"]
        positions = self.original_positions.copy()
        
        for i in range(len(positions)):
            x, y, z = positions[i]
            # Hitung jarak dari center
            distance = sqrt(x*x + y*y + z*z)
            # Tambahkan wave displacement
            wave = sin(distance * 5 + self.time * 3) * 0.1
            # Normalize dan apply wave
            if distance > 0:
                positions[i] = [x * (1 + wave), y * (1 + wave), z * (1 + wave)]
        
        position_attribute.data = positions
        position_attribute.uploadData()
        
        # Rotasi kedua sphere
        self.sphere_left.rotateY(0.5 * self.deltaTime)
        self.sphere_right.rotateY(0.5 * self.deltaTime)
        
        # Animasi warna sphere kanan - simulasi fragment shader effect
        # (mengubah warna material untuk simulasi)
        hue = (self.time * 0.3) % 1.0
        if hue < 0.33:
            color = [1.0, hue * 3, 0.2]
        elif hue < 0.66:
            color = [(1.0 - (hue - 0.33) * 3), 1.0, 0.2]
        else:
            color = [0.2, (1.0 - (hue - 0.66) * 3), (hue - 0.66) * 3 + 0.6]
        
        self.sphere_right.material.uniforms["baseColor"].data = color
        
        # Render
        self.renderer.render(self.scene, self.camera)


# Instantiate and run
if __name__ == "__main__":
    print("\nMemulai demo shader pipeline...")
    demo = ShaderPipelineDemo(screenSize=[800, 600])
    demo.run()
    
    # Auto-launch demo 4
    print("\n" + "=" * 70)
    print("Demo 3 selesai! Meluncurkan Demo 4 (Rasterization)...")
    print("=" * 70)
    import subprocess
    subprocess.Popen([sys.executable, "pipeline_demo_4_rasterization.py"])
