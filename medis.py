import cv2
import numpy as np
from skimage import measure

# 1. Baca citra
img = cv2.imread('bloodImage_00010.jpg')

# 2. Grayscale + Gaussian Blur
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# 3. Threshold Otsu → biner
_, binary = cv2.threshold(
    blur, 0, 255,
    cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)

# Elemen penstruktur elips
kernel = cv2.getStructuringElement(
    cv2.MORPH_ELLIPSE, (7, 7)
)

# 4. Opening: hapus noise kecil
opened = cv2.morphologyEx(
    binary, cv2.MORPH_OPEN, kernel, iterations=2
)

# 5. Closing: tutup celah dalam sel
cleaned = cv2.morphologyEx(
    opened, cv2.MORPH_CLOSE, kernel, iterations=2
)

# 6. Hitung dan label setiap sel (Visualisasi)
labels = measure.label(cleaned)
regions = measure.regionprops(labels)
count = len([r for r in regions if r.area > 500])
print(f'Jumlah sel terdeteksi: {count}')

output_img = img.copy()
for r in regions:
    if r.area > 500:
        minr, minc, maxr, maxc = r.bbox
        # Pakai warna hijau (BGR: 0, 255, 0) biar lebih kontras
        cv2.rectangle(output_img, (minc, minr), (maxc, maxr), (0, 255, 0), 2)

# ==========================================
# TAMPILIN 6 POP-UP SESUAI LANGKAH TUGAS
# ==========================================
cv2.imshow('1. Baca Citra', img)
cv2.imshow('2. Grayscale + Blur', blur)
cv2.imshow('3. Threshold Otsu', binary)
cv2.imshow('4. Opening (Hapus Noise)', opened)
cv2.imshow('5. Closing (Tutup Celah)', cleaned)
cv2.imshow('6. Labeling & Counting', output_img)

# Tunggu pencetan keyboard buat nutup
cv2.waitKey(0)
cv2.destroyAllWindows()
