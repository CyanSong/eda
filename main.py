import network as nt


def test():
    circuits = open("spice.sp")
    circuits = circuits.read()
    print(circuits + "\n")

    c = nt.network(circuits)
    c.dc_handler(None)
    # pydot__tree_to_png(tree, r"tree.png")


if __name__ == "__main__":
    test()
