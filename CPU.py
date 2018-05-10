class CPU:

    def __init__(self, mem_fis_size, mem_vir_size, page_size, subtitution,
                 num_line, corr, subs, num_prog, prog):
        self.mem_fis_size = mem_fis_size
        self.mem_vir_size = mem_vir_size
        self.page_size = page_size
        self.subtitution = subtitution
        self.num_line = num_line
        self.corr = corr
        self.subs = subs
        self.num_prog = num_prog
        self.prog = prog

        # Stores index of current program running
        self.current_program_index = 0

        # Dict to store last addr for each program
        # {program_index : last_addr_used_index}
        self.last_addr_used_register = {prog: 0 for prog in range(num_prog)}
        print(self.last_addr_used_register)

    @property
    def is_finished(self):
        ''' Returns true if all programs did everything they had to do.
        Checks if last index of program is equal to the lenght  - 1 for
        every program'''
        last_address_programs = [len(prog) - 1 for prog in self.prog]
        last_used = self.last_addr_used_register.values()
        comparations = [i == j for i, j in zip(last_address_programs, last_used)]

        return len(set(comparations)) == 1 and comparations[0]

    @property
    def current_program_list(self):
        return self.prog[self.current_program_index]

    def load_components(self):
        pass

    def print_components_info(self):
        pass

    def run_programs(self):
        for addr, j in enumerate(self.current_program_list):
            pass

    def next_program(self):
        self.current_program_index += 1
        self.current_program_index = 0 if self.current_program_index == self.num_prog else self.current_program_index
