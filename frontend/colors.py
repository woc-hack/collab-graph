import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as c
import numpy as np


def colorFader(c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(c.to_rgb(c1))
    c2=np.array(c.to_rgb(c2))
    return c.to_hex((1-mix)*c1 + mix*c2)

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
        h = colorFader(c1_small, c2_small, (size - 30) / 970)
    elif 150 <= size < 400:
        h = colorFader(c1, c2, (size - 30) / 970)
    else:
        h = c3
    print(h)
    # h = h.lstrip("#")
    r, g, b = tuple(int(round(col * 255)) for col in c.to_rgb(h))
    return f"              <viz:color r=\"{r}\" g=\"{g}\" b=\"{b}\"/>\n"


n = 500
fig, ax = plt.subplots(figsize=(8, 5))
for x in range(n+1):
    ax.axvline(x, color=colorFader(c1,c2,x/n), linewidth=4)
for x in range(100):
    ax.axvline(n+1+x, color=c3, linewidth=4)

plt.show()

