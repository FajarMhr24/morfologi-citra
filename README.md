# medis

Library `skimage.measure` digunakan untuk mengekstraksi properti spasial dan menganalisis objek pada citra yang telah disegmentasi menjadi biner (hitam-putih). Dalam proyek deteksi sel ini, ada dua fungsi utama yang digunakan:

### 1.`measure.label()` (Connected-Component Labeling)
Fungsi ini bertugas memindai citra biner dan memberikan label (nomor urut unik) pada setiap kumpulan piksel putih yang saling terhubung. Proses ini mengubah sekumpulan piksel putih biasa menjadi entitas atau "objek sel" yang terpisah dan dapat dikenali oleh sistem secara individual.

### 2. `measure.regionprops()` (Ekstraksi Properti Objek)
Setelah setiap sel memiliki label, fungsi ini mengekstrak informasi dan karakteristik fisik dari setiap objek tersebut. Pada kode ini, properti yang digunakan meliputi:
  * `area`: Mengukur luas objek berdasarkan jumlah piksel. Properti ini digunakan sebagai thresholding ukuran (seperti kondisi `if r.area > 500`). Objek dengan luas di bawah 500 piksel akan diabaikan karena dianggap sebagai noise atau kotoran, bukan sel darah.
  * `bbox` (Bounding Box): Mengambil titik koordinat ekstrem (batas atas, bawah, kiri, dan kanan) dari setiap sel. Koordinat ini digunakan oleh OpenCV untuk menggambar kotak penanda pembatas di sekeliling sel pada citra hasil akhir.

# Industry

### Top Hat & Black Hat

### Top-Hat Transform (Sering disebut White Top-Hat):

  * Fungsi Utama: Mendeteksi atau menonjolkan objek/cacat berukuran kecil yang lebih terang daripada area sekitarnya.

  * Cara Kerja Matematis: Citra asli dikurangi dengan citra hasil operasi Opening.

  * Kapan Dipakainya?: Dipakai kalau lu mau mendeteksi goresan yang memantulkan cahaya (putih/terang) di atas permukaan plat besi yang warnanya gelap, atau mencari debu putih di atas kain berwarna gelap.

### Black-Hat Transform (Sering disebut Bottom-Hat):

  * Fungsi Utama: Mendeteksi atau menonjolkan objek/cacat berukuran kecil yang lebih gelap daripada area sekitarnya.

  * Cara Kerja Matematis: Citra hasil operasi Closing dikurangi dengan citra asli.

  * Kapan Dipakainya?: Dipakai kalau lu mau mendeteksi noda hitam, lubang, atau titik gosong di atas permukaan produk yang warnanya putih atau terang (kayak keramik atau kertas).

# ORC/Dokumen

### 3. Algoritma zhang-suen
  * Cara Kerja: Bekerja secara paralel dengan membagi satu kali iterasi menjadi dua sub-tahap (mengecek piksel tetangga di arah genap dan ganjil secara bergantian).
  * Kelebihan: Kecepatan komputasinya sangat tinggi dan efisien, sehingga sangat cocok untuk pemrosesan citra real-time atau data teks yang masif.
  * Kekurangan: Kadang tidak menghasilkan kerangka yang benar-benar sempurna setebal 1 piksel. Pada beberapa pola diagonal atau sudut siku-siku, hasilnya bisa menyisakan garis dengan ketebalan 2 piksel atau efek tangga (staircase effect).

### 3.1 Algoritma Hilditch
  * Cara Kerja: Mengevaluasi piksel berdasarkan sekumpulan aturan ketat (biasanya ada 6 kondisi) dengan melihat jendela 3x3 piksel sekitarnya untuk memastikan penghapusan piksel tidak merusak konektivitas atau menghilangkan titik ujung (endpoint).
  * Kelebihan: Kualitas skeleton yang dihasilkan lebih bersih, mulus, dan terjamin konsisten menjadi garis tunggal setebal persis 1 piksel. Sangat ideal untuk akurasi tinggi pada Optical Character Recognition (OCR).
  * Kekurangan: Proses komputasinya lebih berat dan lambat dibandingkan Zhang-Suen karena pengecekan kondisionalnya yang lebih kompleks pada setiap piksel.

# Remote sensing
NDVI (Normalized Difference Vegetation Index) adalah indeks yang sangat akurat untuk mendeteksi tingkat kehijauan atau kesehatan tanaman dengan memanfaatkan pantulan cahaya Near-Infrared (NIR) dan warna Merah (Red) dari citra satelit.

Untuk menggabungkan kekuatan NDVI dengan operasi morfologi citra, alur kerja komputasinya adalah sebagai berikut:

### 1. Ekstraksi Nilai NDVI
Pertama, citra satelit multispektral (yang memiliki band NIR dan Red) dihitung menggunakan rumus NDVI. Hasilnya adalah sebuah peta piksel dengan rentang nilai kontinu antara -1.0 hingga +1.0. (Semakin mendekati +1, semakin lebat/sehat vegetasinya).

### 2. Binarisasi (Thresholding)
Operasi morfologi bekerja optimal pada citra biner (hitam-putih). Oleh karena itu, peta NDVI tadi harus diubah menjadi biner dengan menentukan nilai ambang batas (threshold).
  * Contoh: Jika nilai NDVI > 0.3, maka ubah piksel menjadi Putih (Vegetasi). Jika di bawah itu, ubah menjadi Hitam (Bukan Vegetasi).

### 3. Penerapan Operasi Morfologi
Setelah mendapatkan masking atau citra biner vegetasi dari hasil NDVI, barulah operasi morfologi diaplikasikan untuk menyempurnakan bentuk area vegetasi tersebut:
  * Opening: Digunakan untuk menghapus noise atau titik-titik putih kecil di luar area vegetasi utama (misalnya rumput liar kecil di tengah jalan aspal yang ikut terdeteksi oleh NDVI).
  * Closing: Digunakan untuk menutup lubang-lubang hitam kecil di dalam area putih (misalnya area hutan yang lebat, tetapi ada bayangan gelap antar kanopi pohon yang tidak sengaja terdeteksi sebagai non-vegetasi oleh NDVI).

# Analitik

### Cara Menggunakan Algoritma Watershed untuk Memisahkan Sel yang Saling Menyentuh

Algoritma Watershed mengibaratkan sebuah citra (gambar) seperti peta topografi 3D, di mana piksel terang dianggap sebagai "puncak bukit" dan piksel gelap sebagai "lembah". Konsep utamanya adalah "mengairi" lembah tersebut dari titik-titik pusat objek (marker), dan ketika air dari dua sumber sel yang berbeda bertemu, algoritma akan otomatis membangun "bendungan" alias garis batas pembatas.

Alur kerjanya untuk memisahkan sel yang menyentuh adalah sebagai berikut:

### 1. Mencari Sure Background (Latar Belakang Pasti): Citra biner sel diperbesar sedikit menggunakan operasi morfologi Dilasi. Area terluar dari hasil dilasi ini dipastikan adalah background atau latar belakang yang sebenarnya.

### 2.Mencari Sure Foreground (Objek Pasti) dengan Distance Transform: Ini adalah kunci utama pemisahannya. Fungsi distance transform menghitung jarak setiap piksel di dalam sel menuju tepi sel terdekat. Bagian paling tengah (inti sel) akan memiliki nilai paling tinggi. Setelah di-threshold, kita akan mendapatkan titik-titik inti (marker) dari masing-masing sel yang sudah terpisah satu sama lain, meskipun bagian kulit luarnya saling menyentuh.

### 3. Menentukan Area Unknown (Area Abu-abu): Area sisa di antara sure background dan sure foreground diklasifikasikan sebagai area unknown (tidak pasti). Sistem belum tahu apakah area ini milik sel A, sel B, atau background.

### 4. Eksekusi Watershed: Algoritma Watershed kemudian dijalankan dengan patokan marker inti sel tadi. Algoritma akan mengekspansi area dari inti sel menuju area unknown. Tepat di titik pertemuan antara sel yang satu dengan sel lainnya, Watershed akan membentuk garis batas (batas pemisah) yang tegas.
