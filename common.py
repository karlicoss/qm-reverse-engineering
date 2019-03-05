import argparse

def main(run, plot):
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=['run', 'plot'])
    args = p.parse_args()
    if args.mode == 'run':
        run()
    elif args.mode == 'plot':
        plot()
    else:
        raise AssertionError(args.mode)
