from TableOfPages import TableOfPages
from Ram import Ram
from Tlb import Tlb
from Disk import Disk


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

        # Works as a timestamp for FIFO, LFU, LRU stats
        self.iteration = 0

        self.load_components()

    @property
    def is_finished(self):
        ''' Returns true if all programs did everything they had to do.
        Checks if last index of program is equal to the length  - 1 for
        every program'''
        last_address_programs = [len(prog) - 1 for prog in self.prog]
        last_used = self.last_addr_used_register.values()
        comparations = [i == j for i, j in zip(last_address_programs, last_used)]

        return len(set(comparations)) == 1 and comparations[0]

    @property
    def current_program_list(self):
        ''' Returns current program list '''
        return self.prog[self.current_program_index]

    @property
    def current_program_is_finished(self):
        ''' Compares indexes of last addr used and len of program - 1 '''
        last_addr_current_program = len(self.current_program_list) - 1
        last_addr_used = self.last_addr_used_register[self.current_program_index]

        return last_addr_used == last_addr_current_program

    def load_components(self):
        ''' Loads all essentials components'''
        # print("Loading components")
        self.table_of_pages = TableOfPages(self.mem_vir_size, self.page_size,
                                           self.num_prog)
        self.ram = Ram(self.mem_fis_size, self.page_size, self.subtitution, self.num_prog)
        self.tlb = Tlb(self.num_line, self.subs, self.corr, self.num_prog)
        self.disk = Disk(self.num_prog)

    def run_programs(self):
        ''' Flow control to run programs in correct order '''
        while not self.is_finished:
            # If current program is finished go to next program
            if self.current_program_is_finished:
                print("Program {} already finished".format(self.current_program_index))
                self.next_program()
                continue

            # If it is not finished, use it
            # print("-" * 25)
            # print("Current program {}".format(self.current_program_index))

            # Get last addres used by this program
            last_used_this_program = self.last_addr_used_register[self.current_program_index]

            # If program starts with yield, save info and go to next program
            if last_used_this_program == 0 and self.current_program_list[last_used_this_program] == -1:
                # print("Cleaning TLB")
                self.tlb.clear()

                # Save last addres used in this program and add one so it does not resumes from
                # index 0 and addres -1
                self.last_addr_used_register[self.current_program_index] = last_used_this_program + 1

                # Go to next program
                self.next_program()

                # Skip iteration
                continue

            # If not, check if it resumes from a -1.
            # Add one to the index if cpu takes this program from a -1
            last_used_this_program = last_used_this_program + 1 if self.current_program_list[last_used_this_program] == -1 else last_used_this_program

            # For every address not used, run it
            for j, addr in enumerate(self.current_program_list):
                # Omit addresses already used
                if j < last_used_this_program:
                    continue

                # print("Addr: {}, program: {}".format(addr, self.current_program_index))

                # Save last addres used in this program
                self.last_addr_used_register[self.current_program_index] = j

                # If addr is a yield, clean TLB and go to next program
                if addr < 0:
                    # print("Cleaning TLB")
                    self.tlb.clear()

                    # Go to next program
                    self.next_program()

                    # Break out of for loop
                    break

                # If it is not a yield, increase iteration counter
                self.iteration += 1

                # Check first digits of addr to get page number
                bin_addr = self.table_of_pages.to_binary(addr)
                bits_to_check = self.table_of_pages.num_of_bits_page
                page_digits = bin_addr[:bits_to_check]
                page_number = self.table_of_pages.to_decimal(page_digits)

                # Check page in TLB, if it finds the page updates hit count and returns it
                page = self.tlb.get_page(page_number, self.current_program_index, self.iteration)

                if not page:
                    # If it not found, go to table of pages and add to TLB
                    page = self.table_of_pages.get_page(page_number, self.current_program_index)

                    self.tlb.add_page(page, bin_addr, self.iteration)

                # Check if it has a marco in RAM
                if not page.has_marco:
                    # Page fault
                    self.table_of_pages.update_page_faults(self.current_program_index)

                    # Assign a marco
                    self.ram.add_page(page, self.iteration, self.disk)
                else:
                    # If it has it can be on disk or ram
                    if page.on_disk:
                        # Page fault
                        self.table_of_pages.update_page_faults(self.current_program_index)

                        # Bring back page to ram, and backup one marco to disk
                        self.ram.swap_in_out(page, self.disk, self.iteration)

                        # It counts as a use for page that came back (LFU, LRU)
                        self.ram.update_counters(page, self.iteration)
                    else:
                        # It has a marco on ram (LFU, LRU)
                        self.ram.update_counters(page, self.iteration)

        # print("All programs finished")
        self.print_statistics()

    def print_statistics(self):
        for p in range(self.num_prog):
            print("Programa {}".format(p))
            # Hit TLB
            hit_tlb = self.tlb.hit_stats[p]
            page_fault = self.table_of_pages.page_fault_stats[p]
            swap_in = self.ram.swap_in_stats[p]
            swap_out = self.ram.swap_out_stats[p]
            page_disk = self.disk.get_pages_on_disk(p)
            pages_ram = self.ram.get_pages_on_ram(p)
            page_valid = page_disk + pages_ram
            print("hit TLB: {}".format(hit_tlb))
            print("page fault: {}".format(page_fault))
            print("swap in: {}".format(swap_in))
            print("swap out: {}".format(swap_out))
            print("page valid: {}".format(page_valid))
            print("page disk: {}".format(page_disk))

    def next_program(self):
        self.current_program_index += 1
        self.current_program_index = 0 if self.current_program_index == self.num_prog else self.current_program_index
