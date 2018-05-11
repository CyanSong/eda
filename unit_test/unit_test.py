import os

import xspice.xspice as nt


def test(fileName):
    circuits = open("unit_test/test_netlist/" + fileName + ".sp")
    circuits = circuits.read()
    nt.Xspice(circuits)


def unit_test():
    for root, dirs, files in os.walk("unit_test/test_netlist/"):
        for file in files:
            circuits = open(root + file)
            circuits = circuits.read()
            nt.Xspice(circuits)


if __name__ == "__main__":
    unit_test()
    #test('dc_test')
    #test('ac_test')
    # test('tran_test')
