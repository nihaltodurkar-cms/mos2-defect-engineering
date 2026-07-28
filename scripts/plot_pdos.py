#!/usr/bin/env python3
"""Plot projected density of states from a Quantum ESPRESSO projwfc.x output file.

Usage:
    python plot_pdos.py output/pristine/Trial_2.pdos_tot --fermi 0.6716 -o pdos_pristine.png
"""
import argparse

import matplotlib.pyplot as plt
import numpy as np


def read_pdos_tot(path):
    data = np.loadtxt(path, comments="#")
    energy, dos, pdos = data[:, 0], data[:, 1], data[:, 2]
    return energy, dos, pdos


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdos_file", help="Path to a .pdos_tot file from projwfc.x")
    parser.add_argument("--fermi", type=float, default=0.0, help="Fermi energy in eV")
    parser.add_argument("--erange", type=float, nargs=2, default=(-6, 6),
                         help="Energy window relative to E_F")
    parser.add_argument("-o", "--output", default=None, help="Output image path")
    args = parser.parse_args()

    energy, dos, pdos = read_pdos_tot(args.pdos_file)
    x = energy - args.fermi

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, dos, color="0.4", lw=1.2, label="Total DOS")
    ax.plot(x, pdos, color="#d62728", lw=1.4, label="Projected DOS (sum)")
    ax.axvline(0.0, color="0.3", ls="--", lw=1)
    ax.set_xlim(*args.erange)
    ax.set_ylim(bottom=0)
    ax.set_xlabel(r"$E - E_F$ (eV)")
    ax.set_ylabel("DOS (states/eV)")
    ax.set_title("Projected density of states")
    ax.legend(frameon=False)
    fig.tight_layout()

    if args.output:
        fig.savefig(args.output, dpi=300)
        print(f"Saved figure to {args.output}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
