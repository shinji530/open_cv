#sobel_edge_detect.py

import cv2
import numpy as np
import sys

def calculate(color_img):
    arr = [[0 for j in range(color_img.shape[1])] for i in range(color_img.shape[0])]
    under, over = float("inf"), float("-inf")
    total = 0

    for x in range(color_img.shape[0]):
        for y in range(color_img.shape[1]):
            cal_x, cal_y = 0.0, 0.0

            x_start, x_end = max(0, x - 1), min(color_img.shape[0], x + 2)
            y_start, y_end = max(0, y - 1), min(color_img.shape[1], y + 2)
            part_img = color_img[x_start : x_end, y_start : y_end, 0]
            if part_img.shape != (3, 3):
                part_img = np.pad(part_img, ((3 - part_img.shape[0], 0), (3 - part_img.shape[1], 0)), mode='constant', constant_values=0)
            cal_x = (part_img * edge_mask_x).sum()
            cal_y = (part_img * edge_mask_x).sum()

            arr[x][y] = abs(cal_x) + abs(cal_y)
            total += arr[x][y]
            under = min(under, arr[x][y])
            over = max(over, arr[x][y])
            
    total = total / (color_img.shape[0] * color_img.shape[1])

    for x in range(color_img.shape[0]):
        for y in range(color_img.shape[1]):
            if arr[x][y] < total:
                normalize = 0
            else:
                normalize = 255
            img[x, y] = (normalize, normalize, normalize)

def erode(image, kernel_size):
    height = image.shape[0]
    width = image.shape[1]
    result = [[0 for j in range(width)] for i in range(height)]

    # Iterate over the image
    for i in range(kernel_size // 2, height - kernel_size // 2):
        for j in range(kernel_size // 2, width - kernel_size // 2):
            flag = True
            for x in range(-(kernel_size // 2), kernel_size // 2 + 1):
                for y in range(-(kernel_size // 2), kernel_size // 2 + 1):
                    if image[i + x][j + y][0] != 255:
                        flag = False
                        break
            if flag:
                result[i][j] = 255
            else:
                result[i][j] = 0
    return result

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sobel_edge_detect.py <image_path>")
        # sys.exit(1)

    imgPath = sys.argv[1]
        
    # imgPath = 'hihihi.jpeg'
    original = cv2.imread(imgPath)
    img = cv2.imread(imgPath)
    red_img = cv2.imread(imgPath)
    blue_img = cv2.imread(imgPath)
    green_img = cv2.imread(imgPath)

    edge_mask_x = np.array([[-1,	0,		1],
                [-2, 	0, 	    2],
                [-1, 	0, 	    1]])
    edge_mask_y = np.array([[1,	2,		1],
                [0, 	0, 	    0],
                [-1, 	-2,     -1]])

    print("Get each color image")
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            (b, g, r) = img[x, y]
            gray = (int(b) + int(g) + int(r)) / 3
            img[x, y] = (gray, gray, gray)
            red_img[x, y] = (r, r, r)
            blue_img[x, y] = (b, b, b)
            green_img[x, y] = (g, g, g)
    
    print("Detect edge with each color image and combine in one image")
    calculate(red_img)
    calculate(blue_img)
    calculate(green_img)

    print("Erode image")
    eroded_image = erode(img, 3)

    print("Apply edge in original image")
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if eroded_image[x][y] == 255:
                original[x, y] = (0, 0, 0)

    # 이미지를 윤곽선과 함께 저장
    output_path = imgPath.replace('.', '_edge.')
    cv2.imwrite(output_path, original)
    print(f"The outlined image has been saved: {output_path}")

    # cv2.imshow('image', original)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    