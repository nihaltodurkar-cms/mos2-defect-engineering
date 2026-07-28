#!/usr/bin/env python3
"""Summarize Bader charge analysis (ACF.dat, from the Henkelman group's Bader
code run on a QE pp.x charge density) on a per-species basis.

ATOMIC_POSITIONS in the QE input lists atoms grouped by species in a fixed
order, and ACF.dat preserves that atom ordering, so species are recovered
by supplying the atom count for each species in the same order.

Usage:
    python bader_summary.py output/pristine/ACF.dat --species Mo:16 S:32
"""
import argparse

import numpy as np


def read_acf(path):
    charges = []
    with open(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) == 7 and parts[0].isdigit():
                charges.append(float(parts[4]))
    return np.array(charges)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("acf_file", help="Path to an ACF.dat file")
    parser.add_argument("--species", nargs="+", required=True,
                         help="Species:count pairs in atom order, e.g. Mo:16 S:32")
    parser.add_argument("--valence", nargs="+", default=[],
                         help="Optional Species:valence_electrons pairs to report "
                              "net charge transfer, e.g. Mo:6 S:6")
    args = parser.parse_args()

    charges = read_acf(args.acf_file)
    species = [s.split(":") for s in args.species]
    species = [(name, int(count)) for name, count in species]
    valence = dict(s.split(":") for s in args.valence)

    total_atoms = sum(count for _, count in species)
    if total_atoms != len(charges):
        raise SystemExit(
            f"Species counts sum to {total_atoms} but ACF.dat has {len(charges)} atoms"
        )

    print(f"{'Species':<10}{'N':>4}{'Mean Bader charge (e)':>26}{'Net transfer (e)':>20}")
    idx = 0
    for name, count in species:
        block = charges[idx: idx + count]
        idx += count
        mean_q = block.mean()
        transfer = ""
        if name in valence:
            transfer = f"{float(valence[name]) - mean_q:+.4f}"
        print(f"{name:<10}{count:>4}{mean_q:>26.4f}{transfer:>20}")


if __name__ == "__main__":
    main()
