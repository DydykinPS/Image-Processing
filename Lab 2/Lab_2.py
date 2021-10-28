import cv2
import numpy as np
from matplotlib import pyplot as plt

img1 = cv2.imread('1.jpg')
img2 = cv2.imread('2.jpg')
img3 = cv2.imread('3.jpg')
img4 = cv2.imread('4.jpg')
img5 = cv2.imread('5.jpg')
img6 = cv2.imread('6.jpg')
img7 = cv2.imread('7.jpg')
img8 = cv2.imread('8.jpg')
img9 = cv2.imread('9.jpg')
img10 = cv2.imread('10.jpg')
img11 = cv2.imread('11.jpg')
img12 = cv2.imread('12.jpg')


def NonLocalMeans(img):
    b, g, r = cv2.split(img)
    rgb_img = cv2.merge([r, g, b])
    
    #Denoisng 
    dst = cv2.fastNlMeansDenoisingColored(img, None, 500, 4, 7, 21)
    
    b, g, r = cv2.split(dst)  #get b,g,r
    rgb_dst = cv2.merge([r, g, b])  #switch it to rgb
    
    return rgb_dst

def BilaterialFilter(img):
    b, g, r = cv2.split(img)
    rgb_img = cv2.merge([r, g, b])
    bilateral = cv2.bilateralFilter(img, 4, 300, 100)
    return bilateral
    
def CalcOfDamageAndNonDamage(img):
    
    image = img
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    image_erode = cv2.erode(image, kernel)
    
    hsv_img = cv2.cvtColor(image_erode, cv2.COLOR_BGR2HSV)        
    
    markers = np.zeros((image.shape[0], image.shape[1]), dtype="int32")
    markers[90: 120, 90: 140] = 255
    markers[236: 255, 0: 20] = 1
    markers[0: 20, 0: 20] = 1
    markers[0: 20, 236: 255] = 1
    markers[236: 255, 236: 255] = 1
    

    leafs_area_bgr = cv2.watershed(image_erode, markers)
    healthy_part = cv2.inRange(hsv_img, (36, 25, 25), (86, 255, 255))
    l1 = cv2.inRange(hsv_img, (0, 0, 0), (360, 255, 50))
    l2 = cv2.add(cv2.bitwise_not(l1), healthy_part)
    leafs_area_bgr = cv2.convertScaleAbs(markers)
    list = cv2.bitwise_and(leafs_area_bgr, l2)
  
    ill_part = list - healthy_part
    
    mask = np.zeros_like(image, np.uint8)
    mask[leafs_area_bgr > 1] = (255, 0, 255)
    mask[ill_part > 1] = (0, 0, 255)
    
    return mask



def result(img):
    #изначальное изображение
    plt.subplot(221), plt.imshow(img), plt.title("Original")
    plt.xticks([]), plt.yticks([])
    #Удаление шума методом Non-Local Means 
    im = NonLocalMeans(img)
    im2=CalcOfDamageAndNonDamage(im)
    plt.subplot(222),
    plt.imshow(im2),
    plt.title("Non-Local Means")
    plt.xticks([]), plt.yticks([])
    #Билатериальный фильтр
    im1=BilaterialFilter(img)
    im2=CalcOfDamageAndNonDamage(im1)
    plt.subplot(223), 
    plt.imshow(im2),
    plt.title("Bilateral Filter")
    #Watershed
    im2=CalcOfDamageAndNonDamage(img)
    plt.subplot(224), 
    plt.imshow(im2),
    plt.title("Only Watershed")
    plt.show()
    
result(img1)
result(img2)
result(img3)
result(img4)
result(img5)
result(img6)
result(img7)
result(img8)
result(img9)
result(img10)
result(img11)
result(img12)