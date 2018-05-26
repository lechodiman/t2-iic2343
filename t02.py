import json
from CPU import CPU


if __name__ == "__main__":
    # MEM_FIS_SIZE = int(input())
    # MEM_VIR_SIZE = int(input())
    # PAGE_SIZE = int(input())
    # SUBSTITUTION = input()
    # NUM_LINE = int(input())
    # CORR = input()
    # SUBS = input()
    # NUM_PROG = int(input())
    # PROG = json.loads(input())
    #################################################################

    # Versión harcodeada con un ejemplo de input
    # MEM_FIS_SIZE = 16
    # MEM_VIR_SIZE = 32
    # PAGE_SIZE = 4
    # SUBSTITUTION = "LRU"
    # NUM_LINE = 2
    # CORR = "FA"
    # SUBS = "FIFO"
    # NUM_PROG = 4
    # PROG = [[1, 2, 4, 7, 3, 5, 31, -1, 31, 23, 15, 25, 1, 9, 15],
    #         [-1, 6, 4, 2, 5, 7, 8, 5, 4, 5, -1, 5],
    #         [-1, 4, 5, 6, 7],
    #         [-1, 2, 3, 4, 5, 6, 3]]

    with open('./Debug/Test 1 Input.txt') as file:
        lines = [l.strip().replace(" ", "").split("=") for l in file.readlines()]
        kwargs = {v[0]: v[1] for v in lines}

        # change type
        kwargs["MEM_FIS_SIZE"] = int(kwargs["MEM_FIS_SIZE"])
        kwargs["MEM_VIR_SIZE"] = int(kwargs["MEM_VIR_SIZE"])
        kwargs["PAGE_SIZE"] = int(kwargs["PAGE_SIZE"])
        kwargs["SUBSTITUTION"] = kwargs["SUBSTITUTION"].replace('"', '')
        kwargs["NUM_LINE"] = int(kwargs["NUM_LINE"])
        kwargs["CORR"] = kwargs["CORR"].replace('"', '')
        kwargs["SUBS"] = kwargs["SUBS"].replace('"', '')
        kwargs["NUM_PROG"] = int(kwargs["NUM_PROG"])
        kwargs["PROG"] = json.loads(kwargs["PROG"])

    cpu = CPU(**kwargs)
    # cpu = CPU(MEM_FIS_SIZE, MEM_VIR_SIZE, PAGE_SIZE, SUBSTITUTION,
    #           NUM_LINE, CORR, SUBS, NUM_PROG, PROG)
    cpu.run_programs()
