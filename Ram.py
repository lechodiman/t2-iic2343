from Marco import Marco


class Ram:

    def __init__(self, mem_fis_size, page_size, subtitution):
        self.mem_fis_size = mem_fis_size
        self.page_size = page_size
        self.subtitution = subtitution

        self.init_marcos()

    @property
    def num_of_marcos(self):
        return int(self.mem_fis_size / self.page_size)

    def init_marcos(self):
        self.marcos = []
        for num_of_marco in range(self.num_of_marcos):
            m = Marco(num_of_marco)
            self.marcos.append(m)
