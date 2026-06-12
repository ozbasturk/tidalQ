from tidalQ import TidalInteraction

# Example data for a generic hot Jupiter
system_data = {
    "planet_name": "WASP-4b",
    # Based on parameters from Basturk et al. (2025)
    # Table 4 & 5 params
    # a_quad is the quadratic term of the function (1/2 dP / dE)
    "a_quad": (-9.81e-11, 1.21e-11),  # (Value, Error) in days/cycle
    "p_orb": (1.338230994, 0.000000084),  # (Value, Error) in days
    "m_p": (1.200, 0.032),  # (Value, Error) in jupiter mass
    "m_s": (0.899, 0.033),  # (Value, Error) in solar mass
    "a_div_rs": (5.411, 0.053),  # (Value, Error) - unitless
}

# Instantiate the object
system = TidalInteraction(**system_data)

# Print the comprehensive report
print(system.generate_report())

# You can also access individual properties and uncertainties directly
print(f"Direct access to dp/dt: {system.dp_dt:.2e}")
print(f"Direct access to characteristic decay: {system.tau_decay:.2e} years")
