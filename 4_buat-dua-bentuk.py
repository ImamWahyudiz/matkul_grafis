from core.base import Base
from core.openGLUtils import OpenGLUtils 
from core.attribute import Attribute
from OpenGL.GL import * 

class Test(Base):
    def initialize(self):
        print("init")
        # Vertex Shader
        vsCode = """
        in vec3 position;
        void main(){
            gl_Position = vec4(position.x, position.y, position.z, 1.0);
        }
        """
        # Fragment Shader
        fsCode = """
        out vec4 fragColor;
        void main(){
            fragColor = vec4(1.0, 1.0, 0.0, 1.0);
        }
        """

        # Inisialisasi shader program
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        # Mengatur lebar garis
        glLineWidth(4)

       
        # VAO Vertex Array Object, menyimpan array vertex
        # glGenVertexArrays membuat id buffer
        self.vaoTri = glGenVertexArrays(1)
        # menhubungkan
        glBindVertexArray(self.vaoTri)
        positionDataTri = [[-0.5, 0.8, 0.0], 
                           [-0.2,0.2, 0.0],
                            [-0.8, 0.2, 0.0]]
        # membuat variabel
        self.vertexCountTri = len(positionDataTri)
        positionAttributeTri = Attribute("vec3",positionDataTri)
        positionAttributeTri.associateVariable(self.programRef, "position" )

        self.vaoSquare = glGenVertexArrays(1)
        glBindVertexArray(self.vaoSquare)
        positionDataSquare = [[0.8, 0.8, 0.0], 
                              [0.8,0.2, 0.0],
                              [0.2, 0.2, 0.0], 
                              [0.2, 0.8, 0.0]]

        self.vertexCountSquare =len(positionDataSquare)
        positionAttributeSquare = Attribute("vec3", positionDataSquare)
        positionAttributeSquare.associateVariable(self.programRef, "position")

    def update(self):
        glUseProgram( self.programRef )
        # draw the triangle
        glBindVertexArray( self.vaoTri )
        glDrawArrays( GL_LINE_LOOP , 0 , self.vertexCountTri )
        # draw the square
        glBindVertexArray( self.vaoSquare )
        glDrawArrays( GL_LINE_LOOP , 0 , self.vertexCountSquare )

Test().run()
