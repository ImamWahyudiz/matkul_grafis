"""
Graphics Pipeline Module
========================
Modul ini menjelaskan dan mendemonstrasikan cara kerja Graphics Pipeline dalam OpenGL.

Graphics Pipeline adalah serangkaian tahapan yang dilalui data geometri untuk 
ditransformasi dari koordinat objek 3D menjadi piksel pada layar 2D.

Tahapan Utama Graphics Pipeline:
1. Vertex Specification - Mendefinisikan vertex data (posisi, warna, texture coords)
2. Vertex Processing - Transformasi vertex (Model, View, Projection)
3. Vertex Post-Processing - Clipping, Culling
4. Primitive Assembly - Menggabungkan vertices menjadi primitif (triangles, lines)
5. Rasterization - Mengkonversi primitif menjadi fragments (pixel candidates)
6. Fragment Processing - Menghitung warna setiap fragment (Fragment Shader)
7. Per-Sample Operations - Depth test, blending, output ke framebuffer
"""

import numpy as np
from core.matrix import Matrix


class PipelineVisualizer:
    """
    Kelas untuk memvisualisasikan tahapan-tahapan graphics pipeline.
    """
    
    @staticmethod
    def explain_vertex_specification():
        """
        Tahap 1: Vertex Specification
        Mendefinisikan data vertex yang akan dirender.
        """
        print("=" * 60)
        print("TAHAP 1: VERTEX SPECIFICATION")
        print("=" * 60)
        print("Pada tahap ini, kita mendefinisikan data vertex:")
        print("- Posisi vertex dalam 3D space")
        print("- Atribut tambahan (warna, normal, texture coordinates)")
        print()
        
        # Contoh vertex data untuk segitiga
        vertices = np.array([
            [-0.5, -0.5, 0.0],  # Vertex 1
            [ 0.5, -0.5, 0.0],  # Vertex 2
            [ 0.0,  0.5, 0.0]   # Vertex 3
        ], dtype=float)
        
        print("Contoh: Vertex data untuk segitiga")
        print(f"Vertex 1: {vertices[0]}")
        print(f"Vertex 2: {vertices[1]}")
        print(f"Vertex 3: {vertices[2]}")
        print()
        
        return vertices
    
    @staticmethod
    def explain_vertex_processing(vertices):
        """
        Tahap 2: Vertex Processing
        Mentransformasi vertex menggunakan matriks transformasi.
        """
        print("=" * 60)
        print("TAHAP 2: VERTEX PROCESSING (Transformasi)")
        print("=" * 60)
        print("Pada tahap ini, setiap vertex ditransformasi menggunakan:")
        print()
        print("1. MODEL MATRIX - Transformasi dari object space ke world space")
        print("   (Rotasi, translasi, scaling objek dalam dunia 3D)")
        print()
        print("2. VIEW MATRIX - Transformasi dari world space ke view space")
        print("   (Posisi dan orientasi kamera)")
        print()
        print("3. PROJECTION MATRIX - Transformasi dari view space ke clip space")
        print("   (Perspektif atau orthographic projection)")
        print()
        
        # Model transformation (scaling dan rotasi)
        model_matrix = Matrix.makeRotationZ(0.5) @ Matrix.makeScale(0.8)
        
        # View transformation (kamera mundur di sumbu Z)
        view_matrix = Matrix.makeTranslation(0, 0, -5)
        
        # Projection transformation (perspektif)
        projection_matrix = Matrix.makePerspective(60, 1.0, 0.1, 100)
        
        # MVP Matrix (gabungan semua transformasi)
        mvp_matrix = projection_matrix @ view_matrix @ model_matrix
        
        print("Transformasi vertex:")
        transformed_vertices = []
        for i, vertex in enumerate(vertices):
            # Tambahkan komponen w=1 untuk homogeneous coordinates
            vertex_homogeneous = np.append(vertex, 1.0)
            
            # Terapkan MVP matrix
            transformed = mvp_matrix @ vertex_homogeneous
            
            # Perspective division (w-division)
            if transformed[3] != 0:
                transformed = transformed / transformed[3]
            
            transformed_vertices.append(transformed[:3])
            print(f"Vertex {i+1}: {vertex} -> {transformed[:3]}")
        
        print()
        return np.array(transformed_vertices)
    
    @staticmethod
    def explain_primitive_assembly():
        """
        Tahap 3: Primitive Assembly
        Menggabungkan vertices menjadi primitif geometri.
        """
        print("=" * 60)
        print("TAHAP 3: PRIMITIVE ASSEMBLY")
        print("=" * 60)
        print("Pada tahap ini, vertices digabungkan menjadi primitif:")
        print()
        print("Jenis primitif:")
        print("- GL_POINTS: Setiap vertex menjadi satu titik")
        print("- GL_LINES: Setiap 2 vertices menjadi satu garis")
        print("- GL_TRIANGLES: Setiap 3 vertices menjadi satu segitiga")
        print("- GL_TRIANGLE_STRIP: Vertices membentuk strip segitiga")
        print()
        print("Untuk contoh kita (3 vertices), menggunakan GL_TRIANGLES:")
        print("Vertex 1, 2, 3 -> Triangle 1")
        print()
    
    @staticmethod
    def explain_rasterization():
        """
        Tahap 4: Rasterization
        Mengkonversi primitif menjadi fragments (pixel candidates).
        """
        print("=" * 60)
        print("TAHAP 4: RASTERIZATION")
        print("=" * 60)
        print("Pada tahap ini:")
        print("1. Primitif geometri (garis, segitiga) dikonversi ke fragments")
        print("2. Fragment adalah 'pixel candidate' - data untuk satu pixel")
        print("3. Setiap fragment berisi:")
        print("   - Posisi pada layar (x, y)")
        print("   - Depth value (z)")
        print("   - Atribut yang di-interpolasi (warna, texture coords, dll)")
        print()
        print("Contoh: Segitiga dengan 3 vertices akan menghasilkan")
        print("        ribuan fragments yang menutupi area segitiga tersebut")
        print()
    
    @staticmethod
    def explain_fragment_processing():
        """
        Tahap 5: Fragment Processing (Fragment Shader)
        Menghitung warna final setiap fragment.
        """
        print("=" * 60)
        print("TAHAP 5: FRAGMENT PROCESSING (Fragment Shader)")
        print("=" * 60)
        print("Pada tahap ini, Fragment Shader dijalankan untuk setiap fragment:")
        print()
        print("Fragment Shader bertanggung jawab untuk:")
        print("1. Menghitung warna final fragment")
        print("2. Texture sampling (mengambil warna dari texture)")
        print("3. Perhitungan lighting (Phong, Lambert, dll)")
        print("4. Special effects (bump mapping, normal mapping, dll)")
        print()
        print("Input Fragment Shader:")
        print("- Atribut yang di-interpolasi dari vertices")
        print("- Uniform variables (lighting, material properties)")
        print("- Texture samplers")
        print()
        print("Output Fragment Shader:")
        print("- Warna RGBA untuk fragment tersebut")
        print()
    
    @staticmethod
    def explain_output_operations():
        """
        Tahap 6: Per-Sample Operations
        Operasi akhir sebelum fragment ditulis ke framebuffer.
        """
        print("=" * 60)
        print("TAHAP 6: PER-SAMPLE OPERATIONS")
        print("=" * 60)
        print("Operasi terakhir sebelum fragment menjadi pixel:")
        print()
        print("1. DEPTH TEST (Z-buffering)")
        print("   - Membandingkan depth fragment dengan depth buffer")
        print("   - Hanya fragment terdekat yang ditulis")
        print("   - Mengatasi masalah objek yang saling tumpang tindih")
        print()
        print("2. STENCIL TEST")
        print("   - Masking area tertentu pada layar")
        print("   - Untuk efek seperti refleksi, shadows")
        print()
        print("3. BLENDING")
        print("   - Mencampur warna fragment dengan warna di framebuffer")
        print("   - Untuk transparansi dan efek lainnya")
        print()
        print("4. OUTPUT KE FRAMEBUFFER")
        print("   - Fragment yang lolos semua test ditulis ke framebuffer")
        print("   - Hasil akhir ditampilkan di layar")
        print()
    
    @staticmethod
    def explain_full_pipeline():
        """
        Menjelaskan dan mendemonstrasikan seluruh pipeline.
        """
        print("\n")
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 15 + "GRAPHICS PIPELINE" + " " * 25 + "║")
        print("╚" + "═" * 58 + "╝")
        print()
        
        # Tahap 1: Vertex Specification
        vertices = PipelineVisualizer.explain_vertex_specification()
        input("\nTekan Enter untuk lanjut ke tahap berikutnya...")
        
        # Tahap 2: Vertex Processing
        transformed_vertices = PipelineVisualizer.explain_vertex_processing(vertices)
        input("\nTekan Enter untuk lanjut ke tahap berikutnya...")
        
        # Tahap 3: Primitive Assembly
        PipelineVisualizer.explain_primitive_assembly()
        input("\nTekan Enter untuk lanjut ke tahap berikutnya...")
        
        # Tahap 4: Rasterization
        PipelineVisualizer.explain_rasterization()
        input("\nTekan Enter untuk lanjut ke tahap berikutnya...")
        
        # Tahap 5: Fragment Processing
        PipelineVisualizer.explain_fragment_processing()
        input("\nTekan Enter untuk lanjut ke tahap berikutnya...")
        
        # Tahap 6: Output Operations
        PipelineVisualizer.explain_output_operations()
        
        print("=" * 60)
        print("PIPELINE SELESAI!")
        print("=" * 60)
        print("Vertex data telah melewati semua tahapan dan")
        print("sekarang muncul sebagai pixel di layar Anda!")
        print()


class ShaderPipelineExplainer:
    """
    Menjelaskan peran Vertex Shader dan Fragment Shader dalam pipeline.
    """
    
    @staticmethod
    def explain_vertex_shader():
        """
        Menjelaskan Vertex Shader.
        """
        print("=" * 60)
        print("VERTEX SHADER")
        print("=" * 60)
        print()
        print("Vertex Shader adalah program yang berjalan sekali per vertex.")
        print()
        print("TANGGUNG JAWAB:")
        print("1. Transformasi posisi vertex (MVP transformation)")
        print("2. Perhitungan lighting per-vertex (optional)")
        print("3. Meneruskan atribut ke fragment shader")
        print()
        print("INPUT:")
        print("- Attribute: posisi, normal, color, texCoords (per-vertex)")
        print("- Uniform: MVP matrices, lighting info (sama untuk semua vertex)")
        print()
        print("OUTPUT:")
        print("- gl_Position: posisi vertex di clip space (WAJIB)")
        print("- Varying variables: data yang akan di-interpolasi")
        print()
        print("CONTOH VERTEX SHADER:")
        print("-" * 60)
        vertex_shader_code = """
attribute vec3 vertexPosition;
attribute vec3 vertexColor;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;

varying vec3 color;

void main() {
    // Transformasi posisi
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
    
    // Teruskan warna ke fragment shader
    color = vertexColor;
}
        """
        print(vertex_shader_code)
        print("-" * 60)
        print()
    
    @staticmethod
    def explain_fragment_shader():
        """
        Menjelaskan Fragment Shader.
        """
        print("=" * 60)
        print("FRAGMENT SHADER")
        print("=" * 60)
        print()
        print("Fragment Shader adalah program yang berjalan sekali per fragment.")
        print("(Fragment = pixel candidate)")
        print()
        print("TANGGUNG JAWAB:")
        print("1. Menghitung warna final fragment")
        print("2. Texture sampling")
        print("3. Perhitungan lighting (Phong, Lambert)")
        print("4. Special effects")
        print()
        print("INPUT:")
        print("- Varying variables: data yang di-interpolasi dari vertices")
        print("- Uniform: textures, lighting info, material properties")
        print()
        print("OUTPUT:")
        print("- gl_FragColor: warna RGBA fragment (WAJIB)")
        print()
        print("CONTOH FRAGMENT SHADER:")
        print("-" * 60)
        fragment_shader_code = """
varying vec3 color;
uniform float brightness;

void main() {
    // Hitung warna final
    vec3 finalColor = color * brightness;
    
    // Output warna
    gl_FragColor = vec4(finalColor, 1.0);
}
        """
        print(fragment_shader_code)
        print("-" * 60)
        print()
    
    @staticmethod
    def explain_shader_pipeline():
        """
        Menjelaskan hubungan vertex shader dan fragment shader.
        """
        print("\n")
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 18 + "SHADER PIPELINE" + " " * 25 + "║")
        print("╚" + "═" * 58 + "╝")
        print()
        
        ShaderPipelineExplainer.explain_vertex_shader()
        input("Tekan Enter untuk lanjut...")
        
        ShaderPipelineExplainer.explain_fragment_shader()
        
        print("=" * 60)
        print("ALUR DATA DALAM SHADER PIPELINE:")
        print("=" * 60)
        print()
        print("1. Vertex data (attributes) -> VERTEX SHADER")
        print("2. Vertex shader mentransformasi posisi -> gl_Position")
        print("3. Vertex shader meneruskan data -> varying variables")
        print("4. Rasterizer meng-interpolasi varying variables")
        print("5. Interpolated data -> FRAGMENT SHADER")
        print("6. Fragment shader menghitung warna -> gl_FragColor")
        print("7. gl_FragColor -> Framebuffer (layar)")
        print()
