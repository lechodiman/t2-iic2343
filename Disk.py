class Disk:

    def __init__(self, num_programs):
        self.backed_up_marcos = []
        self.num_programs = num_programs

    def receive_marco(self, marco):
        marco.on_disk = True
        marco.page_inside.on_disk = True

        self.backed_up_marcos.append(marco)

    def pop_marco_to_swap_in(self, page):
        for m in self.backed_up_marcos:
            if m.page_inside == page:
                # Remove from disk
                self.backed_up_marcos.remove(m)

                # Update on disk attr
                m.on_disk = False
                m.page_inside.on_disk = False

                # Return it
                return m

    def get_pages_on_disk(self, prog_index):
        pages_on_disk = 0
        for m in self.backed_up_marcos:
            if m.page_inside.program == prog_index:
                pages_on_disk += 1

        return pages_on_disk
