import matplotlib.pyplot as plt
import numpy as np

# Create a sample figure to access the colormap
fig, ax = plt.subplots(figsize=(4, 1))
cmap = plt.get_cmap('cividis')

# Create a colormap index from 0 to 255 (256 discrete colors)
color_index = np.linspace(0, 255, 256, dtype=int)

# Get the RGB values of the colormap at each index
cividis_rgb_values = cmap(color_index)

# Close the sample figure
plt.close(fig)