from Page import Page
from math import log


class TableOfPages:

    def __init__(self, mem_vir_size, page_size, num_programs):
        self.mem_vir_size = mem_vir_size
        self.page_size = page_size
        self.num_programs = num_programs

        self.init_tables()

    @property
    def num_of_pages(self):
        return int(self.mem_vir_size / self.page_size)

    @property
    def num_of_bits_page(self):
        return int(log(self.num_of_pages, 2))

    @property
    def num_of_bits_offset(self):
        return int(log(self.page_size, 2))

    @property
    def num_of_bits_addr(self):
        return int(self.num_of_bits_page + self.num_of_bits_offset)

    def init_tables(self):
        self.pages = []
        for program_number in range(self.num_programs):
            for page_number in range(self.num_of_pages):
                p = Page(page_number, program_number)
                self.pages.append(p)

    def to_binary(self, addr):
        ''' Helper method to get binary representation of addr '''
        bin_format = "0{}b".format(self.num_of_bits_addr)
        return format(addr, bin_format)

    def to_decimal(self, bin_number):
        ''' Helper method to get decimal repr of binary '''
        return int(bin_number, 2)
