import network as nt


def test(fileName):
    circuits = open("test_netlist/"+fileName+".sp")
    circuits = circuits.read()
    nt.network(circuits)


if __name__ == "__main__":
    test('dc_test')
    test('ac_test')
    test('tran_test')