"""
Y-Factor Noise Figure Calculator
Based on R&S Application Note 1MA178 (5th edition)
Includes second-stage (spectrum analyzer) correction via Friis cascade equation.
"""

import math


T0 = 290.0  # Reference temperature in Kelvin (standard)


def dbm_to_watts(dbm: float) -> float:
    return 1e-3 * 10 ** (dbm / 10)


def db_to_linear(db: float) -> float:
    return 10 ** (db / 10)


def linear_to_db(linear: float) -> float:
    return 10 * math.log10(linear)


def calculate_noise_figure(
    ns_off_dbm: float,   # Noise source only, OFF (dBm)
    ns_on_dbm: float,    # Noise source only, ON  (dBm)
    dut_off_dbm: float,  # Noise source + DUT, OFF (dBm)
    dut_on_dbm: float,   # Noise source + DUT, ON  (dBm)
    enr_db: float,       # Noise source ENR (dB)
) -> dict:

    ns_off = dbm_to_watts(ns_off_dbm)
    ns_on  = dbm_to_watts(ns_on_dbm)
    dut_off = dbm_to_watts(dut_off_dbm)
    dut_on  = dbm_to_watts(dut_on_dbm)

    # ENR must be positive (negative ENR is physically invalid)
    if enr_db < 0:
        raise ValueError("ENR cannot be negative. Check the value on your noise source calibration sheet.")

    # Y-factors (linear power ratios)
    Y_src = ns_on / ns_off
    Y_dut = dut_on / dut_off

    if Y_src <= 1:
        raise ValueError("Y_src <= 1: noise source ON power must exceed OFF power (calibration path).")
    if Y_dut <= 1:
        raise ValueError("Y_dut <= 1: noise source ON power must exceed OFF power (DUT path).")

    # Noise source hot temperature from ENR
    ENR = db_to_linear(enr_db)
    T_on  = T0 * (ENR + 1)
    T_off = T0

    # Spectrum analyzer noise temperature (second-stage correction)
    T_sa = (T_on - Y_src * T_off) / (Y_src - 1)
    F_sa = T_sa / T0 + 1

    # Cascaded (SA + DUT) noise factor
    T_cascade = (T_on - Y_dut * T_off) / (Y_dut - 1)
    F_cascade  = T_cascade / T0 + 1

    # DUT gain from cold-state power ratio
    G_dut    = dut_off / ns_off
    G_dut_db = linear_to_db(G_dut)

    # DUT noise factor via Friis equation (second-stage corrected)
    F_dut = F_cascade - (F_sa - 1) / G_dut

    if F_dut < 1:
        raise ValueError(
            "Calculated noise factor is unphysical (F < 1). "
            "Check that DUT+source readings are higher than source-only readings."
        )

    NF_dut = linear_to_db(F_dut)

    return {
        "noise_figure_db": round(NF_dut, 3),
        "gain_db":         round(G_dut_db, 3),
        "y_factor_src_db": round(linear_to_db(Y_src), 3),
        "y_factor_dut_db": round(linear_to_db(Y_dut), 3),
        "nf_sa_db":        round(linear_to_db(F_sa), 3),
    }
