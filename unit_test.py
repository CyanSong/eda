import network as nt


def test():
    circuits = open("spice.sp")
    circuits = circuits.read()
    r = nt.network(circuits)


if __name__ == "__main__":
    test()
