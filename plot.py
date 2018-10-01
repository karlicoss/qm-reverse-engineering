#!/usr/bin/env python3

# rerunning is quite consistent!
from matplotlib import pyplot as plt # type: ignore

import seaborn as sns # type: ignore

def plot_results(results, title, plot_name, maxdelay, maxerrors, step=20):
    sns.set(style='darkgrid')
    rdict = {}
    for r in results:
        key = (r['delay'], r['errors'])
        if key in rdict:
            print(f"WARNING: duplicate {r}")
        else:
            rdict[key] = r

    plt.figure(figsize=(20, 10))
    plt.title(title)
    plt.xlabel('Errors')
    plt.ylabel('Score')


    # sns.set_palette(sns.light_palette("green"))

    for delay in range(0, maxdelay + step, step):
        errs = []
        vals = []
        for errors in range(maxerrors + 1):
            rr = rdict.get((delay, errors), None)
            if rr is not None:
                res = float(rr['res'].split()[0])
                errs.append(errors)
                vals.append(res)
        if len(errs) > 0:
            ints = int(delay / maxdelay * 255)
            hv = hex(ints)[2:]
            if len(hv) == 1:
                hv = "0" + hv
            sns.lineplot(errs, vals, label=f"{delay:3} ms", linewidth=3, color='#{cc}0000'.format(cc=hv))


    plt.tight_layout()
    plt.savefig(plot_name)
    plt.show()

from results import results_visual_matching, results_simple_reaction
plot_results(
    results_visual_matching,
    "Visual matching: dependency of score on errors and average delay (ms)",
    'visual-matching.png',
    maxdelay=1200,
    maxerrors=12,
    step=40,
)

# plot_results(
#     results_simple_reaction,
#     "Simple reaction time: dependency of score on errors and average delay (ms)",
#     'simple-reaction-time.png',
#     maxdelay=700,
#     maxerrors=19,
# )
