class Page:

    def __init__(self, number, program):
        self.number = number
        self.program = program
        self.marco = None
        self.marco_on_disk = None

    @property
    def has_marco(self):
        return self.marco is not None

    def __eq__(self, other):
        return self.number == other.number and self.program == other.program

    def __repr__(self):
        msg = "Page({}, {})".format(self.number, self.program)

        return msg
