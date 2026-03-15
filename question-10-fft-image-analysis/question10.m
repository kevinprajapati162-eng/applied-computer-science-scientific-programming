% --- Preamble: Clear old variables and close old windows ---
clear;         % Clears any old variables from memory
clc;           % Clears the Command Window
close all;     % Closes all open figures (image windows)

% --- Step 1: Import an Image ---
% We will use a built-in MATLAB image called 'cameraman.tif'
% This avoids any problems with file paths.
I = imread('cameraman.tif');

% --- Step 2: Apply 2D FFT ---
% This converts the image from pixels (spatial domain)
% to frequencies (frequency domain).
F = fft2(I);

% --- Step 3: Shift Zero-Frequency Component to Centre ---
% By default, the main brightness (DC component) is in the top-left
% corner. fftshift() moves it to the center for easier viewing.
F_shifted = fftshift(F);

% --- Step 4: Take Logarithm of Absolute FFT Output ---
% The FFT output has a huge dynamic range. We use log(1 + abs(...))
% to see the details. We use '1 +' to avoid taking log(0).
F_log_abs = log(1 + abs(F_shifted));

% --- Step 5: Visualize the Results ---
% Create a figure window to hold our plots
figure;

% Create the first plot (1 row, 2 columns, 1st position)
subplot(1, 2, 1);
imshow(I); % 'imshow' is great for showing standard images
title('Original Image');

% Create the second plot (1 row, 2 columns, 2nd position)
subplot(1, 2, 2);
% 'imagesc' scales the data to show the full range of values
imagesc(F_log_abs);
colormap('gray'); % Set the color map to grayscale as requested
title('FFT Log-Magnitude Spectrum');
axis equal tight; % Makes the image look correctsa