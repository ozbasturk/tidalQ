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
