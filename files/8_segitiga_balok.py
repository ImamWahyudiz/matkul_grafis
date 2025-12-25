from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.customTriangleGeometry import CustomTriangleGeometry # Menggunakan geometri kustom
from geometry.boxGeometry import BoxGeometry # Mengimpor BoxGeometry untuk objek kedua
from material.surfaceMaterial import SurfaceMaterial
import numpy as np

class Test(Base):
    def initialize(self):
        print("Menginisialisasi program untuk menampilkan segitiga dan kotak sederhana...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.scene.setPosition([0.0, 4.0, 0]) 
        self.camera = Camera( aspectRatio=800/600 )
        self.camera.setPosition( [0, 4, 4] ) # Kamera di [0,0,4] melihat ke origin

        # --- OBJEK 1: SEGITIGA ---
        # Anda bisa mengubah koordinat X, Y, Z dari setiap verteks di bawah ini.
        # Setiap baris adalah satu verteks: [pos_x, pos_y, pos_z]
        positionDataTriangle = [
            [ 0.0,  1.0, 0.0], # Verteks atas
            [-1.0, -1.0, 0.0], # Verteks kiri bawah
            [ 1.0, -1.0, 0.0]  # Verteks kanan bawah
        ]
        
        # Warna merah solid untuk segitiga
        colorDataTriangle = [
            [1.0, 0.0, 0.0], # Merah solid untuk semua verteks
            [1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0]
        ]

        # Membuat geometri segitiga menggunakan CustomTriangleGeometry
        geometryTriangle = CustomTriangleGeometry(positionDataTriangle, colorDataTriangle) 
        
        # Membuat material yang menggunakan warna verteks
        materialTriangle = SurfaceMaterial({"useVertexColors": True} )
        
        # Membuat mesh dari geometri dan material
        self.triangleMesh = Mesh( geometryTriangle, materialTriangle )
        
        # Menambahkan mesh segitiga ke scene
        self.scene.add( self.triangleMesh )

        # --- Mengatur Posisi Segitiga ---
        # Anda bisa mengubah nilai X, Y, Z di bawah ini untuk memindahkan segitiga.
        self.triangleMesh.setPosition([-1.5, 0, 0]) # Posisi awal segitiga
        print(f"Posisi awal segitiga (lokal): {self.triangleMesh.getPosition()}")
        print(f"Posisi awal segitiga (dunia): {self.triangleMesh.getWorldPosition()}")

        # --- OBJEK 2: KOTAK ---
        # Membuat geometri kotak (ukuran default 1x1x1)
        geometryBox = BoxGeometry()
        
        # Membuat material dengan warna solid (misal: biru)
        # materialBox = SurfaceMaterial()
        materialBox = SurfaceMaterial({"useVertexColors": True})
        # materialBox.uniforms["baseColor"].data = [0.0, 0.0, 1.0] # Biru solid
        
        # Membuat mesh dari geometri dan material
        self.boxMesh = Mesh( geometryBox, materialBox )
        
        # Menambahkan mesh kotak ke scene
        self.scene.add( self.boxMesh )

        # --- Mengatur Posisi Kotak ---
        # Anda bisa mengubah nilai X, Y, Z di bawah ini untuk memindahkan kotak.
        self.boxMesh.setPosition([1.5, 0, 0]) # Posisi awal kotak
        print(f"Posisi awal kotak (lokal): {self.boxMesh.getPosition()}")
        print(f"Posisi awal kotak (dunia): {self.boxMesh.getWorldPosition()}")

        # --- Demonstrasi Fungsi Object3D lainnya (opsional, bisa diaktifkan/dinonaktifkan) ---
        # Coba aktifkan baris di bawah ini satu per satu untuk melihat efeknya:
        # self.triangleMesh.rotateX(np.pi / 4) # Memutar segitiga
        # self.boxMesh.scale(0.7)             # Memperkecil kotak
        # self.boxMesh.rotateX(np.pi / 4) 

    def update(self):
        # Tidak ada rotasi otomatis di sini, balok akan diam.
        self.boxMesh.rotateY( 0.0514 )
        self.boxMesh.rotateX( 0.0337 ) 
        # Merender scene dari sudut pandang kamera
        self.renderer.render( self.scene, self.camera)

# Menjalankan aplikasi dengan ukuran layar 800x600
Test( screenSize=[800,600] ).run()
