#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Dict, Tuple

# rerunning is quite consistent!
from matplotlib import pyplot as plt # type: ignore
import matplotlib.ticker as tck # type: ignore

import seaborn as sns # type: ignore

# TODO jitter?
def plot_results(results_file: str, title, plot_name, delays, max_errors):
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
    sns.set_palette("cool", len(delays))
    plt.figure(figsize=(20, 15))
    plt.title(title)

    plt.xlabel('Errors')
    plt.gca().xaxis.set_major_locator(tck.MultipleLocator(base=1))

    plt.ylabel('Score')
    # plt.gca().yaxis.set_major_locator(tck.MultipleLocator(base=step))

    for i, delay in enumerate(delays):
        errs = []
        vals = []
        for errors in range(max_errors + 1):
            rr = rdict.get((delay, errors), None)
            if rr is None:
                continue # TODO warn?
            errs.append(errors)
            vals.append(rr)

            if errors == 0: # TODO ??
                plt.annotate(
                    f'{delay:<4} ms',
                    xy=(-0.3, rr),
                    fontsize=8,
                    zorder=len(delays) + 1,
                )
        if len(errs) > 0:
            sns.lineplot(errs, vals, label=f"{delay:3} ms", linewidth=2, zorder=len(delays) - i)

    plt.legend(fontsize='x-small')
    plt.tight_layout()
    plt.savefig(plot_name)
    plt.show()
