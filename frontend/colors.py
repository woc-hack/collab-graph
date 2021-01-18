import sys
from typing import List

import matplotlib.pyplot as plt
import matplotlib.colors as c
import numpy as np


class Part:
    def __init__(self, from_n: int, to_n: int, from_color: str, to_color: str):
        self.from_n = from_n
        self.to_n = to_n
        self.from_color = from_color
        self.to_color = to_color


#  Create gradient colors according to colored parts
class Colored:
    def __init__(self, parts: List[Part]):
        self._parts = parts

    def get_color(self, current_value):
        h = self._parts[0].from_color
        for part in self._parts:
            if part.from_n <= current_value < part.to_n:
                h = color_fader(part.from_color, part.to_color,
                                (current_value - part.from_n) / (part.to_n - part.from_n))
                break
        print(h)
        r, g, b = tuple(int(round(col * 255)) for col in c.to_rgb(h))
        return f"              <viz:color r=\"{r}\" g=\"{g}\" b=\"{b}\"/>\n"

    def plot_gradient(self, step=500):
        fig, ax = plt.subplots(figsize=(8, 5))
        for i, part in enumerate(self._parts):
            for x in range(step):
                ax.axvline(i * step + x, color=color_fader(part.from_color, part.to_color, x / step), linewidth=4)
        plt.show()


authors_colored = Colored([Part(50, 150, '#040254', '#49a692'),
                           Part(150, 350, '#49a692', '#f9ffe0'),
                           Part(350, sys.maxsize, '#fff9c9', '#fff9c9')])

projects_colored = Colored([Part(50, 100, '#480266', '#910049'),
                            Part(100, 1000, '#910049', '#ffe330'),
                            Part(1000, 306900, '#fff9c9', '#fff9c9')])


# AuthorsColored = Colored([Part()])


def color_fader(c1, c2, mix=0.0):  # fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1 = np.array(c.to_rgb(c1))
    c2 = np.array(c.to_rgb(c2))
    return c.to_hex((1 - mix) * c1 + mix * c2)


# ptojects
c0 = '#480266'
c1 = '#910049'  # red
c2 = '#ffe330'  # yellow

# old_authors
# c1='#49a692' #dark blue
# c2='#f9ffe0' #yellow
#
c3 = '#fff9c9'
#
# c1_small = '#040254'
# c2_small = '#49a692'
#
# from_n = 50
# to_n = 200
# или 2000?




authors_colored.plot_gradient()
