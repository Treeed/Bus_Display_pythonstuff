import re
from collections import defaultdict

base_dir = r"./saleae"


def read_can_dump(filename):
    with open(base_dir+"\\"+filename) as file:
        can_data = file.read()
    return can_data


def parse_can_dump(can_dump):
    can_data = can_dump.split('\n')[1:]

    parsed_data = defaultdict(list)

    for can_msg in can_data:
        parsed_msg = {}
        re_result = re.search(r'"([^"]*)","data",(\d+.\d+),\d.[\de-]+,(0x[A-F0-9]{2})',
                 can_msg)
        if not re_result:
            continue
        metadata = re_result.groups()
        parsed_msg["channel"] = metadata[0]
        parsed_msg["time"] = float(metadata[1])
        parsed_msg["data"] = int(metadata[2], 16)
        parsed_data[metadata[0]].append(parsed_msg)


    segmented = defaultdict(list)
    for channelname, channeldata in parsed_data.items():
        segment = []
        last_time = 1e100
        for msg in channeldata:
            if msg['time'] > last_time + 15 / 1e6:
                segmented[channelname].append(segment)
                segment = []
            segment.append(msg)
            last_time = msg["time"]
        segmented[channelname].append(segment)

    for channel in list(segmented.values()): # make a list here just to get a copy to iterate over while changing the dict
        segmented["all"].extend(channel)

    segmented["all"].sort(key=lambda elem: elem[0]["time"])


    return segmented
