#!/usr/bin/env python3
"""Plot an electronic band structure from a QE plotband.x .gnu file.

The .gnu format is a sequence of (k-distance, energy) pairs, one band per
block, blocks separated by a blank line.

Usage:
    python plot_bands.py output/pristine/MoSt_band.gnu --fermi 0.6716 -o bands_pristine.png
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np


def read_bands(path):
    bands = []
    current = []
    with open(path) as f:
        for line in f:
            if line.strip() == "":
                if current:
                    bands.append(np.array(current))
                    current = []
                continue
            k, e = line.split()
            current.append((float(k), float(e)))
    if current:
        bands.append(np.array(current))
    return bands


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gnu_file", help="Path to a *.gnu band-structure file")
    parser.add_argument("--fermi", type=float, default=0.0, help="Fermi energy in eV")
    parser.add_argument("--erange", type=float, nargs=2, default=(-4, 4),
                         help="Energy window relative to E_F")
    parser.add_argument("-o", "--output", default=None, help="Output image path")
    args = parser.parse_args()

    bands = read_bands(args.gnu_file)

    fig, ax = plt.subplots(figsize=(5, 5))
    for band in bands:
        ax.plot(band[:, 0], band[:, 1] - args.fermi, color="#1f77b4", lw=0.8)
    ax.axhline(0.0, color="0.3", ls="--", lw=1)
    ax.set_xlim(bands[0][0, 0], bands[0][-1, 0])
    ax.set_ylim(*args.erange)
    ax.set_ylabel(r"$E - E_F$ (eV)")
    ax.set_xticks([])
    ax.set_title(f"Band structure ({len(bands)} bands)")
    fig.tight_layout()

    if args.output:
        fig.savefig(args.output, dpi=300)
        print(f"Saved figure to {args.output}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
