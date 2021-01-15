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
    def __init__(self, parts: List[Part], min_value: int, max_value: int):
        self._parts = parts
        self._min_value = min_value
        self._max_value = max_value

    def get_color(self, current_value):
        h = self._parts[0].from_color
        for part in self._parts:
            if part.from_n <= current_value < part.to_n:
                h = color_fader(part.from_color, part.to_color, (current_value - self._min_value) / self._max_value)
                break
        print(h)
        r, g, b = tuple(int(round(col * 255)) for col in c.to_rgb(h))
        return f"              <viz:color r=\"{r}\" g=\"{g}\" b=\"{b}\"/>\n"


ProjectsColored = Colored([Part(50, 150, '#040254', '#49a692'),
                           Part(150, 400, '#49a692', '#f9ffe0'),
                           Part(400, 10000000, '#fff9c9', '#fff9c9')],
                          30, 970)

# AuthorsColored = Colored([Part()])


def color_fader(c1, c2, mix = 0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(c.to_rgb(c1))
    c2=np.array(c.to_rgb(c2))
    return c.to_hex((1 - mix) * c1 + mix * c2)

# ptojects
# c1='#910049' #red
# c2='#ffe330' #yellow

# authors
c1='#49a692' #dark blue
c2='#f9ffe0' #yellow

c3='#fff9c9'

c1_small = '#040254'
c2_small = '#49a692'

from_n = 50
to_n = 200
# или 2000?


def get_color(size):
    if 50 <= size < 150:
        # not really sure what is (size - 30) / 970
        h = color_fader(c1_small, c2_small, (size - 30) / 970)
    elif 150 <= size < 400:
        h = color_fader(c1, c2, (size - 30) / 970)
    else:
        h = c3
    print(h)
    r, g, b = tuple(int(round(col * 255)) for col in c.to_rgb(h))
    return f"              <viz:color r=\"{r}\" g=\"{g}\" b=\"{b}\"/>\n"


n = 500
fig, ax = plt.subplots(figsize=(8, 5))
for x in range(n+1):
    ax.axvline(x, color=color_fader(c1, c2, x / n), linewidth=4)
for x in range(100):
    ax.axvline(n+1+x, color=c3, linewidth=4)

plt.show()

