from scipy.integrate import quad
from scipy.optimize import brentq
import math


def f_left(t, scale, delta):
    return (1 - (1 - math.exp(scale*t)) / (1 - math.exp(-scale*delta))) / 2

def f(t, scale, delta, t_centre=0):
    t = t - t_centre
    if t < -delta:
        return 0
    elif t > delta:
        return 1
    elif t <= 0:
        return f_left(t, scale, delta)
    elif t > 0:
        return 1 - f_left(-t, scale, delta)

def g(t, scale, delta, t_centre):
    t = t_centre-t
    return f(t, scale, delta)

def sigma_tree(scale, sigma, diagnostic_delay):
    delta = min(3*sigma, diagnostic_delay)
    variance = sigma ** 2
    return (2 + (-2 - scale * delta * (2 + scale * delta)) * math.exp(-scale * delta)) / (scale ** 2 * (1 - math.exp(-scale * delta))) - variance

def find_delta_scale(diagnostic_delay, sigma):
    error = ''
    delta = None
    scale = None
    if 3*sigma < diagnostic_delay:
        delta = 3*sigma
        scale = 1.195554/sigma
    else:
        delta = diagnostic_delay
        try:
            scale = brentq(f=sigma_tree, a=1/(10*sigma), b=10*(1/sigma), args=(sigma, diagnostic_delay))
        except Exception:
            error = 'Scale parameters that satisfies specified sigma could not be found\n'
            return delta, scale, error

    return delta, scale, error

def likelihood(t, t1, t2, scale1, delta1, scale2, delta2):
  return f(t, scale1, delta1, t1) * g(t, scale2, delta2, t2)

def posterior_density_prop(t, t1, t2, scale1, delta1, scale2, delta2, const):

    prop = quad(
        func=likelihood, a=t1-delta1, b=t,
        args=(t1, t2, scale1, delta1, scale2, delta2))[0]/const

    if prop < 0:
        prop = 0
    elif prop > 1:
        prop = 1

    return prop

def posterior_tree(t, t1, t2, scale1, delta1, scale2, delta2, const, p=0.025):
    prop = posterior_density_prop(t, t1, t2, scale1, delta1, scale2, delta2, const)
    return prop - p

def find_ci_limits(t1, t2, scale1, delta1, scale2, delta2, alpha=0.05):
    error = ''
    ci_lb = None
    ci_ub = None

    const = quad(
        func=likelihood, a=t1-3*delta1, b=t2+3*delta2,
        args=(t1, t2, scale1, delta1, scale2, delta2))

    if const:
        const = const[0]
    else:
        error = 'Integral of likelihood function could not be obtained\n'
        return ci_lb, ci_ub, error

    ci_lb = brentq(f=posterior_tree, a=t1-3*delta1, b=t2+3*delta2, args=(
        t1, t2, scale1, delta1, scale2, delta2, const, alpha/2
    ))

    ci_ub = brentq(f=posterior_tree, a=t1-3*delta1, b=t2+3*delta2, args=(
        t1, t2, scale1, delta1, scale2, delta2, const, 1-alpha/2
    ))

    return ci_lb, ci_ub, error
