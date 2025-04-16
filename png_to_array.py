from PIL import Image
import numpy as np
# filename = "formattest.png"
filename = "teebeutel.png"
im = Image.open(filename)

img = np.array(im).swapaxes(0,1)

reordered = np.zeros((10, 128), dtype="bool")
reordered[:,8:68] = img[10:20,:]
reordered[:,68:128] = img[0:10,:]
packed = np.packbits(reordered, axis=1)


fil = open(filename+".txt", "w")
for line in packed:
    for byt in line:
        fil.write(f"{byt}, ")
    fil.write("\n")
fil.close()
print("tt")