import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scipy.special as sps

def complex_gamma_function(s, t_offset=0):
    return sps.gamma(s - t_offset)

x = np.linspace(-5, 5, 200)
y = np.linspace(-5, 5, 200)
X, Y = np.meshgrid(x, y)

S = X + 1j * Y

t_static = 0

W = complex_gamma_function(S, t_static)

fig_heatmap = plt.figure(figsize=(10, 8))
mag_clipped = np.clip(np.abs(W), 0, 1e10)
plt.imshow(np.log1p(mag_clipped), 
           extent=[x.min(), x.max(), y.min(), y.max()], 
           origin='lower', 
           cmap='inferno')
plt.colorbar(label='log(1 + |Gamma(s)|)')
plt.title(f'2D Heatmap of |Gamma(s)| Magnitude (t={t_static})')
plt.xlabel('Real Part (x)')
plt.ylabel('Imaginary Part (y)')

for p in [0, -1, -2, -3, -4]:
    plt.axvline(p, color='cyan', linestyle='--', linewidth=1, 
                label='Poles' if p==0 else None)
plt.legend()

heatmap_file = 'gamma_heatmap.png'
fig_heatmap.savefig(heatmap_file)
print(f"Heatmap saved successfully as '{heatmap_file}'")

plt.show()

fig_3d = plt.figure(figsize=(14, 7))
fig_3d.suptitle(f'3D Surface Plots of Gamma(s) (t={t_static})', fontsize=16)

ax1 = fig_3d.add_subplot(1, 2, 1, projection='3d')
W_real_clipped = np.clip(np.real(W), -10, 10)
ax1.plot_surface(X, Y, W_real_clipped, cmap='viridis')
ax1.set_title(f'Real Part (Re[Gamma(s)])')
ax1.set_xlabel('Real (x)')
ax1.set_ylabel('Imaginary (y)')
ax1.set_zlabel('Re(W) (Clipped)')

ax2 = fig_3d.add_subplot(1, 2, 2, projection='3d')
W_imag_clipped = np.clip(np.imag(W), -10, 10)
ax2.plot_surface(X, Y, W_imag_clipped, cmap='magma')
ax2.set_title(f'Imaginary Part (Im[Gamma(s)])')
ax2.set_xlabel('Real (x)')
ax2.set_ylabel('Imaginary (y)')
ax2.set_zlabel('Im(W) (Clipped)')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

surface_plot_file = 'gamma_3d_surfaces.png'
fig_3d.savefig(surface_plot_file)
print(f"3D surface plots saved successfully as '{surface_plot_file}'")

plt.show()

skip = 10
X_skip = X[::skip, ::skip]
Y_skip = Y[::skip, ::skip]
W_skip = W[::skip, ::skip]

U = np.real(W_skip)
V = np.imag(W_skip)

fig_quiver = plt.figure(figsize=(10, 10))
plt.quiver(X_skip, Y_skip, U, V, 
           color='blue', 
           scale=200, 
           headwidth=4, 
           width=0.003)
plt.title(f'Vector Field (Quiver Plot) of Gamma(s)')
plt.xlabel('Real (x)')
plt.ylabel('Imaginary (y)')
for p in [0, -1, -2, -3, -4]:
    plt.axvline(p, color='red', linestyle='--', linewidth=1, 
                label='Poles' if p==0 else None)
plt.axis('image')
plt.legend()

quiver_plot_file = 'gamma_quiver_plot.png'
fig_quiver.savefig(quiver_plot_file)
print(f"Quiver plot saved successfully as '{quiver_plot_file}'")

plt.show()

fig_anim, ax_anim = plt.subplots(figsize=(8, 6))

initial_t = 0
W_initial = complex_gamma_function(S, initial_t)
mag_initial = np.log1p(np.clip(np.abs(W_initial), 0, 1e10))

vmax = np.log1p(100)
cax = ax_anim.pcolormesh(X, Y, mag_initial, 
                         cmap='inferno', 
                         vmin=0, vmax=vmax)

fig_anim.colorbar(cax, label='log(1 + |Gamma(s-t)|)')
title = ax_anim.set_title(f'Magnitude |Gamma(s - t)| for t = {initial_t:.2f}')
ax_anim.set_xlabel('Real (x)')
ax_anim.set_ylabel('Imaginary (y)')

def update(frame):
    t = float(frame) 
    W_anim = complex_gamma_function(S, t)
    mag_anim = np.log1p(np.clip(np.abs(W_anim), 0, 1e10))
    
    cax.set_array(mag_anim.ravel())
    title.set_text(f'Magnitude |Gamma(s - t)| for t = {t:.2f}')

t_values = np.linspace(0, 3, 100)

print("Saving animation... This may take a moment.")
ani = FuncAnimation(fig_anim, 
                    update, 
                    frames=t_values, 
                    interval=50)

animation_file = 'gamma_function_animation.html'
ani.save(animation_file, writer='html')
print(f"Animation saved successfully as '{animation_file}'")

plt.close(fig_anim)
