from Block import Block


class Tlb:

    def __init__(self, num_line, subs, corr):
        self.num_line = num_line
        self.subs = subs
        self.corr = corr

        self.init_blocks()

    def init_blocks(self):
        self.blocks = []
        for i in range(self.num_line):
            b = Block(i)
            self.blocks.append(b)
