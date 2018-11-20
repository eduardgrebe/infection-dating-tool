import math

def f_left(t, alpha, delta):
    return (1 - (1 - math.exp(alpha*t)) / (1 - math.exp(-alpha*delta))) / 2

def f(t, alpha, delta):
    if t < -delta:
        return 0
    elif t > delta:
        return 1
    elif t <= 0:
        return f_left(t, alpha, delta)
    elif t > 0:
        return 1 - f_left(-t, alpha, delta)

def signma_tree(alpha, sigma, diagnostic_delay):
    delta = min(3*sigma, diagnostic_delay)
    variance = sigma ** 2
    return (2 + (-2 - alpha * delta * (2 + alpha * delta)) * math.exp(-alpha * delta)) / (alpha ** 2 * (1 - math.exp(-alpha * delta))) - variance
