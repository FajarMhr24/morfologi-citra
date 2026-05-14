import cv2
import numpy as np
from scipy import ndimage

# 1. Citra input & Binarisasi
img = cv2.imread('32.jpg', 0)

if img is None:
    print("Gambar '32.jpg' gak ketemu nih! Cek lagi ya.")
    exit()

_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# ── 5. Isi lubang dalam objek ──
def fill_holes(binary_img):
    inv = cv2.bitwise_not(binary_img)
    flood = inv.copy()
    # Mask untuk floodFill harus lebih besar 2 piksel dari gambar asli
    mask = np.zeros((inv.shape[0]+2, inv.shape[1]+2), np.uint8)
    cv2.floodFill(flood, mask, (0,0), 255)
    flood_inv = cv2.bitwise_not(flood)
    return cv2.bitwise_or(binary_img, flood_inv)

# ── Pisahkan objek (Watershed) ──
filled = fill_holes(binary)

# 3. Dilasi terkontrol (Mencari area background yang pasti)
kernel = np.ones((3,3), np.uint8)
sure_bg = cv2.dilate(filled, kernel, iterations=3)

# 2 & 4. Tentukan marker (Mencari area foreground/objek yang pasti)
dist = cv2.distanceTransform(filled, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)
sure_fg = sure_fg.astype(np.uint8)

# Mencari area abu-abu (unknown) yang tumpang tindih
unknown = cv2.subtract(sure_bg, sure_fg)

# Memberi label marker untuk tiap objek
_, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0

# 6. Watershed morfologi
# Watershed butuh gambar berwarna (BGR), jadi kita konversi dulu
img_color = cv2.cvtColor(filled, cv2.COLOR_GRAY2BGR)
cv2.watershed(img_color, markers)

# Kasih warna merah (BGR: 0, 0, 255) di garis batas objek yang saling nempel
img_color[markers == -1] = [0, 0, 255]

# Normalisasi visual buat pop-up Distance Transform biar kelihatan jelas
dist_visual = cv2.normalize(dist, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# ==========================================
# TAMPILIN 6 POP-UP SESUAI LANGKAH TUGAS
# ==========================================
cv2.imshow('1. Citra Biner Input', binary)
cv2.imshow('2. Isi Lubang (Reconstruct)', filled)
cv2.imshow('3. Sure Background', sure_bg)
cv2.imshow('4. Distance Transform', dist_visual)
cv2.imshow('5. Sure Foreground (Marker)', sure_fg)
cv2.imshow('6. Hasil Watershed Morfologi', img_color)

# Tunggu pencetan keyboard buat nutup
cv2.waitKey(0)
cv2.destroyAllWindows()
