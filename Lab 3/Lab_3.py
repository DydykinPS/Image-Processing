import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import glob


def DFFTnp(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    return fshift


def reverseDFFTnp(dfft):
    f_ishift = np.fft.ifftshift(dfft)
    reverse_image = np.fft.ifft2(f_ishift)
    return reverse_image

def Gauss(img):
    ksize = 10
    kernel = np.zeros(img.shape)

    blur = cv.getGaussianKernel(ksize, -1)
    blur = np.matmul(blur, np.transpose(blur))
    kernel[0:ksize, 0:ksize] = blur

    fkshift = DFFTnp(kernel)
    mult = np.multiply(fshift, fkshift)
    
    reverse_image = reverseDFFTnp(mult)
    return reverse_image
    

folder_path = r"C:\stripes/"
images = glob.glob(folder_path + '*.png')
for image in images:
    img = np.float32(cv.imread(image, 0))
    fshift = DFFTnp(img)

    magnitude_spectrum = 20*np.log(np.abs(fshift))
    plt.subplot(121), plt.title('Magnitude Spectrum')
    plt.imshow(magnitude_spectrum)

    w, h = fshift.shape
    maxp = fshift[w//2][h//2]
    for i in range(w):
        for j in range(h):
            if i != w//2 and j != h//2:
                if abs(np.abs(fshift[i][j])-np.abs(maxp)) < np.abs(maxp) - 200000:
                    fshift[i][j] = 0

    plt.subplot(122), plt.title('Notch')
    plt.imshow(np.abs(fshift), norm=LogNorm(vmin=5))
    plt.show()

    reverse_image = reverseDFFTnp(fshift)
    reverse_image = Gauss(reverse_image)

    plt.subplot(121), plt.title('Before')
    plt.imshow(abs(img), cmap='gray')
    plt.subplot(122), plt.title('After')
    plt.imshow(abs(reverse_image), cmap='gray')
    plt.show()
