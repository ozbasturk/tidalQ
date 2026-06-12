"""
Tidal Interaction Calculator

Computes the tidal quality factor and associated timescales for a star 
in tidal interaction with a close-in planet, based on Ogilvie (2014).
"""

from typing import Tuple, Optional
from math import pi
from uncertainties import ufloat
from astropy import constants as const

# Physical Constants
M_JUP = const.M_jup.value
M_SUN = const.M_sun.value
R_SUN = const.R_sun.value
AU = const.au.value / 1e3


class TidalInteraction:
    """
    Calculates tidal quality factors and orbital evolution timescales for a
    star-planet system.

    Parameters
    ----------
    planet_name : str
        Name of the planet.
    a_quad : tuple of float
        Quadratic coefficient of the best-fitting 2-degree polynomial and its error (value, error).
    p_orb : tuple of float
        Orbital period in days and its error (value, error).
    m_p : tuple of float
        Planetary mass in Jupiter masses and its error (value, error).
    m_s : tuple of float
        Stellar mass in solar masses and its error (value, error).
    a_div_rs : tuple of float
        Ratio of semi-major axis to stellar radius (a/R*) and its error (value, error).
    a5p : float, optional
        The 5th percentile for the quadratic coefficient. If None, it is calculated
        to a 99% confidence level (value - 2.33 * error).
    """

    def __init__(
        self,
        planet_name: str,
        a_quad: Tuple[float, float],
        p_orb: Tuple[float, float],
        m_p: Tuple[float, float],
        m_s: Tuple[float, float],
        a_div_rs: Tuple[float, float],
        a5p: Optional[float] = None,
    ):
        self.planet_name = planet_name

        # Initialize uncertainties objects
        self.a_quad_val, self.a_quad_err = a_quad
        self.p_orb = ufloat(*p_orb)

        # Convert masses to kg
        self.m_p = ufloat(m_p[0] * M_JUP, m_p[1] * M_JUP)
        self.m_s = ufloat(m_s[0] * M_SUN, m_s[1] * M_SUN)

        self.a_div_rs = ufloat(*a_div_rs)

        # Calculate derived geometries
        self.rs_div_a = 1 / self.a_div_rs

        # Determine 5th percentile for lower limits
        if a5p is not None:
            self.a5p = float(a5p)
        else:
            # 99% confidence level
            self.a5p = self.a_quad_val - 2.33 * self.a_quad_err

        # Compute period derivatives
        self._calculate_derivatives()

    def _calculate_derivatives(self):
        """Calculates the change in orbital period (dP/dE, dP/dt, Pdot)."""
        # Best-fitting quadratic function
        self.dp_de = ufloat(2 * self.a_quad_val, 2 * self.a_quad_err)

        # Lower limit for inferior quadratic fit
        self.dp_de_lower = ufloat(2 * self.a5p, 2 * self.a_quad_err)

        self.dp_dt = self.dp_de / self.p_orb
        self.p_dot = self.dp_dt * 86400 * 365.25

    def _qred_star(self, dp_de_val) -> float:
        """
        Internal method to compute the reduced tidal quality factor.
        """
        qred = (
            (27 / 2 * pi * (self.m_p / self.m_s) * (self.rs_div_a**5))
            * self.p_orb
            / dp_de_val
        )
        return abs(qred)

    @property
    def qs_red(self):
        """Reduced tidal quality factor."""
        return self._qred_star(self.dp_de)

    @property
    def qs_red_lower(self):
        """Lower limit for the reduced quality factor (95% confidence)."""
        return self._qred_star(self.dp_de_lower)

    @property
    def t_decay(self):
        """Time in years until the orbit shrinks to zero."""
        return abs(self.p_orb**2 / self.dp_de / 365.25)

    @property
    def tau_decay(self):
        """Characteristic timescale for orbital decay in years (Siverd et al. 2012)."""
        tau = abs(
            1
            / (12 * pi)
            * self.qs_red
            * (self.m_s / self.m_p)
            * self.a_div_rs**5
            * self.p_orb
        )
        return tau / 365.25

    @property
    def tau_circ(self):
        """Circularization time in years (Mazeh 2008)."""
        qp_kp = 1e5  # Canonical value for planets
        tau = abs(
            self.p_orb
            / (21 * pi)
            * qp_kp
            * (self.m_p / self.m_s)
            * self.a_div_rs**5
            / 365.25
        )
        return tau

    def calculate_t0_shift(self, years: float = 10.0, q_val: Optional[float] = None):
        """
        Calculates the shift in mid-transit time over a given number of years.

        Parameters
        ----------
        years : float
            The timespan in years over which to calculate the shift.
        q_val : float, optional
            A specific Q value to use (e.g., 1e6 for canonical Maciejewski et al. 2018).
            If None, uses the calculated self.qs_red.
        """
        q_factor = q_val if q_val is not None else self.qs_red
        shift = abs(
            27
            / 4
            * pi
            / q_factor
            * (self.m_p / self.m_s)
            * (self.rs_div_a) ** 5
            * (1 / (self.p_orb / 365.25))
            * years**2
        )
        return shift * 365.25 * 86400

    def generate_report(self) -> str:
        """Returns a formatted string summarizing the tidal interaction parameters."""
        report = [
            f"=== Tidal Interaction Report for {self.planet_name} ===",
            "\n--- The change in the orbital period ---",
            f"dP/dE: {self.dp_de:.4e} days/cycle",
            f"dP/dt: {self.dp_dt:.4e}",
            f"Pdot:  {self.p_dot * 1000:.4e} milliseconds per year",
            "\n--- Tidal quality factor ---",
            f"Reduced Q factor (Qs_red): {self.qs_red:.4e}",
            f"Lower limit (Qs_red_lower): {self.qs_red_lower:.4e}",
            "\n--- Timescales ---",
            f"Orbital shrink to zero (t_decay): {self.t_decay:.4e} years",
            f"Characteristic decay (tau_decay): {self.tau_decay:.4e} years",
            f"Circularization time (tau_circ):  {self.tau_circ:.4e} years",
            "\n--- Shifts in T0 ---",
            f"Shift in {self.planet_name} mid-transit (10 yrs): {self.calculate_t0_shift(10):.2f} seconds",
            f"Canonical Q=10^6 shift (10 yrs): {self.calculate_t0_shift(10, q_val=1e6):.2f} seconds",
            "=========================================\n",
        ]
        return "\n".join(report)
