import network as nt


def test():
    circuits = open("test_netlist/spice.sp")
    circuits = circuits.read()
    r = nt.network(circuits)


if __name__ == "__main__":
    test()
