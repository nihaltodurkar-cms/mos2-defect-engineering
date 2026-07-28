# Defect Engineering in Monolayer MoS₂

[![Code](https://img.shields.io/badge/DFT%20code-Quantum%20ESPRESSO-1f425f)](https://www.quantum-espresso.org/)
[![Functional](https://img.shields.io/badge/XC%20functional-PBE-blue)](#computational-methodology)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/analysis-Python%203-3776AB)](requirements.txt)

A first-principles (DFT) study of how intrinsic point defects — starting with
the single sulfur vacancy — perturb the electronic structure of monolayer
MoS₂, using plane-wave pseudopotential DFT as implemented in Quantum ESPRESSO.

## Abstract

Monolayer MoS₂ is a direct-gap semiconductor of interest for
next-generation transistors, photodetectors, and catalysis, but its
properties in real devices are strongly modified by intrinsic defects
introduced during synthesis — chalcogen vacancies chief among them. This
repository documents a reproducible DFT workflow that (1) relaxes and
characterizes pristine monolayer MoS₂, (2) introduces a single sulfur
vacancy in a 4×4 supercell, and (3) compares the resulting total/projected
density of states, band structure, and Bader charge distribution against
the pristine reference to quantify the defect's electronic signature.

## Computational Methodology

| Parameter | Value |
|---|---|
| Code | Quantum ESPRESSO (`pw.x`, `dos.x`, `projwfc.x`, `bands.x`, Bader charge analysis) |
| Exchange-correlation | PBE (GGA), ultrasoft pseudopotentials |
| Pseudopotentials | `mo_pbe_v1.uspp.F.UPF`, `s_pbe_v1.4.uspp.F.UPF` |
| Supercell | 4×4×1 monolayer, ~15 Å vacuum along *c* |
| System size | 48 atoms (pristine), 47 atoms (single S vacancy) |
| Plane-wave cutoffs | `ecutwfc` = 55–65 Ry, `ecutrho` = 500 Ry |
| k-point sampling | 12×12×1 (SCF), 6×6×1 (relaxation / NSCF) |
| Convergence | Force < 1×10⁻⁴ Ry/bohr, energy < 1×10⁻¹⁰ Ry |
| Defect calculations | Spin-polarized (`nspin=2`), Fermi–Dirac smearing (`degauss=0.005` Ry) |

Exact parameters for every calculation are in the corresponding `input/*.in`
files — nothing above is hard-coded elsewhere, so the table is a summary,
not the source of truth.

## Repository Structure

```
input/
  pristine/       QE input files: relax, SCF, NSCF, DOS, PDOS, bands, charge density
  1S_vacancy/     Same workflow for the single sulfur vacancy defect
pseudopotentials/ PBE ultrasoft pseudopotentials (Mo, S)
output/
  pristine/       QE output logs + post-processing data (.dos, .pdos_tot, bands.dat, ACF.dat, avg.dat)
  1S_vacancy/     Same, for the defect supercell
scripts/          Python post-processing: DOS, PDOS, band structure, Bader charge summary
requirements.txt  Python dependencies for scripts/
```

## Reproducing the Calculations

Each stage is run with the corresponding QE binary against the `.in` file
of the same name, using outputs from the previous stage (`relax` → `scf` →
`nscf`/`dos`/`projwfc`/`bands`):

```bash
pw.x     < input/pristine/MoSt_relax.in    > output/pristine/MoSt_relax.out
pw.x     < input/pristine/MoSt_scf.in      > output/pristine/MoSt_scf.out
pw.x     < input/pristine/MoSt_nscf.in     > output/pristine/MoSt_nscf.out
dos.x    < input/pristine/MoSt_dos.in      > output/pristine/MoSt_dos.out
projwfc.x< input/pristine/MoSt_projwfc.in  > output/pristine/MoSt_projwfc.out
pw.x     < input/pristine/MoSt_bands.in    > output/pristine/MoSt_bands.out
```

The same sequence applies under `input/1S_vacancy/` with the `MoSt_1V_*`
input files. `outdir`/`pseudo_dir` paths in the `.in` files are absolute and
should be edited to match your local environment before running.

### Post-processing

```bash
pip install -r requirements.txt

python scripts/plot_dos.py    output/pristine/Trial_2.dos      --fermi 0.6716 -o dos_pristine.png
python scripts/plot_pdos.py   output/pristine/Trial_2.pdos_tot --fermi 0.6716 -o pdos_pristine.png
python scripts/plot_bands.py  output/pristine/MoSt_band.gnu    --fermi 0.6716 -o bands_pristine.png
python scripts/bader_summary.py output/pristine/ACF.dat --species Mo:16 S:32 --valence Mo:14 S:6
```

## Results Summary

| Quantity | Pristine | Single S vacancy |
|---|---|---|
| Total energy | −3003.724 Ry | −2979.427 Ry |
| Kohn–Sham gap (HOMO/LUMO, no SOC) | 1.61 eV (0.6716 → 2.2809 eV) | Fermi level pinned in-gap at 1.1663 eV by defect states |
| Ground state magnetization | — | 0.00 μ_B/cell (non-magnetic, despite spin-polarized setup) |
| Net Bader charge transfer, Mo / S | +1.18 e / −0.59 e | +1.17 e / −0.61 e |

The sulfur vacancy introduces localized in-gap states that pin the Fermi
level well inside the pristine gap, consistent with the well-known role of
chalcogen vacancies as deep trap states in MoS₂. Full DOS/PDOS/band-structure
data for both systems are under `output/`, and can be regenerated as figures
with the scripts above.

## Roadmap

- [x] Pristine monolayer MoS₂: relaxation, SCF/NSCF, DOS, PDOS, bands, Bader charges
- [x] Single sulfur vacancy: same characterization pipeline
- [ ] Sulfur di-vacancy and antisite defects
- [ ] Substitutional doping (e.g. Nb, Re) at the Mo site
- [ ] Defect formation energies as a function of chemical potential

## Citation

If this repository is useful in your own work, please cite it — see
[`CITATION.cff`](CITATION.cff).

## License

Released under the [MIT License](LICENSE).

## Author

**Nihal Todurkar**
B.Tech, Metallurgical and Materials Engineering
National Institute of Technology Karnataka (NITK), Surathkal
