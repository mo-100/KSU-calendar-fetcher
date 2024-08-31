class ColorGenerator:
    def __init__(self):
        self.color_num = 0
        self.course_colors = {}

    def color_of(self, symbol: str) -> int:
        if symbol not in self.course_colors.keys():
            self.course_colors[symbol] = self.color_num
            self.color_num = (self.color_num + 1) % 12
        return self.course_colors[symbol]
