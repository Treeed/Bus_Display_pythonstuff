import imageio
import numpy as np
# filename = "formattest.png"
# filename = "sr211149541d131 Kopie.gif"
filename = "sr211149541d131 shapetestt.gif"
im = np.asarray(imageio.mimread(filename))
# im = im[0:1]
im = np.logical_and.reduce(im != im[0, 0, 0], axis=-1)
imcrop = np.zeros((im.shape[0], 40, 120), dtype=bool)
maxsizes = np.min((imcrop.shape[1:3],im.shape[1:3]), axis=0)
imcrop[:, :maxsizes[0], :maxsizes[1]] = im[:, :maxsizes[0], :maxsizes[1]]

imm = imcrop.flatten()
imm = np.packbits(imm)
np.savetxt(filename+"_array", imm, delimiter=",",fmt="%.f,", newline="")
print("tt")