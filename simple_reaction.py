#!/usr/bin/env python3
import common
import run
import plot
import js_scripts

SAMPLES = 20

def run_sr():
    blocks = [
        (
            range(20, 100, 110),
            range(0, SAMPLES + 1),
        ),
        (
            range(20, 400, 20),
            range(0, SAMPLES + 1),
        ),
        (
            range(20, 800, 30),
            range(0, SAMPLES + 1),
        ),
        (
            range(20, 1010, 40),
            range(0, SAMPLES + 1),
        ),
        (
            range(20, 1010, 10),
            range(0, SAMPLES + 1),
        ),
    ]

    for dell, errl in blocks:
        run.run_test(
            test_url='http://www.quantified-mind.com/tests/simple_reaction_time/practice',
            js_script_template=js_scripts.SIMPLE_REACTION_SCRIPT,
            delays=list(dell),
            errors=list(errl),
            state_file='simple-reaction.json',
        )


def plot_sr():
    plot.plot_results(
        'simple-reaction.json',
        "Simple reaction time: dependency of score on errors and average delay (ms)",
        'simple-reaction-time.png',
        maxdelay=800,
        maxerrors=20,
    )


def main():
    common.main(
        run=run_sr,
        plot=plot_sr,
    )

if __name__ == '__main__':
    main()
