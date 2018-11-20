from scipy.integrate import quad
from scipy.optimize import brentq
import math


def f_left(t, scale, delta):
    return (1 - (1 - math.exp(scale*t)) / (1 - math.exp(-scale*delta))) / 2

def f(t, scale, delta, t_centre=0):
    t = t = t_centre
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

def signma_tree(scale, sigma, diagnostic_delay):
    delta = min(3*sigma, diagnostic_delay)
    variance = sigma ** 2
    return (2 + (-2 - scale * delta * (2 + scale * delta)) * math.exp(-scale * delta)) / (scale ** 2 * (1 - math.exp(-scale * delta))) - variance

def likelihood(t, t1, t2, scale1, delta1, scale2, delta2):
  return f(t, scale1, delta1, t1) * g(t, scale2, delta2, t2)

def posterior_density_prop(t, t1, t2, scale1, delta1, scale2, delta2):

    const = quad(
        f=likelihood, a=t1-delta1, b=t2+delta2,
        args=(t1, t2, scale1, delta1, scale2, delta2))
    prop = quad(
        f=likelihood, a=t1-delta1, b=t,
        args=(t1, t2, scale1, delta1, scale2, delta2))

    # prop = cubature::adaptIntegrate(f = likelihood,
    #                                lowerLimit = t1-delta1,
    #                                upperLimit = t,
    #                                t1 = t1,
    #                                t2 = t2,
    #                                scale1 = scale1,
    #                                delta1 = delta1,
    #                                scale2 = scale2,
    #                                delta2 = delta2)$integral/const
    return prop/const

def posterior_tree(t, t1, t2, scale1, delta1, scale2, delta2, p=0.025):
    prop = posterior_density_prop(t, t1, t2, scale1, delta1, scale2, delta2)
    return prop - p

def find_ci_limits(t1, t2, scale1, delta1, scale2, delta2, alpha=0.05):

    ci_lb = brentq(f=posterior_tree, a=t1-2*delta1, b=t2+2*delta2, args=(
        t1, t2, scale1, delta1, scale2, delta2, alpha/2
    ))

    # ci.lb <- uniroot(f = posterior_tree, lower = t1- 2 * delta1, upper = t2 + 2 * delta2, t1 = t1, t2 = t2, scale1 = scale1, delta1 = delta1, scale2 = scale2, delta2 = delta2, p = alpha/2)$root

    ci_ub = brentq(f=posterior_tree, a=t1-2*delta1, b=t2+2*delta2, args=(
        t1, t2, scale1, delta1, scale2, delta2, 1-alpha/2
    ))

    # ci.ub <- uniroot(f = posterior_tree, lower = t1- 2 * delta1, upper = t2 + 2 * delta2, t1 = t1, t2 = t2, scale1 = scale1, delta1 = delta1, scale2 = scale2, delta2 = delta2, p = 1 - alpha/2)$root

    return {
        'ci_lb': ci_lb,
        'ci_ub': ci_ub,
    }
