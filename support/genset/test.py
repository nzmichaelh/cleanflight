import serial
import sys

import msp
import libmsp

def reader(link, port):
    while True:
        got = port.read(1)
        if not got:
            yield None
            continue

        got += port.read(port.inWaiting())
        yield from link.feed(got)


def main():
    print(msp)
    registry = msp.register()

    port = serial.Serial(sys.argv[1], 115200, timeout=0.2)
    link = libmsp.Link(port, registry)
    r = reader(link, port)

#    for pg in r:
#        print(repr(pg))
    for i in range(0, 25600):
        i = msp.PGN.MSP_STATUS
#        link.request(msp.PGN.MSP_BOXNAMES)
        name = msp.PGN.name(i)
        if not name:
            continue
        if 'REBOOT' in name:
            continue
        if '_SET_' in name:
            continue
        link.request(i)
        f = None
        for pg in r:
            if pg is None:
                break
            if pg.PGN == i:
                f = pg
                break
            print(repr(pg))
        print(msp.PGN.name(i), repr(f))

main()
