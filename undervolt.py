#!/usr/bin/env python3
import os
import struct
import glob
import argparse
import json

parser = argparse.ArgumentParser(description='Undervolt intel 6+th gen CPU and GPU.')
parser.add_argument('-gpu', type=int, help='Undervolt GPU by this amount of millivolts. Must be negative.')
parser.add_argument('-cpu', type=int, help='Undervolt CPU by this amount of millivolts. Must be negative.')
parser.add_argument('-config', type=str, help='Config file to load. Other flags has priority over -config.')
opt=parser.parse_args()


if os.geteuid() != 0:
    print("Running as non-root. Apply commands by hand.")

def writemsr(msr, val):
    if os.geteuid() != 0:
        print("sudo wrmsr 0x%X 0x%X" % (msr, val))
        return

    n = glob.glob('/dev/cpu/[0-9]*/msr')
    for c in n:
        f = os.open(c, os.O_WRONLY)
        os.lseek(f, msr, os.SEEK_SET)
        os.write(f, struct.pack('Q', val))
        os.close(f)
    if not n:
        raise OSError("msr module not loaded (run modprobe msr)")

def set_undervolt(device_name, mv):
    device_map = {
        "cpu": [0, 2],
        "gpu": [1]
    }

    devices = device_map.get(device_name)
    assert device_name is not None, "Invalid device %s" % device_name
    for device in devices:
        assert device >= 0
        assert mv <= 0
        offset = mv*1.024

        payload = (1<<63) | ((device & 0x0F)<<40) | 0x11 << 32 | (0xFFE00000&((round(offset) & 0xFFF)<<21))

        writemsr(0x150, payload)

if opt.config is not None:
    with open(opt.config) as f:
        cfile = json.load(f)

    if opt.cpu is None:
        opt.cpu = cfile.get("cpu")
    if opt.gpu is None:
        opt.gpu = cfile.get("gpu")

if opt.cpu is not None:
    set_undervolt("cpu", opt.cpu)

if opt.gpu is not None:
    set_undervolt("gpu", opt.gpu)
