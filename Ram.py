from Marco import Marco


class Ram:

    def __init__(self, mem_fis_size, page_size, subtitution, num_programs):
        self.mem_fis_size = mem_fis_size
        self.page_size = page_size
        self.subtitution = subtitution

        self.init_marcos()

        # Dict to store swap outs
        self.swap_out_stats = {num: 0 for num in range(num_programs)}

        # Dict to store swap in
        self.swap_in_stats = {num: 0 for num in range(num_programs)}

        print("Memoria fisica de {} bytes tiene {} marcos".format(self.mem_fis_size, self.num_of_marcos))

    @property
    def num_of_marcos(self):
        return int(self.mem_fis_size / self.page_size)

    @property
    def is_full(self):
        # Look for available marco
        available_marco = None
        for m in self.marcos:
            if m.is_empty:
                available_marco = m

        if not available_marco:
            return True

        return False

    def __repr__(self):
        msg = "\n\t Memoria Fisica, substitution: {}\n\n".format(self.subtitution)
        for m in self.marcos:
            msg += "Marco {} ".format(m.num_block)
            msg += "- Pagina virtual {}".format(repr(m.page_inside))
            msg += "- LRU: {} ".format(m.last_used_time)
            msg += "- LFU: {} ".format(m.times_used)
            msg += "- FIFO: {} ".format(m.insertion_time)
            msg += "\n"

        return msg

    def init_marcos(self):
        self.marcos = []
        for num_of_marco in range(self.num_of_marcos):
            m = Marco(num_of_marco)
            self.marcos.append(m)

    def add_page(self, page, iteration, disk):
        if not self.is_full:
            self.swap_in_stats[page.program] += 1

        # Look for available marco (the first one)
        available_marco = None
        for m in self.marcos:
            if m.is_empty:
                available_marco = m
                break

        if available_marco:
            print("[RAM] Asociando pagina {} a marco {}".format(page, available_marco.num_block))
            available_marco.assign_page(page, iteration)

        # If there is no av marco, backup one
        else:
            print("[PAGE FAULT] (de nuevo ?) Memoria llena. \
                Es necesario asignar marco para pagina {}".format(page))

            marco_to_backup = self.get_marco_to_backup()
            print("[Sustitucion RAM] {}, se va el marco {}".format(self.subtitution, marco_to_backup.num_block))

            # Move marco to disk (this updates on_disk attr)
            disk.receive_marco(marco_to_backup)

            # Update swap out and swap in
            print("[SWAP OUT] La pagina virtual: {}".format(marco_to_backup.page_inside))
            print("[SWAP IN]  La pagina virtual: {}".format(page))
            program_out_index = marco_to_backup.page_inside.program
            program_in_index = page.program
            self.swap_out_stats[program_out_index] += 1
            self.swap_in_stats[program_in_index] += 1

            # Create new marco with same number
            marco_number = marco_to_backup.num_block
            new_marco = Marco(marco_number)

            # Replace in self.marcos
            for index, m in enumerate(self.marcos):
                if m.num_block == marco_number:
                    self.marcos[index] = new_marco
                    break

            # Assign page
            new_marco.assign_page(page, iteration)

    def get_marco_to_backup(self):
        if self.subtitution == "FIFO":
            # Replace with marco with min insertion time
            marco_min_insertion_time = self.marcos[0]
            for m in self.marcos:
                if m.insertion_time < marco_min_insertion_time.insertion_time:
                    marco_min_insertion_time = m

            marco_to_backup = marco_min_insertion_time

        elif self.subtitution == "LRU":
            # Replace with marco with min time of last usage
            marco_min_time = self.marcos[0]
            for m in self.marcos:
                if m.last_used_time < marco_min_time.last_used_time:
                    marco_min_time = m

            marco_to_backup = marco_min_time

        elif self.subtitution == "LFU":
            # Replace with marco with least times used, if tie, then FIFO
            marco_to_backup = sorted(self.marcos, key=lambda m:(m.times_used, m.insertion_time))[0]

        return marco_to_backup

    def swap_in_out(self, page, disk, iteration):
        marco_to_backup = self.get_marco_to_backup()

        marco_to_swap_in = disk.pop_marco_to_swap_in(page)

        # Update counters
        entering_page = marco_to_swap_in.page_inside
        marco_to_swap_in.remove_page()
        marco_to_swap_in.assign_page(entering_page, iteration)

        # Change number of marco to stay the same
        marco_to_swap_in.num_block = marco_to_backup.num_block

        # Replace in self.marcos in same position
        for index, m in enumerate(self.marcos):
            if m == marco_to_backup:
                self.marcos[index] = marco_to_swap_in

        # Move marco to disk
        disk.receive_marco(marco_to_backup)

        # Update swap out
        program_out_index = marco_to_backup.page_inside.program
        self.swap_out_stats[program_out_index] += 1

        # Update swap in
        program_in_index = marco_to_swap_in.page_inside.program
        self.swap_in_stats[program_in_index] += 1

        print("[SWAP OUT] El marco {}".format(marco_to_backup))
        print("[SWAP IN] El marco {}".format(marco_to_swap_in))

    def update_counters(self, page, iteration):
        for m in self.marcos:
            if m.page_inside and m.page_inside == page:
                m.last_used_time = iteration
                m.times_used += 1

    def get_pages_on_ram(self, program_index):
        pages_on_ram = 0
        for m in self.marcos:
            if m.page_inside and m.page_inside.program == program_index:
                pages_on_ram += 1

        return pages_on_ram
