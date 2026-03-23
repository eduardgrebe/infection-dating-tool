# Copyright (C) Stellenbosch University
# Copyright (C) 2026 Eduard Grebe Consulting (Pty) Ltd
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is derived from the original Infection Dating Tool
# (https://github.com/eduardgrebe/infection-dating-tool).

"""
Bayesian posterior probability density functions for HIV infection date estimation.

Ported from the original Django/Python 2 app with no logic changes.
All functions are pure Python/scipy with no framework dependencies.
"""

import math

from scipy.integrate import quad
from scipy.optimize import brentq


def f_left(t, scale, delta):
    return (1 - (1 - math.exp(scale * t)) / (1 - math.exp(-scale * delta))) / 2


def f(t, scale, delta, t_centre=0):
    """Cumulative probability function for infection timing relative to a test date."""
    t = t - t_centre
    if t < -delta:
        return 0
    elif t > delta:
        return 1
    elif t <= 0:
        return f_left(t, scale, delta)
    else:
        return 1 - f_left(-t, scale, delta)


def g(t, scale, delta, t_centre):
    """Reflection of f around t_centre; used for the positive test side of the likelihood."""
    t = t_centre - t
    return f(t, scale, delta)


def sigma_tree(scale, sigma, diagnostic_delay):
    """
    Variance difference for a given scale parameter.
    Used by brentq to find the scale where variance matches the specified sigma.
    """
    delta = min(3 * sigma, diagnostic_delay)
    variance = sigma ** 2
    return (
        (2 + (-2 - scale * delta * (2 + scale * delta)) * math.exp(-scale * delta))
        / (scale ** 2 * (1 - math.exp(-scale * delta)))
        - variance
    )


def find_delta_scale(diagnostic_delay, sigma):
    """
    Determine the delta (window half-width) and scale (exponential decay rate)
    parameters for the infection timing distribution.

    Returns
    -------
    (delta, scale, error) where error is an empty string on success.
    """
    error = ""
    delta = None
    scale = None

    if 3 * sigma < diagnostic_delay:
        delta = 3 * sigma
        scale = 1.195554 / sigma
    else:
        delta = diagnostic_delay
        try:
            scale = brentq(
                f=sigma_tree,
                a=1 / (10 * sigma),
                b=10 * (1 / sigma),
                args=(sigma, diagnostic_delay),
            )
        except Exception:
            error = (
                "Under the test sensitivity model in use, the sigma specified "
                "could not be attained. "
            )
            return delta, scale, error

    return delta, scale, error


def likelihood(t, t1, t2, scale1, delta1, scale2, delta2):
    """Joint likelihood of infection at time t given a negative test at t1 and positive at t2."""
    return f(t, scale1, delta1, t1) * g(t, scale2, delta2, t2)


def posterior_density_prop(t, t1, t2, scale1, delta1, scale2, delta2, const):
    """Proportion of the posterior density up to time t."""
    prop = quad(
        func=likelihood,
        a=t1 - delta1,
        b=t,
        args=(t1, t2, scale1, delta1, scale2, delta2),
    )[0] / const

    return max(0.0, min(1.0, prop))


def posterior_tree(t, t1, t2, scale1, delta1, scale2, delta2, const, p=0.025):
    """Root function for brentq: finds t where cumulative posterior equals p."""
    prop = posterior_density_prop(t, t1, t2, scale1, delta1, scale2, delta2, const)
    return prop - p


def find_ci_limits(t1, t2, scale1, delta1, scale2, delta2, alpha=0.05):
    """
    Find the lower and upper bounds of the (1 - alpha) credibility interval
    for the infection date, expressed as days relative to t1.

    Parameters
    ----------
    t1 : float
        Time of the (adjusted) latest negative test, typically 0.
    t2 : float
        Time of the (adjusted) earliest positive test, in days after t1.
    scale1, delta1 : float
        Shape parameters for the negative-test distribution.
    scale2, delta2 : float
        Shape parameters for the positive-test distribution.
    alpha : float
        Significance level; produces a (1 - alpha) credibility interval.

    Returns
    -------
    (ci_lb, ci_ub, error) where error is an empty string on success.
    """
    error = ""
    ci_lb = None
    ci_ub = None

    const_result = quad(
        func=likelihood,
        a=t1 - 3 * delta1,
        b=t2 + 3 * delta2,
        args=(t1, t2, scale1, delta1, scale2, delta2),
    )

    if not const_result:
        error = "Integral of likelihood function could not be obtained. "
        return ci_lb, ci_ub, error

    const = const_result[0]

    ci_lb = brentq(
        f=posterior_tree,
        a=t1 - 3 * delta1,
        b=t2 + 3 * delta2,
        args=(t1, t2, scale1, delta1, scale2, delta2, const, alpha / 2),
    )

    ci_ub = brentq(
        f=posterior_tree,
        a=t1 - 3 * delta1,
        b=t2 + 3 * delta2,
        args=(t1, t2, scale1, delta1, scale2, delta2, const, 1 - alpha / 2),
    )

    return ci_lb, ci_ub, error
