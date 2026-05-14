import cv2
import numpy as np

# 1. Baca citra produk
img = cv2.imread('apalah.jpg')

# Jaga-jaga kalau gambar nggak ketemu biar nggak langsung close/error
if img is None:
    print("Waduh, gambar 'scratch.jpg' belum ada di folder nih!")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. CLAHE: tingkatkan kontras lokal
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
enhanced = clahe.apply(gray)

# 3. Top-Hat: isolasi detail kecil (cacat)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
tophat = cv2.morphologyEx(enhanced, cv2.MORPH_TOPHAT, kernel)

# 4. Threshold adaptif
_, thresh = cv2.threshold(tophat, 30, 255, cv2.THRESH_BINARY)

# 5. Dilasi untuk perjelas area cacat
k2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
dilated = cv2.dilate(thresh, k2, iterations=2)

# 6. Bounding box cacat
contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
result = img.copy()

# ==========================================
# TAMBAHAN: Bikin hitungan buat jumlah cacat
# ==========================================
jumlah_cacat = 0

for c in contours:
    if cv2.contourArea(c) > 50:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(result, (x,y), (x+w, y+h), (0,0,255), 2)
        jumlah_cacat += 1  # Hitungannya nambah 1 setiap nemu lecet

# Print jumlah akhir ke terminal
print(f"Total titik cacat (lecet) terdeteksi: {jumlah_cacat}")

# ==========================================
# TAMPILIN POP-UP SESUAI LANGKAH TUGAS
# ==========================================
cv2.imshow('1. Gambar Asli', img)
cv2.imshow('2. Hasil Top-Hat', tophat)
cv2.imshow('3. Hasil Deteksi Cacat', result)
cv2.imshow('4. Threshold + Dilasi', dilated)
cv2.imshow('5. Hasil Deteksi Cacat', result)

cv2.waitKey(0)
cv2.destroyAllWindows() 
