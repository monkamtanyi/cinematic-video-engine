import math

def linear(t):
    return t

def ease_in(t):
    return t * t

def ease_out(t):
    return 1 - (1 - t) ** 2

def ease_in_out(t):
    if t < 0.5:
        return 2 * t * t
    return 1 - ((-2 * t + 2) ** 2) / 2

def smoothstep(t):
    return t * t * (3 - 2 * t)

def smootherstep(t):
    return t * t * t * (t * (t * 6 - 15) + 10)