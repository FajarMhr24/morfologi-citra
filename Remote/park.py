import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. Baca citra satelit
sat = cv2.imread('31.jpg')

# Jaga-jaga kalau gambar nggak ketemu
if sat is None:
    print("Gambar '31.jpg' gak ketemu nih! Cek lagi lokasinya ya.")
    exit()

# 2. Konversi ke HSV
hsv = cv2.cvtColor(sat, cv2.COLOR_BGR2HSV)

# 3. Masker warna vegetasi (hijau di HSV)
lo_green = np.array([35, 40, 40])
hi_green = np.array([85, 255, 255])
veg_mask = cv2.inRange(hsv, lo_green, hi_green)

# 4. Opening + Closing (Bersihkan mask vegetasi)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
# Opening dulu
opened = cv2.morphologyEx(veg_mask, cv2.MORPH_OPEN, kernel)
# Baru Closing
veg_clean = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

# 5. Gradient morfologi: temukan tepi vegetasi
boundary = cv2.morphologyEx(veg_clean, cv2.MORPH_GRADIENT, kernel)

# 6. Visualisasi peta (Overlay warna pada citra asli)
overlay = sat.copy()
# Warna hijau (BGR: 0, 200, 0) untuk area vegetasi
overlay[veg_clean > 0] = [0, 200, 0]
# Warna kuning (BGR: 0, 255, 255) untuk tepi/batas vegetasi
overlay[boundary > 0] = [0, 255, 255]

# Gabungin overlay dengan citra asli biar agak transparan
result = cv2.addWeighted(sat, 0.6, overlay, 0.4, 0)

# Simpan hasil akhir (sesuai instruksi asli)
cv2.imwrite('vegetation_map.jpg', result)

# ==========================================
# TAMPILIN 6 POP-UP SESUAI LANGKAH TUGAS
# ==========================================
cv2.imshow('1. Baca Citra Satelit', sat)
cv2.imshow('2. Konversi ke HSV', hsv)
cv2.imshow('3. Masker Vegetasi (Mentah)', veg_mask)
cv2.imshow('4. Opening + Closing (Bersih)', veg_clean)
cv2.imshow('5. Gradient Morfologi (Batas)', boundary)
cv2.imshow('6. Visualisasi Peta', result)

# Tunggu pencetan keyboard buat nutup
cv2.waitKey(0)
cv2.destroyAllWindows()
