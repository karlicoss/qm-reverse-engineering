#!/usr/bin/env python3
import common
import run
import plot
import js_scripts

MAX_ERRORS = 20

def run_sr():
    blocks = [
        (
            range(20, 100, 10),
            range(0, MAX_ERRORS + 1),
        ),
        (
            range(20, 400, 20),
            range(0, MAX_ERRORS + 1),
        ),
        (
            range(20, 800, 30),
            range(0, MAX_ERRORS + 1),
        ),
        (
            range(20, 1010, 40),
            range(0, MAX_ERRORS + 1),
        ),
        (
            range(20, 1010, 10),
            range(0, MAX_ERRORS + 1),
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
        "Simple reaction time: dependency of score on errors and reaction",
        'simple-reaction-time.png',
        delays=[
            *range(20, 200, 10),
            *range(200, 1010, 20),
        ],
        max_errors=MAX_ERRORS,
    )


def main():
    common.main(
        run=run_sr,
        plot=plot_sr,
    )

if __name__ == '__main__':
    main()
