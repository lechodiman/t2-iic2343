from Block import Block


class Marco(Block):
    ''' Marco that behaves like a Tlb block, it contains a page. This can be
    assigned and removed'''

    def __init__(self, num_marco):
        Block.__init__(self, num_marco)

    def __repr__(self):
        return "Marco({}, contains: {})".format(self.num_block, self.page_inside)
