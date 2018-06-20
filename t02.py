import json
from CPU import CPU
import sys

if __name__ == "__main__":
    DEBUG_MODE = True

    if DEBUG_MODE:
        with open('./Debug/TestEvaluados/Test 2 Input.txt') as file:
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

        log_file = open('./message.log', 'w')
        old_stdout = sys.stdout
        sys.stdout = log_file

        cpu = CPU(**kwargs)
        cpu.run_programs()
        sys.stdout = old_stdout
        log_file.close()

    else:
        MEM_FIS_SIZE = int(input())
        MEM_VIR_SIZE = int(input())
        PAGE_SIZE = int(input())
        SUBSTITUTION = input()
        NUM_LINE = int(input())
        CORR = input()
        SUBS = input()
        NUM_PROG = int(input())
        PROG = json.loads(input())
        ###############################################################
        cpu = CPU(MEM_FIS_SIZE, MEM_VIR_SIZE, PAGE_SIZE, SUBSTITUTION,
                  NUM_LINE, CORR, SUBS, NUM_PROG, PROG)
        cpu.run_programs()
