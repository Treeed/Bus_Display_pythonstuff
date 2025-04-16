import time

import serial

ser = serial.Serial("COM12", 2000000)

import parse_segmented_uart

# filename = "sim test3.csv"
filename = "lvds dump full startup duplex data.csv"

can_dump = parse_segmented_uart.read_can_dump(filename)
can_data = parse_segmented_uart.parse_can_dump(can_dump)

last_time = 0
for segment in can_data["all"]:
    for msg in segment:
        if msg["time"]-last_time > 0:
            time.sleep(msg["time"]-last_time)
        last_time = msg["time"]
        ser.write(msg["data"])
