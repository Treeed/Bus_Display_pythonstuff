import parse_segmented_uart

# filename = "sim test3.csv"
filename = "lvds dump full startup.csv"

can_dump = parse_segmented_uart.read_can_dump(filename)
can_data = parse_segmented_uart.parse_can_dump(can_dump)

last_time = 1e100
start = 0
def find_pack():
    pack = []
    global start, last_time
    for byt in can_data[start:]:
        if byt['time'] > last_time+100/1e6:
            last_time = byt['time']
            break
        start += 1
        last_time = byt['time']
        pack.append(byt)
    return pack

segmented = []

while start < len(can_data):
    segmented.append(find_pack())

out = ""
for segment in segmented:
    out+= f'{len(segment)}, '
    for byt in segment:
        out += f'0x{byt["data"]:02x}, '
    out+='\n'
    continue



# for segment in segmented:
#     col = 0
#     for val in segment[7:]:
#         for bit in range(8):
#             dat = (val["data"]>>(7-bit))&1
#             if dat:
#                 out += "#"
#             else:
#                 out += ' '
#             col += 1
#             if col > 127:
#                 out += '\n'
#                 col = 0
#     out += '\n\n'
file = open(f"./{filename}_replay", "w")
file.write(out)
file.close()