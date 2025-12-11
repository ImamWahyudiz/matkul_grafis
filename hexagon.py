from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute 
from OpenGL.GL import * 

class Test(Base):
    def initialize(self):
        print("init...")

        # position merujuk dari referensi associateVariable
        vsCode = """
        in vec3 position;
        void main(){
            gl_Position = vec4(position.x, position.y, position.z, 1.0);
        }
        """

        fsCode = """
        out vec4 fragColor;
        void main(){
           fragColor = vec4(0.0, 1.0, 0.0, 1.0);

        }
        """

        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)
        glLineWidth(4)

        # membuat tempat menyimpan konfigurasi buffer
        # vertex array object
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        positionData = [ 
            [0.0, 0.9, 0.0],   
            [0.5, 0.25, 0.0],   # titik kanan    
            [0.0, -0.9, 0.0],  # titik bawah
            [-0.5, 0.25, 0.0]   # titik kiri
        ]


        self.vertexCount = len(positionData)
        # Attribute mengupload data ke GPU
        positionAttribute = Attribute("vec3", positionData)
        # associateVariable Menghubungkan data di GPU dengan variabel `position` di Vertex Shader
        positionAttribute.associateVariable(self.programRef, "position")

    def update(self):
        # mengaktifkan shader program
        glUseProgram(self.programRef)
        # perintah menggambar, bisa diisi 
        # GL_LINES : putus-putus
        # GL_LINE_STRIP : garis terakhir terpisah
        # GL_LINE_LOOP : bersambung
        # GL_TRIANGLES : segitiga per tiga titik
        # GL_TRIANGLE_FAN : segitiga menyebar

        glDrawArrays(GL_TRIANGLE_FAN, 0, self.vertexCount)

Test().run()