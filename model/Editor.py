class Editor(object):
    def __init__(self):
        self.color = '0 143 192'
        self.visgroupshown = 1
        self.visgroupautoshown = 1

    def __str__(self):
        out_str = 'editor\n\t\t{\n'
        out_str += f'\t\t\t\"color\" \"{self.color}\"\n'
        out_str += f'\t\t\t\"visgroupshown\" \"{self.visgroupshown}\"\n'
        out_str += f'\t\t\t\"visgroupautoshown\" \"{self.visgroupautoshown}\"\n'
        out_str += '\t\t}\n'
        return out_str
