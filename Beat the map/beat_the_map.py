import cv2
import numpy as np
import random

extracted=""
first_hint_img = cv2.imread("first_hint.bmp", cv2.IMREAD_COLOR)
second_hint_img = cv2.imread("second_hint.bmp", cv2.IMREAD_COLOR)
challange_img = cv2.imread("challenge.bmp", cv2.IMREAD_COLOR)

# Hint 1 - Solution
# Using two blank images 
def decrypt(img):
    # Encrypted image
    width = img.shape[0]
    height = img.shape[1]

    # img1 and img2 are two blank images
    img1 = np.zeros((width, height, 3), np.uint8)
    img2 = np.zeros((width, height, 3), np.uint8)

    for i in range(width):
        for j in range(height):
            for l in range(3):
                v1 = format(img[i][j][l], '08b')
                v2 = v1[:4] + chr(random.randint(0, 1) + 48) * 4
                v3 = v1[4:] + chr(random.randint(0, 1) + 48) * 4

                # Appending data to img1 and img2
                img1[i][j][l] = int(v2, 2)
                img2[i][j][l] = int(v3, 2)

    # These are two images produced from
    # the encrypted image
    cv2.imwrite('first_hint_sol_1.png', img1)
    cv2.imwrite('first_hint_sol_2.png', img2)

decrypt(first_hint_img)


# Hint 2 - solution
# Changing every odd pixel to 0 and even to 255
for i in range(512):
    for j in range(512):
        if second_hint_img[i][j][0]%2==0:
            second_hint_img[i][j]=[255,255,255]
        else:
            second_hint_img[i][j] = [0,0,0]

# Saving result
cv2.imwrite('second_hint_sol.png',second_hint_img)


# Challange - solution 
# Lsbit over triangular series
for i in range(512**2):
    n = (i ** 2 + i) // 2
    if n >= 512 ** 2:
        break
    pixel=challange_img[511-n//512][n%512]
    extracted += bin(pixel[0])[-1]

chars = []
for i in range(int(len(extracted) / 8)):
    byte = extracted[i * 8:(i + 1) * 8]
    chars.append(chr(int(byte, 2)))

print("".join(chars))



