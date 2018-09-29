#!/usr/bin/env python3

# rerunning is quite consistent!

results =[
{"delay":   20, "errors":   0, "res": "450.576 ± 74.912"},
{"delay":   20, "errors":   1, "res": "395.277 ± 64.783"},
{"delay":   20, "errors":   2, "res": "352.694 ± 57.509"},
{"delay":   20, "errors":   3, "res": "318.542 ± 51.988"},
{"delay":   20, "errors":   4, "res": "290.148 ± 47.828"},
{"delay":   20, "errors":   5, "res": "265.740 ± 44.690"},
{"delay":   50, "errors":   0, "res": "599.129 ± 272.80"},
{"delay":   50, "errors":   1, "res": "395.412 ± 65.463"},
{"delay":   50, "errors":   2, "res": "352.694 ± 57.509"},
{"delay":   50, "errors":   3, "res": "318.542 ± 51.988"},
{"delay":   50, "errors":   4, "res": "290.148 ± 47.828"},
{"delay":   50, "errors":   5, "res": "265.740 ± 44.690"},
{"delay":  100, "errors":   0, "res": "961.668 ± 27.175"},
{"delay":  100, "errors":   1, "res": "950.700 ± 29.445"},
{"delay":  100, "errors":   2, "res": "801.248 ± 250.57"},
{"delay":  100, "errors":   3, "res": "319.349 ± 56.490"},
{"delay":  100, "errors":   4, "res": "290.149 ± 47.833"},
{"delay":  100, "errors":   5, "res": "265.740 ± 44.690"},
{"delay":  200, "errors":   0, "res": "744.067 ± 27.148"},
{"delay":  200, "errors":   1, "res": "737.056 ± 27.795"},
{"delay":  200, "errors":   2, "res": "720.675 ± 28.486"},
{"delay":  200, "errors":   3, "res": "712.171 ± 29.235"},
{"delay":  200, "errors":   4, "res": "696.689 ± 30.041"},
{"delay":  200, "errors":   5, "res": "680.923 ± 30.916"},
{"delay":  400, "errors":   0, "res": "321.779 ± 24.836"},
{"delay":  400, "errors":   1, "res": "317.443 ± 25.249"},
{"delay":  400, "errors":   2, "res": "313.171 ± 25.682"},
{"delay":  400, "errors":   3, "res": "306.847 ± 26.092"},
{"delay":  400, "errors":   4, "res": "298.687 ± 26.475"},
{"delay":  400, "errors":   5, "res": "289.485 ± 26.843"},
]

from matplotlib import pyplot as plt # type: ignore

import seaborn as sns # type: ignore
sns.set(style='darkgrid')

errcounts = [0, 1, 2, 3, 4, 5]

sns.set_palette(sns.light_palette("green"))
for delay in [20, 50, 100, 200, 400]:
    vals = []
    for errors in errcounts:
        [rr] = [r for r in results if r['delay'] == delay and r['errors'] == errors]
        res = float(rr['res'].split()[0])
        vals.append(res)
    sns.lineplot(errcounts, vals, label=f"delay {delay:3}")


plt.show()
