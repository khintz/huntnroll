#!/usr/bin/env python3
import random
import sys


def pick_gaussian(names):
    n = len(names)
    if n == 0:
        raise ValueError("No names provided.")
    # Centered mean, stddev covers about 2/3 of the list
    mu = (n - 1) / 2
    sigma = n / 4
    while True:
        idx = int(random.gauss(mu, sigma) + 0.5)
        if 0 <= idx < n:
            return names[idx]


def main():
    if len(sys.argv) > 1:
        names = sys.argv[1:]
    else:
        names = input("Enter names separated by commas: ").split(",")
        names = [name.strip() for name in names if name.strip()]
    if not names:
        print("No names provided.")
        sys.exit(1)
    winner = pick_gaussian(names)
    print(f"Selected to start: {winner}")


if __name__ == "__main__":
    main()
