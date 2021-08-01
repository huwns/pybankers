"""CLI Executable"""

import argparse

from .analyze_bankers import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bankers Analysis Tool')
    parser.prog = 'python -m bankers'
    parser.add_argument('max_count', type=int, help='max steps count')
    args = parser.parse_args()
    main(args.max_count)
