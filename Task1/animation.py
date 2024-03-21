import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

image_files = ['graph_plot1.png','graph_plot2.png','graph_plot3.png','graph_plot4.png','graph_plot5.png','graph_plot6.png','graph_plot7.png','graph_plot8.png','graph_plot9.png','graph_plot10.png','graph_plot11.png']

fig, ax = plt.subplots()


def update(frame):
    ax.clear()
    img = plt.imread(image_files[frame]) 
    ax.imshow(img)
    ax.set_title(f'Frame {frame+1}')


animation = FuncAnimation(fig, update, frames=len(image_files), interval=500)


plt.show()

