fn = "TE28F320J3C@TSOP56_correct_20250410232627.BIN"
fil = open(fn, "rb")
content = fil.read()
fil.close()
content = bytearray(content)

for byt in range(0, len(content), 2):
    content[byt], content[byt+1] = content[byt+1], content[byt]

fil = open(fn+"swapped", "wb")
fil.write(content)
fil.close()