

class Dispinfo(object):
    def __init__(self):
        self.power = '3'
        self.startposition = None  # TODO
        self.flags = 0
        self.elevation = 0
        self.subdiv = 0
        self.offsets = None  # TODO
        self.alphas = None  # TODO

    def __str__(self):
        out_str = '\t\t\tdispinfo\n\t\t\t{\n'
        out_str += f'\t\t\t\t\"power\"'
        # TODO
        return out_str
