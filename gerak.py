# Mengimpor kelas-kelas yang diperlukan dari direktori core
from core.base import Base  # Kelas dasar untuk aplikasi OpenGL
from core.openGLUtils import OpenGLUtils  # Utilitas untuk mengelola program shader
from core.attribute import Attribute  # Mengelola data atribut vertex
from core.uniform import Uniform  # Mengelola data uniform shader
from OpenGL.GL import *  # Mengimpor semua fungsi inti OpenGL

# Mendefinisikan kelas Test yang merupakan turunan dari kelas Base
class Test(Base):
    # Metode inisialisasi, dipanggil sekali saat program dimulai
    def initialize(self):
        print("Initializing program...")  # Mencetak pesan ke konsol

        # Kode shader untuk vertex (Vertex Shader)
        vsCode = """
        in vec3 position;  // Menerima posisi vertex sebagai input
        uniform vec3 translation;  // Menerima vektor translasi sebagai uniform
        void main()
        {
            // Menambahkan translasi ke posisi vertex
            vec3 pos = position + translation;
            // Menetapkan posisi akhir vertex
            gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
        }
        """
        # Kode shader untuk fragment (Fragment Shader)
        fsCode = """
        uniform vec3 baseColor;  // Menerima warna dasar sebagai uniform
        out vec4 fragColor;  // Menetapkan warna fragment sebagai output
        void main()
        {
            // Menetapkan warna fragment ke warna dasar yang diberikan
            fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
        }
        """

        # Menginisialisasi program shader dengan kode vsCode dan fsCode
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)
        # Menetapkan warna untuk membersihkan layar (hitam)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        # Menyiapkan Vertex Array Object (VAO)
        vaoRef = glGenVertexArrays(1)  # Membuat satu VAO
        glBindVertexArray(vaoRef)  # Mengikat (mengaktifkan) VAO
        
        # Menyiapkan data atribut vertex untuk posisi
        positionData = [ [0.0, 0.2, 0.0], 
                        [0.2, -0.2,0.0],
                        [-0.2, -0.2, 0.0] ]  # Koordinat untuk sebuah segitiga
        self.vertexCount = len(positionData)  # Jumlah vertex
        # Membuat objek Attribute untuk data posisi
        positionAttribute = Attribute("vec3", positionData)
        # Menghubungkan data posisi ke variabel 'position' di shader
        positionAttribute.associateVariable(self.programRef, "position")
        
        # Menyiapkan data uniform
        # Uniform untuk translasi, dimulai dari posisi [-0.5, 0.0, 0.0]
        self.translation = Uniform("vec3", [-0.5, 0.0, 0.0])
        # Menghubungkan uniform translasi ke variabel 'translation' di shader
        self.translation.locateVariable(self.programRef, "translation")
        # Uniform untuk warna dasar (merah)
        self.baseColor = Uniform("vec3", [1.0, 0.0, 0.0])
        # Menghubungkan uniform warna ke variabel 'baseColor' di shader
        self.baseColor.locateVariable(self.programRef, "baseColor")

    # Metode update, dipanggil berulang kali di setiap frame
    def update(self):
        # Memperbarui data
        # Menambah nilai koordinat x dari translasi sebesar 0.01
        self.translation.data[0] += 0.01
        # Jika segitiga keluar dari layar di sebelah kanan
        if self.translation.data[0] > 1.2:
            # Pindahkan segitiga kembali ke sebelah kiri layar
            self.translation.data[0] = -1.2
            
        # Merender adegan
        # Membersihkan buffer warna dengan warna yang telah ditetapkan
        glClear(GL_COLOR_BUFFER_BIT)
        # Menggunakan program shader yang telah diinisialisasi
        glUseProgram(self.programRef)
        # Mengunggah data translasi dan warna ke shader
        self.translation.uploadData()
        self.baseColor.uploadData()
        # Menggambar array vertex sebagai segitiga
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

# Membuat instance dari kelas Test dan menjalankan program
Test().run()