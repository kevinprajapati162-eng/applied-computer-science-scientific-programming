import numpy as np
import matplotlib.pyplot as plt
from skimage import data, util

plt.close('all')

I = data.camera()
F = np.fft.fft2(I)
F_shifted = np.fft.fftshift(F)
F_log_abs = np.log(1 + np.abs(F_shifted))

plt.figure()
plt.subplot(1, 2, 1)
plt.imshow(I, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(F_log_abs, cmap='gray')
plt.title('FFT Log-Magnitude Spectrum')
plt.axis('off')

plt.savefig('fft_result.png')
plt.show()
