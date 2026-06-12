**

# Tidal Interaction Calculator

A modern, object-oriented Python tool for computing the reduced tidal quality factor ($Q'_*$) and associated orbital evolution timescales for a star in tidal interaction with a close-in planet.

## Overview

This module processes the physical properties of a star-planet system alongside the quadratic coefficients of transit timing variations (TTVs) to calculate:
* The rate of change in the orbital period ($dP/dE$, $dP/dt$, $\dot{P}$).
* The reduced stellar tidal quality factor ($Q'_*$) and its corresponding lower limits at 95% or 99% confidence levels.
* Characteristic timescales for orbital decay and orbital circularization.
* Expected mid-transit time ($T_0$) shifts over user-defined baselines.

The code features an object-oriented design and is fully automated to handle formal error propagation natively, eliminating the need for manual uncertainty calculations.

## Requirements

This code utilizes standard Python 3.x libraries (`math`, `typing`) alongside the following external packages:
* **`astropy`**: Used for fetching high-precision physical constants (e.g., $M_J$, $M_\odot$, $R_\odot$, au).
* **`uncertainties`**: Handles transparent and rigorous linear error propagation across all mathematical operations.

To install the required dependencies, run:
```bash
pip install astropy uncertainties
```

## References and Methodology

The physical formalism and calculations implemented in this code are derived from the following literature:

* **Tidal Quality Factor ($Q$) Formalism:** * Goldreich, P., & Soter, S. (1966). *Q in the Solar System*. Icarus, 5(1-6), 375-389.
* **Tidal Dissipation & System Equations:** * Ogilvie, G. I. (2014). *Tidal dissipation in stars and giant planets*. Annual Review of Astronomy and Astrophysics, 52, 171-210.
* **Transit Timing Variations & Orbital Decay Modeling:** * Patra, A. K., et al. (2017). *The apparently decaying orbit of WASP-12b*. The Astronomical Journal, 154(1), 4.
  * Maciejewski, G., et al. (2018). *Apparent transit timing variations for the hot Jupiter WASP-4b*.
  * Mancini, L., et al. (2022). *The GAPS Programme with HARPS-N at TNG*.
* **Timescales:** * Siverd, R. J., et al. (2012). *KELT-1b: A Strongly Irradiated, Highly Inflated, Short Period, 27 Jupiter-mass Companion Transiting a Mid-F Star*.
  * Mazeh, T. (2008). *Observational evidence for tidal interaction in close binary systems*.

## Citation

If you utilize this code or its methodology in your research, please consider citing the following foundational papers from our group:

* Baştürk, Ö., et al. (2022, 2023, or 2025)
* Yalçınkaya, S., et al. (2024) and  Kutluay, A., et al. (2026) used the same code as well.

## Author

**Özgür Baştürk** 
Ankara University
Professor of Astronomy and Astrophysics
