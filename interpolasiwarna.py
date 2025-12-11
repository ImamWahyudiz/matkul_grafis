from core.base import Base 
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute 
from OpenGL.GL import *

# --- Definisi Kelas Utama ---
# Membuat kelas 'Test' yang mewarisi fungsionalitas dari kelas 'Base' (kemungkinan besar untuk membuat window dan menjalankan loop utama)
class Test(Base):
    # --- Metode Inisialisasi ---
    # Metode ini akan dipanggil sekali saat program dimulai untuk melakukan semua pengaturan awal.
    def initialize(self):
        print("init...") # Mencetak pesan ke konsol untuk menandakan proses inisialisasi dimulai.

        # --- Kode Vertex Shader (vsCode) ---
        # Shader ini dieksekusi untuk setiap vertex (titik sudut) pada objek.
        vsCode = """
        in vec3 position;      // Menerima data posisi vertex (x, y, z) sebagai input.
        in vec3 vertexColor;   // Menerima data warna vertex (r, g, b) sebagai input.
        out vec3 color;         // Mendefinisikan variabel output 'color' untuk dikirim ke Fragment Shader.
        void main(){
            // Menetapkan posisi akhir dari vertex di layar.
            gl_Position = vec4(position.x, position.y, position.z, 1.0);
            // Meneruskan warna dari vertex ini ke Fragment Shader. OpenGL akan menginterpolasi nilai ini.
            color = vertexColor;
        }
        """

        # --- Kode Fragment Shader (fsCode) ---
        # Shader ini dieksekusi untuk setiap piksel (fragment) yang akan digambar.
        fsCode = """
        in vec3 color;          // Menerima data warna yang sudah diinterpolasi dari Vertex Shader.
        out vec4 fragColor;     // Mendefinisikan variabel output untuk warna piksel akhir.
        void main(){
            // Menetapkan warna akhir piksel dengan nilai yang diterima (r, g, b) dan alpha 1.0 (tidak transparan).
            fragColor = vec4(color.r, color.g, color.b, 1.0);
        }
        """

        # --- Inisialisasi Program Shader ---
        # Mengkompilasi dan menautkan (link) vsCode dan fsCode menjadi satu program GPU.
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        # --- Pengaturan Render ---
        glPointSize(10) # Mengatur ukuran titik menjadi 10 piksel (tidak digunakan di sini).
        glLineWidth(4)  # Mengatur ketebalan garis menjadi 4 piksel (tidak digunakan di sini).

        # --- Pengaturan Vertex Array Object (VAO) ---
        # VAO menyimpan semua konfigurasi data vertex (posisi, warna, dll.) untuk satu objek.
        vaoRef = glGenVertexArrays(1) # Membuat satu VAO baru.
        glBindVertexArray(vaoRef)      # Mengaktifkan VAO yang baru dibuat.

        # --- Data Posisi Vertex ---
        # Mendefinisikan 6 titik koordinat (x, y, z) untuk membentuk sebuah heksagon.
        positionData = [ [0.8, 0.0, 0.0], [0.4, 0.6,0.0],
                        [-0.4, 0.6, 0.0], [-0.8, 0.0, 0.0], 
                        [-0.4,-0.6, 0.0], [0.4, -0.6, 0.0] ]

        # Menyimpan jumlah vertex untuk digunakan saat menggambar.
        self.vertexCount = len(positionData)

        # --- Atribut Posisi ---
        # Membuat objek Attribute untuk mengelola data posisi.
        positionAttribute = Attribute("vec3",positionData)
        # Menghubungkan data posisi ini dengan variabel 'position' di dalam Vertex Shader.
        positionAttribute.associateVariable(self.programRef, "position" )

        # --- Data Warna Vertex ---
        # Mendefinisikan 6 warna (merah, oranye, kuning, hijau, biru, ungu) untuk setiap vertex.
        colorData = [ [1.0, 0.0, 0.0], [1.0, 0.5,0.0],
                    [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], 
                    [0.0,0.0, 1.0], [0.5, 0.0, 1.0] ]

        # --- Atribut Warna ---
        # Membuat objek Attribute untuk mengelola data warna.
        colorAttribute = Attribute("vec3", colorData)
        # Menghubungkan data warna ini dengan variabel 'vertexColor' di dalam Vertex Shader.
        colorAttribute.associateVariable(self.programRef, "vertexColor" )

    # --- Metode Update ---
    # Metode ini dipanggil berulang kali dalam loop utama untuk menggambar frame baru.
    def update(self):
        glUseProgram( self.programRef ) # Mengaktifkan program shader yang sudah dibuat.
        # Memberi perintah pada GPU untuk menggambar bentuk menggunakan mode GL_TRIANGLE_FAN,
        # dimulai dari vertex ke-0, sebanyak self.vertexCount vertex.
        glDrawArrays( GL_TRIANGLE_FAN , 0 , self.vertexCount )

# --- Menjalankan Aplikasi ---
# Membuat instance dari kelas Test dan memanggil metode run() untuk memulai aplikasi.
Test().run()