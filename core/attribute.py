from OpenGL.GL import *
import numpy as np 

class Attribute(object):
    def __init__(self, dataType, data):
        self.dataType = dataType
        self.data = data
        # membuat id buffer 
        self.bufferRef = glGenBuffers(1)
        self.uploadData()

    def uploadData(self):
        # ubah list menjadi numpy array
        # ubah ke bentuk 32 bit
        data = np.array(self.data).astype(np.float32)
        # aktifkan buffer 
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)
        # kirim data ke GPU
        # meratakan array menjadi 1 dimensi
        # GL_STATIC_DRAW memberi informasi data tidak sering berubah
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    def associateVariable(self, programRef, variabelName):
        # mencari lokasi variabel di shader berdasar namanya
        variabelRef = glGetAttribLocation(programRef, variabelName)
        if variabelRef == -1:
            return 
        # mengaktifkan buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)
        if self.dataType == 'int':
            glVertexAttribPointer(variabelRef, 1, GL_INT, False, 0, None)
        elif self.dataType == 'float':
            glVertexAttribPointer(variabelRef, 1, GL_FLOAT, False, 0, None)
        elif self.dataType == 'vec2':
            glVertexAttribPointer(variabelRef, 2, GL_FLOAT, False, 0, None)
        elif self.dataType == 'vec3':
            glVertexAttribPointer(variabelRef, 3, GL_FLOAT, False, 0, None)
        elif self.dataType == 'vec4':
            glVertexAttribPointer(variabelRef, 4, GL_FLOAT, False, 0, None)
        else:
            raise Exception("Attribute "+variabelName+" has unknown type "+self.dataType)
        # mengaktifkan tempat di GPU agar data bisa mengalir ke shader saat proses rendering  
        glEnableVertexAttribArray(variabelRef)