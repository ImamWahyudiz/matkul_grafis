from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform # Mengimpor kelas Uniform yang sudah dibuat.
from OpenGL.GL import *

class Test(Base):
    def initialize(self):
        print("Initializing program...")
        
        # --- Kode Vertex Shader ---
        vsCode = """
        in vec3 position;          // Input posisi vertex dari CPU.
        uniform vec3 translation;   // Input uniform untuk menggeser posisi.
        void main()
        {
            // Posisi baru adalah posisi asli ditambah vektor pergeseran.
            vec3 pos = position + translation;
            gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
        }
        """

        # --- Kode Fragment Shader ---
        fsCode = """
        uniform vec3 baseColor;     // Input uniform untuk warna dasar objek.
        out vec4 fragColor;         // Output warna akhir piksel.
        void main()
        {
            // Atur warna piksel sesuai dengan uniform baseColor.
            fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
        }
        """

        # --- Inisialisasi Program dan VAO ---
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        # --- Atribut Vertex ---
        # Data vertex untuk sebuah segitiga.
        positionData = [ [0.0, 0.2, 0.0], [0.2, -0.2, 0.0], [-0.2, -0.2, 0.0] ]
        self.vertexCount = len(positionData)
        positionAttribute = Attribute("vec3", positionData)
        positionAttribute.associateVariable(self.programRef, "position")

        # --- Pengaturan Uniform ---
        # Membuat objek Uniform untuk menggeser segitiga pertama ke kiri.
        self.translation1 = Uniform("vec3", [-0.5, 0.0, 0.0])
        self.translation1.locateVariable(self.programRef, "translation")

        # Membuat objek Uniform untuk menggeser segitiga kedua ke kanan.
        self.translation2 = Uniform("vec3", [0.5, 0.0, 0.0])
        self.translation2.locateVariable(self.programRef, "translation")

        # Membuat objek Uniform untuk warna segitiga pertama (merah).
        self.baseColor1 = Uniform("vec3", [1.0, 0.0, 0.0])
        self.baseColor1.locateVariable(self.programRef, "baseColor")

        # Membuat objek Uniform untuk warna segitiga kedua (biru).
        self.baseColor2 = Uniform("vec3", [0.0, 0.0, 1.0])
        self.baseColor2.locateVariable(self.programRef, "baseColor")

    def update(self):
        glUseProgram(self.programRef) # Aktifkan program shader.

        # --- Gambar segitiga pertama ---
        self.translation1.uploadData() # Kirim data pergeseran ke kiri ke GPU.
        self.baseColor1.uploadData()   # Kirim data warna merah ke GPU.
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount) # Gambar segitiga.

        # --- Gambar segitiga kedua ---
        self.translation2.uploadData() # Kirim data pergeseran ke kanan (menimpa nilai lama).
        self.baseColor2.uploadData()   # Kirim data warna biru (menimpa nilai lama).
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount) # Gambar lagi dengan data vertex yang sama.

Test().run()