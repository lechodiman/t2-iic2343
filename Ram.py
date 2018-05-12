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

    @property
    def num_of_marcos(self):
        return int(self.mem_fis_size / self.page_size)

    def init_marcos(self):
        self.marcos = []
        for num_of_marco in range(self.num_of_marcos):
            m = Marco(num_of_marco)
            self.marcos.append(m)

    def add_page(self, page, iteration, disk):
        # Look for available marco
        available_marco = None
        for m in self.marcos:
            if m.is_empty:
                available_marco = m

        # If there is no av marco, backup one
        if not available_marco:
            marco_to_backup = self.get_marco_to_backup()

            # Move marco to disk
            disk.receive_marco(marco_to_backup)

            # Update swap out
            program_out_index = marco_to_backup.page_inside.program
            self.swap_out_stats[program_out_index] += 1

            # Create new marco with same number
            marco_numer = marco_to_backup.num_block
            new_marco = Marco(marco_numer)

            # Replace in self.marcos
            for index, m in enumerate(self.marcos):
                if m.num.block == marco_numer:
                    self.marcos[index] = new_marco

            # Assign page (this updates on_disk attr)
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
            # Replace with marco with least times used
            marco_least_used = self.marcos[0]
            for m in self.marcos:
                if m.times_used < marco_least_used.times_used:
                    marco_least_used = m

            marco_to_backup = marco_least_used

        return marco_to_backup

    def swap_in_out(self, page, disk):
        marco_to_backup = self.get_marco_to_backup()

        marco_to_swap_in = disk.pop_marco_to_swap_in(page)

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

    def update_counters(self, page, iteration):
        for m in self.marcos:
            if m.page_inside == page:
                m.last_used_time = iteration
                m.times_used += 1

    def get_pages_on_ram(self, program_index):
        pages_on_ram = 0
        for m in self.marcos:
            if m.page_inside and m.page_inside.program == program_index:
                pages_on_ram += 1

        return pages_on_ram
