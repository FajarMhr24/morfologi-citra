import cv2
import numpy as np
from skimage.morphology import skeletonize

# 1. Baca citra teks (0 = baca sebagai grayscale)
img = cv2.imread('download (29).jpg', 0)

if img is None:
    print("Gambar 'download.jpg' gak ketemu nih! Cek lagi nama dan letak foldernya.")
    exit()

# 2. Binarisasi dengan Otsu
_, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# --- CARA 1: Pakai library skimage ---
binary_bool = binary / 255
skeleton = skeletonize(binary_bool)
skel_img = (skeleton * 255).astype(np.uint8) # Ini buat nampilin langkah 4

# --- CARA 2: Pendekatan manual dengan OpenCV ---
def cv_skeleton(img_bin):
    img_temp = img_bin.copy()
    skel = np.zeros_like(img_temp)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    while True:
        eroded = cv2.erode(img_temp, kernel)
        opened = cv2.dilate(eroded, kernel)
        temp = cv2.subtract(img_temp, opened)
        skel = cv2.bitwise_or(skel, temp)
        img_temp = eroded.copy()
        if cv2.countNonZero(img_temp) == 0:
            break
    return skel

hasil_manual = cv_skeleton(binary) # Ini buat nampilin langkah 3

# --- 5. Analisis Konektivitas (Tambahan biar pas 6 langkah) ---
# Ngitung dan misahin tiap huruf/garis yang gak saling nempel
num_labels, labels = cv2.connectedComponents(hasil_manual)
# Bikin warna-warni biar kelihatan bedanya tiap komponen (huruf)
label_hue = np.uint8(179 * labels / np.max(labels))
blank_ch = 255 * np.ones_like(label_hue)
konektivitas_img = cv2.merge([label_hue, blank_ch, blank_ch])
konektivitas_img = cv2.cvtColor(konektivitas_img, cv2.COLOR_HSV2BGR)
konektivitas_img[label_hue == 0] = 0 # Balikin background jadi hitam

# --- 6. Simpan Hasil ---
cv2.imwrite('skeleton.png', hasil_manual)
# Kita baca lagi file yang barusan disimpen buat bukti di layar
hasil_simpan = cv2.imread('skeleton.png')

# ==========================================
# TAMPILIN 6 POP-UP SESUAI LANGKAH TUGAS
# ==========================================
cv2.imshow('1. Baca Citra Teks', img)
cv2.imshow('2. Binarisasi Otsu', binary)
cv2.imshow('3. Thinning Iteratif (OpenCV)', hasil_manual)
cv2.imshow('4. Skeletonization (Skimage)', skel_img)
cv2.imshow('5. Analisis Konektivitas', konektivitas_img)
cv2.imshow('6. Simpan Hasil (File skeleton.png)', hasil_simpan)

cv2.waitKey(0)
cv2.destroyAllWindows()
