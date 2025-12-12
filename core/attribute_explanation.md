# Penjelasan Detail: core/attribute.py

File ini adalah kelas pembantu (helper class) yang menangani pengelolaan **Vertex Buffer Object (VBO)**. Tugas utamanya adalah menyimpan data (seperti posisi titik atau warna) dan mengirimkannya ke kartu grafis (GPU).

## Import Library
```python
from OpenGL.GL import *
import numpy as np 
```
*   `from OpenGL.GL import *`: Mengimpor semua fungsi OpenGL agar bisa memanggil perintah seperti `glGenBuffers`, `glBindBuffer`, dll.
*   `import numpy as np`: Mengimpor library NumPy. Ini **sangat penting** karena OpenGL membutuhkan data dalam format array yang padat dan efisien, bukan list Python biasa.

## Definisi Kelas
```python
class Attribute(object):
```
*   Mendefinisikan kelas `Attribute`. Setiap kali kita ingin mengirim data baru ke GPU (misalnya data posisi segitiga), kita akan membuat objek baru dari kelas ini.

### Fungsi `__init__` (Konstruktor)
```python
    def __init__(self, dataType, data):
        self.dataType = dataType
        self.data = data
        self.bufferRef = glGenBuffers(1)
        self.uploadData()
```
*   `def __init__(...)`: Fungsi yang dijalankan otomatis saat objek dibuat.
*   `self.dataType = dataType`: Menyimpan jenis data, misalnya `"vec3"` (untuk posisi 3D) atau `"vec4"` (untuk warna RGBA).
*   `self.data = data`: Menyimpan data mentah (biasanya berupa List Python).
*   `self.bufferRef = glGenBuffers(1)`: Meminta OpenGL membuatkan **1 buah Buffer kosong**. OpenGL memberikan ID unik (integer) yang disimpan di `self.bufferRef`. Ini seperti memesan loker kosong di GPU.
*   `self.uploadData()`: Langsung memanggil fungsi untuk mengisi loker tersebut dengan data.

### Fungsi `uploadData`
```python
    def uploadData(self):
        data = np.array(self.data).astype(np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)
```
*   `data = np.array(self.data).astype(np.float32)`:
    *   Mengubah list Python menjadi **NumPy Array**.
    *   `.astype(np.float32)`: Memaksa tipe data menjadi **Float 32-bit**. Ini wajib karena GPU standar bekerja dengan float 4-byte, sedangkan Python defaultnya 8-byte (float64).
*   `glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)`: Mengaktifkan buffer (loker) yang tadi kita buat. Semua perintah buffer selanjutnya akan tertuju ke buffer ini.
*   `glBufferData(...)`: Mengirim data sebenarnya ke GPU.
    *   `data.ravel()`: Meratakan array menjadi 1 dimensi (gepeng).
    *   `GL_STATIC_DRAW`: Memberi tahu GPU bahwa data ini tidak akan sering berubah (statis), agar GPU bisa menyimpannya di memori yang paling optimal.

### Fungsi `associateVariable`
```python
    def associateVariable(self, programRef, variabelName):
```
*   Fungsi ini menghubungkan data di buffer dengan variabel di dalam kode Shader (GLSL).

```python
        variabelRef = glGetAttribLocation(programRef, variabelName)
```
*   Mencari ID lokasi variabel di shader berdasarkan namanya (misal: mencari lokasi variabel bernama `"position"`).

```python
        if variabelRef == -1:
            return 
```
*   Jika hasilnya `-1`, berarti variabel tersebut tidak ditemukan di shader. Fungsi langsung berhenti (return) agar tidak error.

```python
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)
```
*   **Penting:** Mengaktifkan kembali buffer kita. Kita harus memastikan buffer yang benar sedang aktif sebelum mengatur pointer di baris berikutnya.

```python
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
```
*   Blok percabangan ini menentukan cara GPU membaca data berdasarkan `dataType`.
*   `glVertexAttribPointer(...)`:
    *   Argumen 2 (Angka 1, 2, 3, 4): Jumlah komponen per data (misal `vec3` butuh 3 angka: x, y, z).
    *   Argumen 3 (`GL_FLOAT`): Tipe data setiap komponen.
    *   Argumen 4 (`False`): Apakah data perlu dinormalisasi? Biasanya False untuk koordinat posisi.
    *   Argumen 5 (`0`): Stride (jarak antar data). 0 berarti data rapat (tightly packed).
    *   Argumen 6 (`None`): Offset awal. None berarti mulai dari awal buffer.

```python
        else:
            raise Exception("Attribute "+variabelName+" has unknown type "+self.dataType)
```
*   Jika tipe data tidak dikenali, lemparkan Error.

```python
        glEnableVertexAttribArray(variabelRef)
```
*   Mengaktifkan slot atribut tersebut di GPU agar data bisa mengalir masuk ke shader saat proses rendering.
