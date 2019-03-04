#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Dict, Tuple

# rerunning is quite consistent!
from matplotlib import pyplot as plt # type: ignore
import matplotlib.ticker as tck # type: ignore

import seaborn as sns # type: ignore

# TODO jitter?
def plot_results(results_file: str, title, plot_name, maxdelay, maxerrors, step=10):
    results = json.loads(Path(results_file).read_text())
    rdict: Dict[Tuple[int, int], float] = {}
    for params, ress in results:
        res = float(ress.split()[0]) # TODO use the ±
        key = (params['delay'], params['errors'])
        if key in rdict:
            print(f"WARNING: duplicate {key}")
        else:
            rdict[key] = res

    sns.set(style='darkgrid')
    # sns.set_palette("husl")
    # https://seaborn.pydata.org/tutorial/color_palettes.html
    sns.set_palette("coolwarm", 50)
    plt.figure(figsize=(20, 10))
    plt.title(title)

    plt.xlabel('Errors')
    plt.gca().xaxis.set_major_locator(tck.MultipleLocator())

    plt.ylabel('Score')
    plt.gca().yaxis.set_major_locator(tck.MultipleLocator(20))

    for delay in range(0, maxdelay + step, step):
        errs = []
        vals = []
        for errors in range(maxerrors + 1):
            rr = rdict.get((delay, errors), None)
            if rr is None:
                continue # TODO warn?
            errs.append(errors)
            vals.append(rr)

            if errors == 0: # TODO ??
                plt.annotate(
                    str(delay),
                    xy=(-0.3, rr),
                    fontsize=8,
                )
        print(errs)
        print(vals)
        if len(errs) > 0:
            ints = int(delay / maxdelay * 255)
            hv = hex(ints)[2:]
            if len(hv) == 1:
                hv = "0" + hv
            # sns.scatterplot(errs, vals, label=f"{delay:3} ms", y_jitter=10)
            sns.lineplot(errs, vals, label=f"{delay:3} ms", linewidth=2) # , color='#{cc}0000'.format(cc=hv))



    plt.tight_layout()
    plt.savefig(plot_name)
    plt.show()


# plot_results(
#     results_visual_matching,
#     "Visual matching: dependency of score on errors and average delay (ms)",
#     'visual-matching.png',
#     maxdelay=1200,
#     maxerrors=12,
#     step=40,
# )

plot_results(
    'simple-reaction.json',
    "Simple reaction time: dependency of score on errors and average delay (ms)",
    'simple-reaction-time.png',
    maxdelay=280,
    maxerrors=19,
)
