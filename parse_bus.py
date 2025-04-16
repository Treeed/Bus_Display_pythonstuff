import parse_segmented_uart

filename = "sim test6.csv"
# filename = "lvds dump full startup duplex data.csv"

can_dump = parse_segmented_uart.read_can_dump(filename)
can_data = parse_segmented_uart.parse_can_dump(can_dump)

out = ""
time = 0
for segment in can_data["all"]:
    #[0xFF, 0xFF, 0xFF, 0xFF, 0xFF,  0xA] every 25ms
    #[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 2] every 25ms
    #[0xFE] every 113ms in the beginning until reply
    # FF FF FF FF FF 16 in the beginning 4 times every 25ms
    # [0x1,  0,  0,  0,  0, not 6] every 40ms (gets a reply)
    # [1,  0,  0,  0,  0, 6] every 25ms (frames)

    # if segment[0]["data"] != 0xff and segment[0]["data"] != 1 :
    #     continue
    # if not all([dat["data"] == targ for dat, targ in zip(segment, [7,  0,  0,  0,  0, 6])]): #segment[0]["data"] != 0xff and segment[0]["data"] != 7 :
    #     continue
    # if not(len(segment) > 5 and segment[0]["data"] == 0xFF and segment[5]["data"] == 0x16):
    #     continue

    if segment[0]["channel"] == "from disp":
        out+= "D:"
    else:
        out+= "C:"

    diff = segment[0]["time"] - time
    out += f"{diff*1e3:>4.0f} "
    time = segment[0]["time"]

    if len(segment) != 167:
        for byt in segment:
            out += f'{byt["data"]:>2X} '
        out+='\n\n'
        continue

    for byt in segment[:7]:
        out+=f'{byt["data"]:>2X} '
    out+='\n'
    for bytnum in range(7, 167, 16):
        line = segment[bytnum:bytnum+16]
        line = line[::-1]
        csum = 0
        for byt in line:
            for bit in range(8):
                dat = (byt["data"]>>bit)&1
                if dat:
                    out += "#"
                else:
                    out += '.'
        out+='\n'
    out+='\n'


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
file = open(f"./{filename}", "w")
file.write(out)
file.close()