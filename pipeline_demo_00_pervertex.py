"""
Demo 00: Graphics Pipeline - Step by Step Visualization
========================================================
Demo ini menunjukkan proses graphics pipeline STEP-BY-STEP dengan kontrol manual:
- Tekan N atau → untuk next step
- Mulai dari 1 vertex, tambah vertex, hubungkan, sampai jadi segitiga
- Setiap step dijelaskan dengan detail

Tahapan:
1. Vertex pertama (merah)
2. Vertex kedua (hijau)  
3. Vertex ketiga (biru)
4. Hubungkan vertex 0-1 (garis pertama)
5. Hubungkan vertex 1-2 (garis kedua)
6. Hubungkan vertex 2-0 (wireframe lengkap)
7. Fill triangle (rasterization)
8. Complete (animasi rotasi)
9. Lanjut ke Demo 1 (konsep pipeline)
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
from geometry.sphereGeometry import SphereGeometry
from material.pointMaterial import PointMaterial
from material.lineMaterial import LineMaterial
from material.surfaceMaterial import SurfaceMaterial
from extras.axesHelper import AxesHelper
from extras.gridHelper import GridHelper
from extras.movementRig import MovementRig
from math import sin, cos, pi


class PerVertexDemo(Base):
    """
    Demo yang menunjukkan setiap vertex secara individual
    dengan transisi animasi antar tahapan pipeline.
    """
    
    def initialize(self):
        print("\n" + "=" * 70)
        print("DEMO 00: GRAPHICS PIPELINE - STEP BY STEP")
        print("=" * 70)
        print()
        print("Demo ini menunjukkan proses pembentukan geometri")
        print("dari vertex individual sampai jadi segitiga lengkap.")
        print()
        print("Kontrol:")
        print("- N atau → : NEXT STEP (tahap berikutnya)")
        print("- B atau ← : BACK (kembali ke tahap sebelumnya)")
        print("- W/A/S/D  : Gerak kamera")
        print("- R/F      : Naik/turun")
        print("- Q/E      : Rotasi kiri/kanan")
        print("- Mouse    : Klik kiri + drag untuk rotasi")
        print()
        print("=" * 70)
        print("\nTekan N atau → untuk memulai...\n")
        
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800/600)
        
        # Setup camera
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0, 1, 5])
        self.scene.add(self.rig)
        
        # Grid
        grid = GridHelper(size=10, gridColor=[0.3, 0.3, 0.3])
        grid.rotateX(-pi / 2)
        self.scene.add(grid)
        
        # Axes
        axes = AxesHelper(axisLength=1.5)
        self.scene.add(axes)
        
        # ===================================================================
        # VERTEX DATA - 3 vertex untuk 1 segitiga
        # ===================================================================
        self.vertices = [
            [-1.0, 0.0, 0.0],  # Vertex 0: kiri (merah)
            [ 1.0, 0.0, 0.0],  # Vertex 1: kanan (hijau)
            [ 0.0, 1.5, 0.0],  # Vertex 2: atas (biru)
        ]
        
        self.colors = [
            [1, 0, 0],  # Vertex 0: merah
            [0, 1, 0],  # Vertex 1: hijau
            [0, 0, 1],  # Vertex 2: biru
        ]
        
        # ===================================================================
        # VISUALISASI VERTEX sebagai SPHERE kecil
        # ===================================================================
        self.vertex_spheres = []
        for i, (pos, color) in enumerate(zip(self.vertices, self.colors)):
            sphere_geom = SphereGeometry(radius=0.1)
            sphere_mat = SurfaceMaterial(properties={
                "useVertexColors": False,
                "baseColor": color
            })
            sphere = Mesh(sphere_geom, sphere_mat)
            sphere.setPosition(pos)
            self.scene.add(sphere)
            self.vertex_spheres.append(sphere)
        
        # ===================================================================
        # LINES - Wireframe (edge dari segitiga) - 3 line segments terpisah
        # ===================================================================
        self.line_meshes = []
        
        # Edge 0-1 (merah ke hijau)
        line_01_pos = [self.vertices[0], self.vertices[1]]
        line_01_col = [self.colors[0], self.colors[1]]
        geom_01 = Geometry()
        geom_01.addAttribute("vec3", "vertexPosition", line_01_pos)
        geom_01.addAttribute("vec3", "vertexColor", line_01_col)
        geom_01.countVertices()
        mat_01 = LineMaterial(properties={"lineWidth": 4})
        mesh_01 = Mesh(geom_01, mat_01)
        mesh_01.visible = False
        self.scene.add(mesh_01)
        self.line_meshes.append(mesh_01)
        
        # Edge 1-2 (hijau ke biru)
        line_12_pos = [self.vertices[1], self.vertices[2]]
        line_12_col = [self.colors[1], self.colors[2]]
        geom_12 = Geometry()
        geom_12.addAttribute("vec3", "vertexPosition", line_12_pos)
        geom_12.addAttribute("vec3", "vertexColor", line_12_col)
        geom_12.countVertices()
        mat_12 = LineMaterial(properties={"lineWidth": 4})
        mesh_12 = Mesh(geom_12, mat_12)
        mesh_12.visible = False
        self.scene.add(mesh_12)
        self.line_meshes.append(mesh_12)
        
        # Edge 2-0 (biru ke merah)
        line_20_pos = [self.vertices[2], self.vertices[0]]
        line_20_col = [self.colors[2], self.colors[0]]
        geom_20 = Geometry()
        geom_20.addAttribute("vec3", "vertexPosition", line_20_pos)
        geom_20.addAttribute("vec3", "vertexColor", line_20_col)
        geom_20.countVertices()
        mat_20 = LineMaterial(properties={"lineWidth": 4})
        mesh_20 = Mesh(geom_20, mat_20)
        mesh_20.visible = False
        self.scene.add(mesh_20)
        self.line_meshes.append(mesh_20)
        
        # ===================================================================
        # TRIANGLE - Filled segitiga
        # ===================================================================
        geometry_triangle = Geometry()
        geometry_triangle.addAttribute("vec3", "vertexPosition", self.vertices)
        geometry_triangle.addAttribute("vec3", "vertexColor", self.colors)
        geometry_triangle.countVertices()
        
        material_triangle = SurfaceMaterial(properties={"useVertexColors": True})
        self.mesh_triangle = Mesh(geometry_triangle, material_triangle)
        self.mesh_triangle.visible = False
        self.scene.add(self.mesh_triangle)
        
        # ===================================================================
        # STEP STATE
        # ===================================================================
        self.time = 0
        self.frame_count = 0
        self.current_step = 0
        self.max_step = 8
        self.rotate_enabled = False
        
        # Track key press untuk prevent multiple triggers
        self.key_pressed = False
        
        self.update_step_visualization()
    
    def update_step_visualization(self):
        """Update visibility berdasarkan current step."""
        print("\n" + "=" * 70)
        print(f"STEP {self.current_step}/{self.max_step}")
        print("=" * 70)
        
        # Hide semua dulu
        for sphere in self.vertex_spheres:
            sphere.visible = False
        for line in self.line_meshes:
            line.visible = False
        self.mesh_triangle.visible = False
        self.rotate_enabled = False
        
        if self.current_step == 0:
            print("Tahap: PERSIAPAN")
            print("→ Graphics pipeline dimulai dengan vertex specification")
            print("→ Kita akan membuat 1 segitiga dari 3 vertex")
            print("\nTekan N atau → untuk lanjut...")
            
        elif self.current_step == 1:
            print("Tahap: VERTEX 0 (MERAH)")
            print("→ Vertex pertama didefinisikan di posisi (-1, 0, 0)")
            print("→ Vertex memiliki atribut: posisi dan warna")
            print("  • Position: vec3(-1.0, 0.0, 0.0)")
            print("  • Color: vec3(1.0, 0.0, 0.0) = merah")
            self.vertex_spheres[0].visible = True
            print("\nTekan N untuk vertex berikutnya...")
            
        elif self.current_step == 2:
            print("Tahap: VERTEX 1 (HIJAU)")
            print("→ Vertex kedua ditambahkan di posisi (1, 0, 0)")
            print("  • Position: vec3(1.0, 0.0, 0.0)")
            print("  • Color: vec3(0.0, 1.0, 0.0) = hijau")
            self.vertex_spheres[0].visible = True
            self.vertex_spheres[1].visible = True
            print("\nTekan N untuk vertex ketiga...")
            
        elif self.current_step == 3:
            print("Tahap: VERTEX 2 (BIRU)")
            print("→ Vertex ketiga melengkapi segitiga di posisi (0, 1.5, 0)")
            print("  • Position: vec3(0.0, 1.5, 0.0)")
            print("  • Color: vec3(0.0, 0.0, 1.0) = biru")
            print("\n✓ VERTEX SPECIFICATION SELESAI")
            print("  Total: 3 vertex siap untuk primitive assembly")
            self.vertex_spheres[0].visible = True
            self.vertex_spheres[1].visible = True
            self.vertex_spheres[2].visible = True
            print("\nTekan N untuk primitive assembly...")
            
        elif self.current_step == 4:
            print("Tahap: PRIMITIVE ASSEMBLY - EDGE 0-1")
            print("→ Menghubungkan Vertex 0 (merah) ke Vertex 1 (hijau)")
            print("→ Primitive type: GL_LINES")
            print("→ Membentuk edge pertama dari segitiga")
            self.vertex_spheres[0].visible = True
            self.vertex_spheres[1].visible = True
            self.vertex_spheres[2].visible = True
            self.line_meshes[0].visible = True
            print("\nTekan N untuk edge berikutnya...")
            
        elif self.current_step == 5:
            print("Tahap: PRIMITIVE ASSEMBLY - EDGE 1-2")
            print("→ Menghubungkan Vertex 1 (hijau) ke Vertex 2 (biru)")
            print("→ Edge kedua terbentuk")
            self.vertex_spheres[0].visible = True
            self.vertex_spheres[1].visible = True
            self.vertex_spheres[2].visible = True
            self.line_meshes[0].visible = True
            self.line_meshes[1].visible = True
            print("\nTekan N untuk edge terakhir...")
            
        elif self.current_step == 6:
            print("Tahap: PRIMITIVE ASSEMBLY - EDGE 2-0")
            print("→ Menghubungkan Vertex 2 (biru) ke Vertex 0 (merah)")
            print("→ Wireframe segitiga lengkap!")
            print("\n✓ PRIMITIVE ASSEMBLY SELESAI")
            print("  Primitive type: GL_TRIANGLES")
            print("  3 vertex → 1 segitiga (wireframe)")
            self.vertex_spheres[0].visible = True
            self.vertex_spheres[1].visible = True
            self.vertex_spheres[2].visible = True
            self.line_meshes[0].visible = True
            self.line_meshes[1].visible = True
            self.line_meshes[2].visible = True
            print("\nTekan N untuk rasterization...")
            
        elif self.current_step == 7:
            print("Tahap: RASTERIZATION & FRAGMENT SHADER")
            print("→ Segitiga dikonversi menjadi fragments (pixels)")
            print("→ Fragment shader menghitung warna untuk setiap pixel")
            print("→ Interpolasi warna dari 3 vertex:")
            print("  • Vertex 0 (merah) + Vertex 1 (hijau) + Vertex 2 (biru)")
            print("  • Barycentric interpolation menghasilkan gradient")
            print("\n✓ RASTERIZATION SELESAI")
            print("  Output: Segitiga ter-rasterisasi dengan smooth color")
            self.vertex_spheres[0].visible = True
            self.vertex_spheres[1].visible = True
            self.vertex_spheres[2].visible = True
            self.line_meshes[0].visible = True
            self.line_meshes[1].visible = True
            self.line_meshes[2].visible = True
            self.mesh_triangle.visible = True
            print("\nTekan N untuk melihat hasil final...")
            
        elif self.current_step == 8:
            print("Tahap: COMPLETE - PIPELINE SELESAI!")
            print("→ Segitiga berhasil di-render ke framebuffer")
            print("→ Rotasi otomatis aktif untuk melihat dari berbagai sudut")
            print("\n✓ GRAPHICS PIPELINE LENGKAP:")
            print("  1. Vertex Specification  → 3 vertex")
            print("  2. Vertex Shader         → Transform vertex")
            print("  3. Primitive Assembly    → Bentuk segitiga")
            print("  4. Rasterization         → Convert ke fragments")
            print("  5. Fragment Shader       → Warna per pixel")
            print("  6. Output                → Render ke screen")
            self.vertex_spheres[0].visible = True
            self.vertex_spheres[1].visible = True
            self.vertex_spheres[2].visible = True
            self.line_meshes[0].visible = True
            self.line_meshes[1].visible = True
            self.line_meshes[2].visible = True
            self.mesh_triangle.visible = True
            self.rotate_enabled = True
            print("\n>>> Tekan N untuk lanjut ke DEMO 1 (Konsep Pipeline)...")
        
        print("=" * 70)
    
    def update(self):
        # Update rig
        self.rig.update(self.input, self.deltaTime)
        
        # Deteksi key press untuk next/back (dengan debounce)
        if self.input.isKeyPressed("n") or self.input.isKeyPressed("right"):
            if not self.key_pressed:
                self.key_pressed = True
                if self.current_step < self.max_step:
                    self.current_step += 1
                    self.update_step_visualization()
                elif self.current_step == self.max_step:
                    print("\n" + "=" * 70)
                    print("TRANSISI KE DEMO 1")
                    print("=" * 70)
                    print("\nMeluncurkan pipeline_demo_1_konsep.py...")
                    print("Demo 1 akan menjelaskan konsep lengkap graphics pipeline.\n")
                    import subprocess
                    subprocess.Popen([sys.executable, "pipeline_demo_1_konsep.py"])
                    self.running = False
        
        elif self.input.isKeyPressed("b") or self.input.isKeyPressed("left"):
            if not self.key_pressed:
                self.key_pressed = True
                if self.current_step > 0:
                    self.current_step -= 1
                    self.update_step_visualization()
        
        else:
            self.key_pressed = False
        
        # Update time
        self.time += self.deltaTime
        
        # Rotasi otomatis hanya di step terakhir
        if self.rotate_enabled and self.current_step == self.max_step:
            rotation_speed = 0.3 * self.deltaTime
            
            # Rotasi semua objek
            for sphere in self.vertex_spheres:
                sphere.rotateY(rotation_speed)
            for line in self.line_meshes:
                line.rotateY(rotation_speed)
            self.mesh_triangle.rotateY(rotation_speed)
        
        # Render
        self.renderer.render(self.scene, self.camera)


# Run
print("\nMemulai demo per-vertex visualization...")
PerVertexDemo(screenSize=[800, 600]).run()
