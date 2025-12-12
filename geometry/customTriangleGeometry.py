from geometry.geometry import Geometry

class CustomTriangleGeometry(Geometry):
    def __init__(self, positionData, colorData):
        super().__init__()
        # Menambahkan atribut posisi verteks
        self.addAttribute("vec3", "vertexPosition", positionData)
        # Menambahkan atribut warna verteks
        self.addAttribute("vec3", "vertexColor", colorData)
        # Menghitung jumlah verteks dari data posisi
        self.countVertices()
