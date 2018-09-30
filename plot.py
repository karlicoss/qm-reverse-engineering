#!/usr/bin/env python3

# rerunning is quite consistent!
from matplotlib import pyplot as plt # type: ignore

import seaborn as sns # type: ignore
sns.set(style='darkgrid')

from results import results

errcounts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
delays = [
    20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200,
    210, 220, 230, 240, 250, 260, 270, 280, 290,
    300, 350, 400,
]

rdict = {}
for r in results:
    key = (r['delay'], r['errors'])
    if key in rdict:
        print(f"WARNING: duplicate {r}")
    else:
        rdict[key] = r

plt.figure(figsize=(20, 10))
plt.title('Simple reaction time: dependency of score on errors and average delay (ms)')
plt.xlabel('Errors')
plt.ylabel('Score')


# sns.set_palette(sns.light_palette("green"))
mdelay = 700
for delay in range(0, mdelay + 10, 20):
    errs = []
    vals = []
    for errors in errcounts:
        rr = rdict.get((delay, errors), None)
        if rr is not None:
            res = float(rr['res'].split()[0])
            errs.append(errors)
            vals.append(res)
    if len(errs) > 0:
        ints = int(delay / mdelay * 255)
        hv = hex(ints)[2:]
        if len(hv) == 1:
            hv = "0" + hv
        sns.lineplot(errs, vals, label=f"delay {delay:3}", linewidth=3, color='#{cc}0000'.format(cc=hv))


plt.tight_layout()
plt.savefig('simple-reaction-time.png')
plt.show()
