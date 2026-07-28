#!/usr/bin/env python3
"""Plot total density of states from a Quantum ESPRESSO dos.x output file.

Usage:
    python plot_dos.py output/pristine/Trial_2.dos -o dos_pristine.png
    python plot_dos.py output/1S_vacancy/Trial_4.dos --fermi 1.1663
"""
import argparse
import re

import matplotlib.pyplot as plt
import numpy as np


def read_dos(path):
    fermi = None
    with open(path) as f:
        header = f.readline()
        match = re.search(r"EFermi\s*=\s*([-\d.]+)", header)
        if match:
            fermi = float(match.group(1))
    data = np.loadtxt(path, comments="#")
    energy, dos, idos = data[:, 0], data[:, 1], data[:, 2]
    return energy, dos, idos, fermi


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dos_file", help="Path to a .dos file from dos.x")
    parser.add_argument("--fermi", type=float, default=None,
                         help="Fermi energy in eV (overrides value parsed from file header)")
    parser.add_argument("--erange", type=float, nargs=2, default=(-6, 6),
                         help="Energy window relative to E_F, e.g. --erange -6 6")
    parser.add_argument("-o", "--output", default=None, help="Output image path")
    args = parser.parse_args()

    energy, dos, idos, parsed_fermi = read_dos(args.dos_file)
    fermi = args.fermi if args.fermi is not None else (parsed_fermi or 0.0)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(energy - fermi, dos, color="#1f77b4", lw=1.4)
    ax.axvline(0.0, color="0.3", ls="--", lw=1, label=r"$E_F$")
    ax.fill_between(energy - fermi, dos, where=(energy - fermi) <= 0,
                     color="#1f77b4", alpha=0.15)
    ax.set_xlim(*args.erange)
    ax.set_ylim(bottom=0)
    ax.set_xlabel(r"$E - E_F$ (eV)")
    ax.set_ylabel("DOS (states/eV)")
    ax.set_title("Total density of states")
    ax.legend(frameon=False)
    fig.tight_layout()

    if args.output:
        fig.savefig(args.output, dpi=300)
        print(f"Saved figure to {args.output}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
