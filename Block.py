class Block:

    def __init__(self, num_block):
        self.num_block = num_block
        self.page_inside = None

        # Replacement counters
        # Stores insertion time (FIFO)
        self.insertion_time = 0

        # Stores last used time (LRU)
        self.last_used_time = 0

        # Stores how many times it was used (LFU)
        self.times_used = 0

    @property
    def is_empty(self):
        return self.page_inside is None

    def assign_page(self, page, iteration):
        self.page_inside = page

        # Update counters
        self.insertion_time = iteration
        self.last_used_time = iteration
        self.times_used += 1

    def remove_page(self):
        self.page_inside = None

        # Reset counters
        self.insertion_time = 0
        self.last_used_time = 0
        self.times_used = 0

    def get_page(self):
        return self.page_inside

    def __repr__(self):
        return "Block({}, contains: {})".format(self.num_block, self.page_inside)
