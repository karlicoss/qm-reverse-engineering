#!/usr/bin/env python3

# rerunning is quite consistent!
from matplotlib import pyplot as plt # type: ignore

import seaborn as sns # type: ignore
sns.set(style='darkgrid')

from results import results

errcounts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
delays = [
    20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200,
    210, 220, 230, 240, 250, 260, 270, 280, 290,
    300, 350, 400,
]

# sns.set_palette(sns.light_palette("green"))
for delay in delays:
    vals = []
    for errors in errcounts:
        rr = [r for r in results if r['delay'] == delay and r['errors'] == errors]
        if len(rr) > 1:
            print(f"WARNING! multiple {rr}")
        res = float(rr[0]['res'].split()[0])
        vals.append(res)
    ints = int(delay / max(delays) * 255)
    hv = hex(ints)[2:]
    if len(hv) == 1:
        hv = "0" + hv
    sns.lineplot(errcounts, vals, label=f"delay {delay:3}", linewidth=3, color='#{cc}0000'.format(cc=hv))


plt.show()
