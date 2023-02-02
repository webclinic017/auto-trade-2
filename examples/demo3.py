import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import matplotlib.animation as animation

def create_heart(ax):
    t = np.linspace(0, 2 * np.pi, 100)
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    ax.plot(x, y, 'r')
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.axis('off')

def create_frame(frame_number):
    ax.clear()
    if frame_number >= 0:
        create_heart(ax)
    if frame_number >= 100:
        ax.add_patch(patches.Polygon([[-15, 0], [0, 20], [15, 0]], fill=True, color='r'))
    if frame_number >= 200:
        ax.text(0, 0, '❤️', ha='center', va='center', fontsize=32)

fig, ax = plt.subplots(figsize=(5, 5))
ani = animation.FuncAnimation(fig, create_frame, frames=300, interval=50)
plt.show()