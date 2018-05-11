class Page:

    def __init__(self, number, program):
        self.number = number
        self.program = program

    def __eq__(self, other):
        return self.number == other.number and self.program == other.program

    def __repr__(self):
        msg = "Page({}, {})".format(self.number, self.program)

        return msg
