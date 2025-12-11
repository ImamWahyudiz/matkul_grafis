from OpenGL.GL import *

# Mendefinisikan kelas bernama Uniform.
class Uniform(object):
    # Metode inisialisasi (constructor) yang dipanggil saat objek Uniform dibuat.
    def __init__(self, dataType, data):
        # Menyimpan tipe data (misal: "vec3", "float") sebagai string.
        self.dataType = dataType
        # Menyimpan data aktual yang akan dikirim ke GPU (misal: [1.0, 0.0, 0.0]).
        self.data = data
        # Referensi (lokasi memori) ke variabel uniform di GPU, awalnya None.
        self.variableRef = None

    # Metode untuk menemukan lokasi variabel uniform di dalam program shader.
    def locateVariable(self, programRef, variableName):
        # Menggunakan fungsi OpenGL untuk mendapatkan lokasi memori dari variabel uniform
        # dengan nama `variableName` di dalam program shader `programRef`.
        self.variableRef = glGetUniformLocation(programRef, variableName)

    # Metode untuk mengirim (upload) data dari CPU ke GPU.
    def uploadData(self):
        # Jika variabel tidak ditemukan di shader (lokasi = -1), hentikan proses.
        if self.variableRef == -1:
            return
        
        # Memeriksa `dataType` dan memanggil fungsi glUniform* yang sesuai.
        # Setiap fungsi ini mengirimkan data ke lokasi `self.variableRef` di GPU.
        if self.dataType == "int":
            glUniform1i(self.variableRef, self.data)
        elif self.dataType == "bool":
            glUniform1i(self.variableRef, self.data)
        elif self.dataType == "float":
            glUniform1f(self.variableRef, self.data)
        elif self.dataType == "vec2":
            glUniform2f(self.variableRef, self.data[0], self.data[1])
        elif self.dataType == "vec3":
            glUniform3f(self.variableRef, self.data[0], self.data[1], self.data[2])
        elif self.dataType == "vec4":
            glUniform4f(self.variableRef, self.data[0], self.data[1], self.data[2], self.data[3])