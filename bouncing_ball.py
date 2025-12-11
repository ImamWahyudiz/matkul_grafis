from core.base import Base
from core.openGLUtils import OpenGLUtils 
from OpenGL.GL import *
import math

class BouncingBall(Base):
    def initialize(self):
        print("Initializing bouncing ball animation...")
        
        # Vertex shader dengan posisi yang bisa diubah via uniform
        vsCode = """#version 330 core
        uniform vec2 position;
        
        void main()
        {
            gl_Position = vec4(position.x, position.y, 0.0, 1.0);
        }
        """

        # Fragment shader untuk warna bola
        fsCode = """#version 330 core
        out vec4 fragColor;
        uniform vec3 color;
        
        void main()
        {
            fragColor = vec4(color, 1.0);
        }
        """

        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        # Setup VAO
        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        # Ukuran bola
        glPointSize(50)
        
        # Enable point smoothing untuk bola bulat
        glEnable(GL_POINT_SMOOTH)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Properti animasi
        self.ball_y = 0.0          # Posisi Y bola
        self.ball_x = 0.0          # Posisi X bola
        self.velocity_y = 0.0      # Kecepatan vertikal
        self.velocity_x = 0.01     # Kecepatan horizontal
        self.gravity = -0.0015     # Gravitasi
        self.bounce_damping = 0.85 # Redaman pantulan
        self.ground = -0.9         # Posisi tanah
        
        # Get uniform locations
        self.positionLoc = glGetUniformLocation(self.programRef, "position")
        self.colorLoc = glGetUniformLocation(self.programRef, "color")

        OpenGLUtils.printSystemInfo()

    def update(self):
        # Update fisika bola
        self.velocity_y += self.gravity
        self.ball_y += self.velocity_y
        self.ball_x += self.velocity_x
        
        # Pantulan di tanah
        if self.ball_y <= self.ground:
            self.ball_y = self.ground
            self.velocity_y = -self.velocity_y * self.bounce_damping
            
            # Hentikan bouncing jika terlalu lambat
            if abs(self.velocity_y) < 0.001:
                self.velocity_y = 0
        
        # Pantulan di dinding kiri dan kanan
        if self.ball_x >= 0.95 or self.ball_x <= -0.95:
            self.velocity_x = -self.velocity_x
        
        # Warna berubah berdasarkan ketinggian
        red = (self.ball_y + 1.0) / 2.0
        green = 1.0 - red
        blue = 0.5
        
        # Render
        glClearColor(0.1, 0.1, 0.15, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        glUseProgram(self.programRef)
        glUniform2f(self.positionLoc, self.ball_x, self.ball_y)
        glUniform3f(self.colorLoc, red, green, blue)
        glDrawArrays(GL_POINTS, 0, 1)

BouncingBall().run()
