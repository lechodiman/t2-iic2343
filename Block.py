class Block:

    def __init__(self, num_block):
        self.num_block = num_block
        self.page_inside = None

    @property
    def is_empty(self):
        return self.page_inside is None

    def assign_page(self, page):
        self.page_inside = page

    def remove_page(self):
        self.page_inside = None

    def __repr__(self):
        return "Block({}, contains: {})".format(self.num_block, self.page_inside)
