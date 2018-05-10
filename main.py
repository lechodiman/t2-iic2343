# import json
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
    MEM_FIS_SIZE = 512
    MEM_VIR_SIZE = 1024
    PAGE_SIZE = 32
    SUBSTITUTION = "FA"
    NUM_LINE = 4
    CORR = "FA"
    SUBS = "FIFO"
    NUM_PROG = 4
    PROG = [[1, 2, 4, 6, 2, -1, 4, 7, 3, 5, -1, 2, 1], [6, 4, 2, 5, 7, 8, 5, 4, 5, -1, 5], [1, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 3]]

    cpu = CPU(MEM_FIS_SIZE, MEM_VIR_SIZE, PAGE_SIZE, SUBSTITUTION,
              NUM_LINE, CORR, SUBS, NUM_PROG, PROG)

    cpu.load_components()
    cpu.print_components_info()
    cpu.run_programs()
    print(cpu.is_finished)
