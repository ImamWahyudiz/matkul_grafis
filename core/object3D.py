# Mengimpor kelas Matrix dari modul core.matrix untuk operasi matriks
from core.matrix import Matrix

# Mendefinisikan kelas Object3D yang akan merepresentasikan objek dalam ruang 3D
class Object3D(object):
    # Metode inisialisasi untuk objek Object3D
    def __init__(self):
        # Menginisialisasi matriks transformasi lokal objek sebagai matriks identitas
        self.transform = Matrix.makeIdentity()
        # Menginisialisasi referensi ke objek induk (parent) sebagai None
        self.parent = None
        # Menginisialisasi daftar kosong untuk menyimpan objek anak (children)
        self.children = []

    # Metode untuk menambahkan objek anak ke objek saat ini
    def add(self, child):
        # Menambahkan objek anak ke daftar anak
        self.children.append(child)
        # Mengatur objek saat ini sebagai induk dari objek anak
        child.parent = self

    # Metode untuk menghapus objek anak dari objek saat ini
    def remove(self, child):
        # Menghapus objek anak dari daftar anak
        self.children.remove(child)
        # Mengatur induk objek anak yang dihapus menjadi None
        child.parent = None

    # Metode untuk menghitung matriks transformasi dunia (world matrix) objek
    def getWorldMatrix(self):
        # Memeriksa apakah objek ini memiliki induk
        if self.parent == None:
            # Jika tidak ada induk, matriks dunia adalah matriks transformasi lokal objek itu sendiri
            return self.transform
        # Jika objek memiliki induk
        else:
            # Mengembalikan hasil perkalian matriks dunia induk dengan matriks transformasi lokal objek ini
            return self.parent.getWorldMatrix() @  self.transform

    # Metode untuk mendapatkan daftar semua turunan (descendants) dari objek ini
    def getDescendantList(self):
        # Menginisialisasi daftar kosong untuk menyimpan semua objek turunan
        descendants = []
        # Menginisialisasi daftar node yang akan diproses dengan objek ini sebagai elemen pertama
        nodesToProcess = [self]
        # Melanjutkan perulangan selama masih ada node yang perlu diproses
        while len( nodesToProcess ) > 0:
            # Mengambil node pertama dari daftar nodesToProcess (mirip BFS)
            node = nodesToProcess.pop(0)
            # Menambahkan node yang sedang diproses ke daftar turunan
            descendants.append(node)
            # Menambahkan anak-anak dari node yang sedang diproses ke awal daftar nodesToProcess untuk diproses selanjutnya
            nodesToProcess = node.children +  nodesToProcess
        # Mengembalikan daftar semua objek turunan
        return descendants

    # Metode untuk menerapkan matriks transformasi ke objek
    def applyMatrix(self, matrix, localCoord=True):
        # Memeriksa apakah transformasi harus diterapkan dalam koordinat lokal
        if localCoord:
            # Jika dalam koordinat lokal, matriks transformasi baru dikalikan setelah matriks transformasi objek saat ini
            self.transform = self.transform @ matrix
        # Jika transformasi harus diterapkan dalam koordinat dunia
        else:
            # Matriks transformasi baru dikalikan sebelum matriks transformasi objek saat ini
            self.transform = matrix @ self.transform

    # Metode untuk melakukan translasi (pergeseran) objek
    def translate(self, x,y,z, localCoord=True):
        # Membuat matriks translasi menggunakan nilai x, y, dan z yang diberikan
        m = Matrix.makeTranslation(x,y,z)
        # Menerapkan matriks translasi ke objek
        self.applyMatrix(m, localCoord)

    # Metode untuk melakukan rotasi objek di sekitar sumbu X
    def rotateX(self, angle, localCoord=True):
        # Membuat matriks rotasi di sekitar sumbu X menggunakan sudut yang diberikan
        m = Matrix.makeRotationX(angle)
        # Menerapkan matriks rotasi ke objek
        self.applyMatrix(m, localCoord)

    # Metode untuk melakukan rotasi objek di sekitar sumbu Y
    def rotateY(self, angle, localCoord=True):
        # Membuat matriks rotasi di sekitar sumbu Y menggunakan sudut yang diberikan
        m = Matrix.makeRotationY(angle)
        # Menerapkan matriks rotasi ke objek
        self.applyMatrix(m, localCoord)

    # Metode untuk melakukan rotasi objek di sekitar sumbu Z
    def rotateZ(self, angle, localCoord=True):
        # Membuat matriks rotasi di sekitar sumbu Z menggunakan sudut yang diberikan
        m = Matrix.makeRotationZ(angle)
        # Menerapkan matriks rotasi ke objek
        self.applyMatrix(m, localCoord)

    # Metode untuk melakukan penskalaan (scaling) objek secara seragam
    def scale(self, s, localCoord=True):
        # Membuat matriks skala menggunakan faktor skala yang diberikan
        m = Matrix.makeScale(s)
        # Menerapkan matriks skala ke objek
        self.applyMatrix(m, localCoord)

    # Metode untuk mendapatkan posisi lokal objek
    def getPosition(self):
        # Mengembalikan komponen translasi (x, y, z) dari matriks transformasi lokal objek
        return [ self.transform.item((0,3)),self.transform.item((1,3)),self.transform.item((2,3)) ]

    # Metode untuk mendapatkan posisi objek dalam koordinat dunia
    def getWorldPosition(self):
        # Menghitung matriks transformasi dunia objek
        worldTransform = self.getWorldMatrix()
        # Mengembalikan komponen translasi (x, y, z) dari matriks transformasi dunia objek
        return [ worldTransform.item((0,3)),worldTransform.item((1,3)),worldTransform.item((2,3)) ]

    # Metode untuk mengatur posisi lokal objek
    def setPosition(self, position):
        # Mengatur komponen x dari translasi dalam matriks transformasi lokal
        self.transform[0,3] = position[0]
        # Mengatur komponen y dari translasi dalam matriks transformasi lokal
        self.transform[1,3] = position[1]
        # Mengatur komponen z dari translasi dalam matriks transformasi lokal
        self.transform[2,3] = position[2]