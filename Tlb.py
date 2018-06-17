from Block import Block
from math import log


class Tlb:

    def __init__(self, num_line, subs, corr, num_programs):
        self.num_line = num_line
        self.subs = subs
        self.corr = corr

        # Stats
        self.hits = 0

        # Stores hits for every program
        self.hit_stats = {num: 0 for num in range(num_programs)}

        self.init_blocks()

    @property
    def num_of_bits_block(self):
        return int(log(self.num_line, 2))

    @property
    def is_empty(self):
        bool_set = {b.is_empty for b in self.blocks}

        return len(bool_set) == 1 and bool_set == {True}

    def __repr__(self):
        msg = "\n\t TLB subs: {}, corr: {}\n\n".format(self.subs, self.corr)

        for b in self.blocks:
            msg += "Entrada(Block) {} ".format(b.num_block)
            msg += "- Pagina virtual {}".format(repr(b.page_inside))
            msg += "- LRU: {} ".format(b.last_used_time)
            msg += "- LFU: {} ".format(b.times_used)
            msg += "- FIFO: {} ".format(b.insertion_time)
            msg += "\n"

        return msg

    def init_blocks(self):
        self.blocks = []
        for i in range(self.num_line):
            b = Block(i)
            self.blocks.append(b)

    def get_page(self, page_number, program, iteration):
        ''' Returns page if found, else returns None'''
        for b in self.blocks:
            page = b.get_page()
            if page and page.number == page_number and page.program == program:
                print("[TLB] Hubo HIT. {}".format(self.subs))
                self.hit_stats[program] += 1

                # Update counters of block
                b.last_used_time = iteration
                b.times_used += 1

                return page

        print("[TLB NO hubo HIT] get_page de TLB returns None")
        return None

    def clear(self):
        if self.is_empty:
            print("[TLB] TLB ya está vacía y necesita ser limpiada.")
            return

        # else (TLB no está vacía)
        print("[TLB] Limpiando TLB")
        for b in self.blocks:
            b.remove_page()

    def add_page(self, page, page_digits, iteration):
        ''' Adds page to a block according to corr and subs'''

        if self.corr == "DM":
            # Get block number, add to specific block

            # block_number = int(page_digits[:self.num_of_bits_block])
            block_number = int(page_digits[::-1][:self.num_of_bits_block][::-1], 2)
            block = self.blocks[block_number]

            # Remove current page
            block.remove_page()

            # Assign new page
            block.assign_page(page, iteration)

            print("""[Sustitucion TLB] DM Se vacio el bloque: {}""".format(block.num_block))

        elif self.corr == "FA":
            # Look for an available block
            available_block = None
            for b in self.blocks:
                if b.is_empty:
                    available_block = b

            # If there is no available block, replace one
            if not available_block:
                if self.subs == "FIFO":
                    # Replace with block with min insertion time
                    block_min_insertion_time = self.blocks[0]
                    for b in self.blocks:
                        if b.insertion_time < block_min_insertion_time.insertion_time:
                            block_min_insertion_time = b

                    block_to_replace = block_min_insertion_time

                elif self.subs == "LRU":
                    # Replace with block with min time of last usage
                    block_min_time = self.blocks[0]
                    for b in self.blocks:
                        if b.last_used_time < block_min_time.last_used_time:
                            block_min_time = b

                    block_to_replace = block_min_time

                elif self.subs == "LFU":
                    # Replace with block with least times used
                    block_least_used = self.blocks[0]
                    for b in self.blocks:
                        if b.times_used < block_least_used.times_used:
                            block_least_used = b

                    block_to_replace = block_least_used

                print("""[Sustitucion TLB] {},
                 se va la entrada de bloque {}""".format(self.subs,
                                                         block_to_replace.num_block))

                # Remove current page
                block_to_replace.remove_page()

                # Now it becomes available
                available_block = block_to_replace

            # Use available block to put in the page
            available_block.assign_page(page, iteration)
