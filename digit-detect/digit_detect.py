import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image

# 设置Tesseract的路径，如果安装后不在系统环境变量中，则需要设置
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

# 读取图片


# 加载图像文件
image_path = 'digits.png'
image = cv2.imread(image_path)
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
_, threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
threshold_image = np.abs(255-threshold_image)
# kernel = np.ones((1,1), np.uint8)
# cleaned_img = cv2.morphologyEx(threshold_image, cv2.MORPH_OPEN, kernel)
plt.imshow(threshold_image, cmap='gray')
plt.axis('off')  # 不显示坐标轴
plt.show()
# 使用Tesseract识别图片中的数字
number = pytesseract.image_to_string(threshold_image, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

print(number)
