# Impor pustaka numpy untuk operasi matriks
import numpy
# Impor fungsi trigonometri dan konstanta pi dari pustaka math
from math import sin, cos, tan, pi

# Definisikan kelas Matrix untuk operasi matriks dalam grafika komputer
class Matrix(object):
    
    # Metode statis untuk membuat matriks identitas 4x4
    @staticmethod
    def makeIdentity():
        # Mengembalikan matriks identitas 4x4 sebagai array numpy dengan tipe data float
        return numpy.array( [[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]] ).astype(float)
        
    # Metode statis untuk membuat matriks translasi (pergeseran)
    @staticmethod
    def makeTranslation(x, y, z):
        # Mengembalikan matriks translasi 4x4 yang menggeser objek sejauh x, y, dan z
        return numpy.array([[1, 0, 0, x],[0, 1, 0, y],[0, 0, 1, z],[0, 0, 0, 1]]).astype(float)
        
    # Metode statis untuk membuat matriks rotasi terhadap sumbu X
    @staticmethod
    def makeRotationX(angle):
        # Hitung nilai kosinus dari sudut rotasi
        c = cos(angle)
        # Hitung nilai sinus dari sudut rotasi
        s = sin(angle)
        # Mengembalikan matriks rotasi 4x4 terhadap sumbu X
        return numpy.array([[1, 0, 0, 0],[0, c, -s, 0],[0, s, c, 0],[0, 0, 0, 1]]).astype(float)
        
    # Metode statis untuk membuat matriks rotasi terhadap sumbu Y
    @staticmethod
    def makeRotationY(angle):
        # Hitung nilai kosinus dari sudut rotasi
        c = cos(angle)
        # Hitung nilai sinus dari sudut rotasi
        s = sin(angle)
        # Mengembalikan matriks rotasi 4x4 terhadap sumbu Y
        return numpy.array([[ c, 0, s, 0],[ 0, 1, 0, 0],[-s, 0, c, 0],[ 0, 0, 0, 1]]).astype(float)
        
    # Metode statis untuk membuat matriks rotasi terhadap sumbu Z
    @staticmethod
    def makeRotationZ(angle):
        # Hitung nilai kosinus dari sudut rotasi
        c = cos(angle)
        # Hitung nilai sinus dari sudut rotasi
        s = sin(angle)
        # Mengembalikan matriks rotasi 4x4 terhadap sumbu Z
        return numpy.array([[c, -s, 0, 0],[s, c, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]]).astype(float)
        
    # Metode statis untuk membuat matriks skala (penskalaan)
    @staticmethod
    def makeScale(s):
        # Mengembalikan matriks skala 4x4 yang mengubah ukuran objek dengan faktor s
        return numpy.array([[s, 0, 0, 0],[0, s, 0, 0],[0, 0, s, 0],[0, 0, 0, 1]]).astype(float)
        
    # Metode statis untuk membuat matriks proyeksi perspektif
    @staticmethod
    def makePerspective(angleOfView=60,aspectRatio=1, near=0.1, far=1000):
        # Konversi sudut pandang dari derajat ke radian
        a = angleOfView * pi/180.0
        # Hitung jarak dari kamera ke bidang proyeksi
        d = 1.0 / tan(a/2)
        # Simpan rasio aspek
        r = aspectRatio
        # Hitung nilai untuk transformasi kedalaman (z)
        b = (far + near) / (near - far)
        # Hitung nilai lain untuk transformasi kedalaman (z)
        c = 2*far*near / (near - far)
        # Mengembalikan matriks proyeksi perspektif 4x4
        return numpy.array([[d/r, 0, 0, 0],[0,d, 0, 0],[0,0, b, c],[0,0, -1, 0]]).astype(float)
