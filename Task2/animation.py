import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

image_files = ['Phase1.png','Phase2.png','Phase3.png','Phase4.png','Phase5.png']

fig, ax = plt.subplots()


def update(frame):
    ax.clear()
    img = plt.imread(image_files[frame]) 
    ax.imshow(img)
    ax.set_title(f'Frame {frame+1}')


animation = FuncAnimation(fig, update, frames=len(image_files), interval=500)


plt.show()

