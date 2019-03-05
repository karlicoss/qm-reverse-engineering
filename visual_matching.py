#!/usr/bin/env python3
import common
import run
import plot
import js_scripts

SAMPLES = 16

def run_vm():
    blocks = [
        (
            # ok, so my delay was 742 on average... so let's do from 20 to 1000 in steps of 20?
            range(20, 1200, 20),
            range(0, SAMPLES + 1),
        ),
        (
            range(30, 1200, 20),
            range(0, SAMPLES + 1),
        ),
    ]
    for dell, errl in blocks:
        run.run_test(
            test_url="http://www.quantified-mind.com/tests/feature_match/practice",
            js_script_template=js_scripts.VISUAL_MATCHING_SCRIPT,
            delays=list(dell),
            errors=list(errl),
            state_file='visual-matching.json',
        )

def plot_vm():
    plot.plot_results(
        'visual-matching.json',
        "Visual matching: dependency of score on errors and average delay (ms)",
        'visual-matching.png',
        maxdelay=1200,
        maxerrors=12,
        step=40,
    )

def main():
    common.main(
        run=run_vm,
        plot=plot_vm,
    )

if __name__ == '__main__':
    main()
