from Block import Block


class Marco(Block):
    ''' Marco that behaves like a Tlb block, it contains a page. This page can be
    assigned and removed'''

    def __init__(self, num_marco):
        Block.__init__(self, num_marco)
        self.on_disk = False

    def assign_page(self, page, iteration):
        super(Marco, self).assign_page(page, iteration)

        # Update reference in page, so Table of Pages can see if it has marco
        page.marco = self

    def __repr__(self):
        return "Marco({}, contains: {})".format(self.num_block, self.page_inside)
