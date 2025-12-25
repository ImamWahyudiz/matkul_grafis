"""
Demo 0: Graphics Pipeline - Visualisasi Dasar Vertex & Primitif
================================================================
Demo ini menunjukkan tahapan paling dasar dalam graphics pipeline:
1. Vertex Data (titik-titik individual)
2. Primitive Assembly (menghubungkan vertex menjadi primitif)
3. Tiga jenis primitif: POINTS, LINES, TRIANGLES

Tahapan yang divisualisasikan:
- Vertex sebagai titik individual
- Lines yang menghubungkan 2 vertex
- Triangles yang menghubungkan 3 vertex

Kontrol:
- W/A/S/D: Gerak kamera (depan/kiri/belakang/kanan)
- R/F: Naik/turun (kontrol tinggi/Y-axis)
- Q/E: Rotasi kiri/kanan (keyboard)
- Mouse: Klik kiri + drag untuk rotasi kamera
- 1: Tampilkan POINTS (vertex saja)
- 2: Tampilkan LINES (garis)
- 3: Tampilkan TRIANGLES (segitiga filled)
- 4: Tampilkan SEMUA (points + lines + triangles)
"""

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.geometry import Geometry
from material.pointMaterial import PointMaterial
from material.lineMaterial import LineMaterial
from material.surfaceMaterial import SurfaceMaterial
from extras.axesHelper import AxesHelper
from extras.gridHelper import GridHelper
from extras.movementRig import MovementRig
from OpenGL.GL import *
import math


class BasicPipelineDemo(Base):
    """
    Demo yang menunjukkan vertex, lines, dan triangles secara terpisah.
    """
    
    def initialize(self):
        print("\n" + "=" * 70)
        print("DEMO: GRAPHICS PIPELINE - VISUALISASI DASAR")
        print("=" * 70)
        print()
        print("Demo ini menunjukkan tahapan paling dasar graphics pipeline:")
        print()
        print("1. VERTEX DATA - Titik-titik dalam 3D space")
        print("   • Setiap vertex memiliki posisi (x, y, z)")
        print("   • Vertex adalah input dasar untuk graphics pipeline")
        print()
        print("2. PRIMITIVE ASSEMBLY - Menghubungkan vertex")
        print("   • POINTS: Render setiap vertex sebagai titik")
        print("   • LINES: Setiap 2 vertex membentuk garis")
        print("   • TRIANGLES: Setiap 3 vertex membentuk segitiga")
        print()
        print("3. RASTERIZATION - Konversi ke pixel")
        print("   • Primitif dikonversi menjadi fragments (pixels)")
        print()
        print("Kontrol:")
        print("- W/A/S/D: Gerak kamera (depan/kiri/belakang/kanan)")
        print("- R/F: Naik/turun (kontrol tinggi/Y-axis)")
        print("- Q/E: Rotasi kiri/kanan (keyboard)")
        print("- Mouse: Klik kiri + drag untuk rotasi kamera")
        print()
        print("Mode Visualisasi:")
        print("- 1: POINTS (vertex saja)")
        print("- 2: LINES (garis)")
        print("- 3: TRIANGLES (segitiga)")
        print("- 4: SEMUA (points + lines + triangles)")
        print("=" * 70)
        print()
        
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800/600)
        
        # Setup camera
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0, 2, 8])
        self.scene.add(self.rig)
        
        # Grid helper
        grid = GridHelper(size=20, gridColor=[0.5, 0.5, 0.5])
        grid.rotateX(-3.14159 / 2)
        self.scene.add(grid)
        
        # Axes helper
        axes = AxesHelper(axisLength=2)
        self.scene.add(axes)
        
        # ===================================================================
        # VERTEX DATA - Definisikan 6 vertex untuk membuat 2 segitiga
        # ===================================================================
        # Ini adalah tahap 1 dalam graphics pipeline: VERTEX SPECIFICATION
        
        # Triangle 1: vertices 0, 1, 2 (segitiga bawah)
        # Triangle 2: vertices 3, 4, 5 (segitiga atas)
        vertex_positions = [
            # Triangle 1 (bawah) - warna merah
            [-1.5,  0.5, 0],  # Vertex 0: kiri bawah
            [ 0.5,  0.5, 0],  # Vertex 1: kanan bawah
            [-0.5,  1.5, 0],  # Vertex 2: atas
            
            # Triangle 2 (atas) - warna biru
            [ 0.5,  0.5, 0],  # Vertex 3: kiri bawah
            [ 2.5,  0.5, 0],  # Vertex 4: kanan bawah
            [ 1.5,  1.5, 0],  # Vertex 5: atas
        ]
        
        vertex_colors = [
            # Triangle 1 - merah
            [1, 0, 0],  # Vertex 0: merah
            [1, 0.5, 0],  # Vertex 1: orange
            [1, 1, 0],  # Vertex 2: kuning
            
            # Triangle 2 - biru
            [0, 1, 0],  # Vertex 3: hijau
            [0, 0.5, 1],  # Vertex 4: cyan
            [0, 0, 1],  # Vertex 5: biru
        ]
        
        # ===================================================================
        # MESH 1: POINTS - Menampilkan vertex sebagai titik
        # ===================================================================
        # Primitive type: GL_POINTS
        # Setiap vertex di-render sebagai 1 titik
        geometry_points = Geometry()
        geometry_points.addAttribute("vec3", "vertexPosition", vertex_positions)
        geometry_points.addAttribute("vec3", "vertexColor", vertex_colors)
        geometry_points.countVertices()
        
        material_points = PointMaterial(properties={"baseColor": [1, 1, 1], "pointSize": 20})
        self.mesh_points = Mesh(geometry_points, material_points)
        self.mesh_points.setPosition([-4, 1, 0])
        self.scene.add(self.mesh_points)
        
        # ===================================================================
        # MESH 2: LINES - Menampilkan edge/garis antar vertex
        # ===================================================================
        # Primitive type: GL_LINES
        # Setiap 2 vertex membentuk 1 garis
        geometry_lines = Geometry()
        geometry_lines.addAttribute("vec3", "vertexPosition", vertex_positions)
        geometry_lines.addAttribute("vec3", "vertexColor", vertex_colors)
        geometry_lines.countVertices()
        
        material_lines = LineMaterial(properties={"baseColor": [1, 1, 1], "lineWidth": 3})
        self.mesh_lines = Mesh(geometry_lines, material_lines)
        self.mesh_lines.setPosition([0, 1, 0])
        self.scene.add(self.mesh_lines)
        
        # ===================================================================
        # MESH 3: TRIANGLES - Menampilkan segitiga filled
        # ===================================================================
        # Primitive type: GL_TRIANGLES
        # Setiap 3 vertex membentuk 1 segitiga
        geometry_triangles = Geometry()
        geometry_triangles.addAttribute("vec3", "vertexPosition", vertex_positions)
        geometry_triangles.addAttribute("vec3", "vertexColor", vertex_colors)
        geometry_triangles.countVertices()
        
        material_triangles = SurfaceMaterial(properties={"useVertexColors": True})
        self.mesh_triangles = Mesh(geometry_triangles, material_triangles)
        self.mesh_triangles.setPosition([4, 1, 0])
        self.scene.add(self.mesh_triangles)
        
        # Visualisasi mode (1=points, 2=lines, 3=triangles, 4=all)
        self.visualization_mode = 4  # Default: tampilkan semua
        
        self.time = 0
        self.frame_count = 0
        
        print("Demo dimulai dengan mode: SEMUA (points + lines + triangles)")
        print("Tekan 1/2/3/4 untuk mengubah mode visualisasi")
        print()
    
    def update(self):
        # Update rig
        self.rig.update(self.input, self.deltaTime)
        
        # Print posisi dan rotasi kamera setiap 30 frame
        self.frame_count += 1
        if self.frame_count % 30 == 0:
            cam_pos = self.rig.getPosition()
            # Dapatkan rotasi dari transform matrix
            import math
            rig_transform = self.rig.transform
            yaw = math.atan2(rig_transform[0, 2], rig_transform[2, 2]) * 180 / math.pi
            look_transform = self.rig.lookAttachment.transform
            pitch = math.asin(-look_transform[1, 2]) * 180 / math.pi
            
            print(f"Kamera → Pos: X={cam_pos[0]:6.2f} Y={cam_pos[1]:6.2f} Z={cam_pos[2]:6.2f} | Rot: Yaw={yaw:6.1f}° Pitch={pitch:6.1f}°")
        
        # Check for visualization mode change
        if self.input.isKeyPressed("1"):
            self.visualization_mode = 1
            print("\n>>> Mode: POINTS (vertex sebagai titik)")
            print("    Setiap vertex di-render sebagai 1 titik besar")
            print("    Ini menunjukkan INPUT dasar dari graphics pipeline\n")
        elif self.input.isKeyPressed("2"):
            self.visualization_mode = 2
            print("\n>>> Mode: LINES (garis antar vertex)")
            print("    Setiap 2 vertex dihubungkan menjadi garis")
            print("    Primitive: GL_LINES\n")
        elif self.input.isKeyPressed("3"):
            self.visualization_mode = 3
            print("\n>>> Mode: TRIANGLES (segitiga filled)")
            print("    Setiap 3 vertex membentuk segitiga")
            print("    Primitive: GL_TRIANGLES → di-rasterize menjadi pixels\n")
        elif self.input.isKeyPressed("4"):
            self.visualization_mode = 4
            print("\n>>> Mode: SEMUA (points + lines + triangles)")
            print("    Menampilkan semua tahapan sekaligus\n")
        
        # Update visibility berdasarkan mode
        self.mesh_points.visible = (self.visualization_mode == 1 or self.visualization_mode == 4)
        self.mesh_lines.visible = (self.visualization_mode == 2 or self.visualization_mode == 4)
        self.mesh_triangles.visible = (self.visualization_mode == 3 or self.visualization_mode == 4)
        
        # Animasi rotasi
        self.time += self.deltaTime
        rotation_speed = 0.3
        
        self.mesh_points.rotateY(rotation_speed * self.deltaTime)
        self.mesh_lines.rotateY(rotation_speed * self.deltaTime)
        self.mesh_triangles.rotateY(rotation_speed * self.deltaTime)
        
        # Render
        self.renderer.render(self.scene, self.camera)


# Instantiate and run
print("\nMemulai demo pipeline dasar...")
BasicPipelineDemo(screenSize=[800, 600]).run()
