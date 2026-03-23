"""
Unit tests for core/calculations.py.

All tests use known or analytically verifiable inputs so they do not depend
on external data files, the database, or Streamlit.
"""

import math
import pytest
from core.calculations import (
    f,
    f_left,
    g,
    find_delta_scale,
    find_ci_limits,
    likelihood,
    sigma_tree,
)


# ---------------------------------------------------------------------------
# f_left / f  — boundary conditions
# ---------------------------------------------------------------------------

class TestF:
    def test_below_support_returns_zero(self):
        assert f(-10, scale=1.0, delta=3.0) == 0

    def test_above_support_returns_one(self):
        assert f(10, scale=1.0, delta=3.0) == 1

    def test_at_centre_returns_half(self):
        # At t == t_centre, f should be 0.5 by symmetry
        result = f(0, scale=1.0, delta=3.0, t_centre=0)
        assert abs(result - 0.5) < 1e-10

    def test_monotone_increasing(self):
        scale, delta = 0.5, 5.0
        values = [f(t, scale, delta) for t in range(-6, 7)]
        assert all(a <= b for a, b in zip(values, values[1:]))

    def test_t_centre_shift(self):
        # f(t, ..., t_centre=c) == f(t - c, ..., t_centre=0)
        scale, delta, c = 0.8, 4.0, 2.0
        assert abs(f(3.0, scale, delta, t_centre=c) - f(1.0, scale, delta)) < 1e-12


class TestG:
    def test_g_mirrors_f(self):
        # g(t, ..., t_centre) should equal f(t_centre - t, ...)
        scale, delta, tc = 1.0, 3.0, 5.0
        for t in [-2, 0, 2, 5, 8]:
            assert abs(g(t, scale, delta, tc) - f(tc - t, scale, delta)) < 1e-12


# ---------------------------------------------------------------------------
# find_delta_scale
# ---------------------------------------------------------------------------

class TestFindDeltaScale:
    def test_large_delay_branch(self):
        """When 3*sigma < diagnostic_delay the analytic branch is used."""
        delta, scale, error = find_delta_scale(diagnostic_delay=30.0, sigma=5.0)
        assert error == ""
        assert abs(delta - 15.0) < 1e-10   # delta = 3 * sigma
        assert abs(scale - 1.195554 / 5.0) < 1e-10

    def test_small_delay_branch(self):
        """When 3*sigma >= diagnostic_delay brentq is used."""
        delta, scale, error = find_delta_scale(diagnostic_delay=10.0, sigma=5.0)
        assert error == ""
        assert delta == 10.0
        assert scale is not None and scale > 0

    def test_scale_produces_correct_sigma(self):
        """The found scale should make sigma_tree return ~0."""
        d, sigma = 10.0, 5.0
        delta, scale, error = find_delta_scale(d, sigma)
        assert error == ""
        residual = sigma_tree(scale, sigma, d)
        assert abs(residual) < 1e-8

    def test_typical_antibody_test(self):
        """Realistic inputs for a 3rd-gen antibody test (18-day delay, sigma ~3.6)."""
        delta, scale, error = find_delta_scale(diagnostic_delay=18.1, sigma=3.6)
        assert error == ""
        assert delta > 0
        assert scale > 0

    def test_typical_viral_load_test(self):
        """Realistic inputs when sigma = 0.2 * delay (20% RSE fallback)."""
        delay = 6.0   # log10(30) / 0.35 ≈ 4.2 days, but use a round number
        sigma = 0.2 * delay
        delta, scale, error = find_delta_scale(delay, sigma)
        assert error == ""
        assert delta > 0


# ---------------------------------------------------------------------------
# find_ci_limits — basic properties
# ---------------------------------------------------------------------------

class TestFindCiLimits:
    @pytest.fixture
    def typical_params(self):
        """Parameters for a subject with a 30-day gap between neg and pos tests."""
        d_neg, s_neg = 18.1, 3.62   # 3rd gen antibody test
        d_pos, s_pos = 18.1, 3.62

        delta1, scale1, _ = find_delta_scale(d_neg, s_neg)
        delta2, scale2, _ = find_delta_scale(d_pos, s_pos)

        return dict(
            t1=0, t2=30,
            scale1=scale1, delta1=delta1,
            scale2=scale2, delta2=delta2,
        )

    def test_returns_ordered_bounds(self, typical_params):
        ci_lb, ci_ub, error = find_ci_limits(**typical_params)
        assert error == ""
        assert ci_lb < ci_ub

    def test_bounds_within_support(self, typical_params):
        ci_lb, ci_ub, error = find_ci_limits(**typical_params)
        p = typical_params
        lower_bound = p["t1"] - 3 * p["delta1"]
        upper_bound = p["t2"] + 3 * p["delta2"]
        assert lower_bound <= ci_lb <= upper_bound
        assert lower_bound <= ci_ub <= upper_bound

    def test_95_percent_ci(self, typical_params):
        ci_lb, ci_ub, error = find_ci_limits(**typical_params, alpha=0.05)
        assert error == ""
        # Interval must be positive
        assert ci_ub - ci_lb > 0

    def test_narrower_ci_with_smaller_alpha(self, typical_params):
        """A smaller alpha (wider CI) should produce a wider interval."""
        _, width_95, _ = find_ci_limits(**typical_params, alpha=0.05)
        _, width_80, _ = find_ci_limits(**typical_params, alpha=0.20)
        interval_95 = width_95  # ci_ub for 95%
        interval_80 = width_80  # ci_ub for 80%
        lb_95, ub_95, _ = find_ci_limits(**typical_params, alpha=0.05)
        lb_80, ub_80, _ = find_ci_limits(**typical_params, alpha=0.20)
        assert (ub_95 - lb_95) > (ub_80 - lb_80)

    def test_midpoint_near_middle_of_gap(self, typical_params):
        """For symmetric test properties the CI midpoint should be near t2/2."""
        ci_lb, ci_ub, _ = find_ci_limits(**typical_params)
        midpoint = (ci_lb + ci_ub) / 2
        t2 = typical_params["t2"]
        # Should be in the first half of the gap (negative test side pulls it earlier)
        assert 0 < midpoint < t2
