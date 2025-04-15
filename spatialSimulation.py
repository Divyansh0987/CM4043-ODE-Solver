import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.cm as cm

# Width, height of the image.
nx, ny = 600, 450

# Reaction parameters.
k1, k2, k3, k4, k5 = 2, 3000000, 66, 3000, 0.06

def update(p, arr):
    """Update arr[p] to arr[q] by evolving in time."""

    # Count the average amount of each species in the 9 cells around each cell
    # by convolution with the 3x3 array m.
    q = (p+1) % 2
    s = np.zeros((3, ny, nx))
    m = np.ones((3, 3)) / 9
    for k in range(3):
        s[k] = convolve2d(arr[p, k], m, mode='same', boundary='wrap')
    
    EPS = k1 / k3
    A = 0.2
    P = (k1 * A) / k5
    Q = 2*k1*k4/(k2*k3)

    # Apply the reaction equations
    arr[q, 0] = (s[0] + s[1] - s[0]*s[1] - Q*(s[0]*s[0]))/EPS
    arr[q, 1] = 2*A*s[2] - s[1] - s[0]*s[1]
    arr[q, 2] = (s[0] - s[2])/P

    # Ensure the species concentrations are kept within [0,1].
    np.clip(arr[q], 0, 1, arr[q])
    return arr

# Initialize the array with amounts of A, B and C.
# arr = np.random.random(size=(2, 3, ny, nx))
arr = np.zeros((2, 3, ny, nx))
arr[:, 0, :, :] = 0.001
arr[:, 1, :, :] = 0.001
arr[:, 2, :, :] = 0.04

# Set up the image
fig, ax = plt.subplots()
im = ax.imshow(np.zeros((ny, nx)), cmap='viridis', vmin=0, vmax=1) # Initialize im here
ax.axis('off')

def animate(i, arr):
    """Update the image for iteration i of the Matplotlib animation."""
    arr = update(i % 2, arr)
    current_arr = arr[i % 2]
    combined_arr = np.stack([current_arr[0], current_arr[1], current_arr[2]], axis=0)
    max_val_indices = np.argmax(combined_arr, axis=0)
    result_image = np.zeros((ny, nx))
    cmap_data = np.zeros((ny, nx, 4))  # RGBA for custom coloring

    for y in range(ny):
        for x in range(nx):
            max_index = max_val_indices[y, x]
            result_image[y, x] = current_arr[max_index, y, x]
            if max_index == 0:
                cmap_data[y, x] = cm.Reds(current_arr[0, y, x])
            elif max_index == 1:
                cmap_data[y, x] = cm.Greens(current_arr[1, y, x])
            else:
                cmap_data[y, x] = cm.Blues(current_arr[2, y, x])

    im.set_array(cmap_data)
    return [im]

anim = animation.FuncAnimation(fig, animate, frames=12000, interval=10,
                               blit=False, fargs=(arr, ))

# To view the animation, uncomment this line
plt.show()

# To save the animation as an MP4 movie, uncomment this line
#anim.save(filename='bz.mp4', fps=30)