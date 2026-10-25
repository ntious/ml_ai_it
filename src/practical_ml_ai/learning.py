"""Small transparent statistical tools for teaching, not automated decisions."""
import math
from statistics import NormalDist
import numpy as np
import pandas as pd


def wilson_interval(successes, observations, confidence=.95):
    """Binomial Wilson interval; requires an appropriate independent sample.

    This arithmetic does not correct clustered sampling, label error or selection
    bias. The fairness exercise uses hand counts to expose sample-size effects.
    """
    if isinstance(successes, bool) or isinstance(observations, bool) or not isinstance(successes, int) or not isinstance(observations, int):
        raise ValueError("Counts must be whole numbers.")
    if not 0 <= successes <= observations or observations <= 0 or not 0 < confidence < 1:
        raise ValueError("Require 0 <= successes <= observations, observations > 0 and 0 < confidence < 1.")
    z = NormalDist().inv_cdf(.5 + confidence/2)
    proportion = successes / observations
    denominator = 1 + z*z/observations
    center = (proportion + z*z/(2*observations))/denominator
    radius = z * math.sqrt(proportion*(1-proportion)/observations + z*z/(4*observations**2))/denominator
    return max(0.,center-radius), min(1.,center+radius)


def calibration_table(actual, probability, bins=5):
    """Development reliability table; empty bins stay absent, not invented zero."""
    y, p = np.asarray(actual), np.asarray(probability,dtype=float)
    if y.ndim != 1 or p.shape != y.shape or not len(y) or not np.isin(y,[0,1]).all():
        raise ValueError("Require equally sized nonempty binary labels and one-dimensional scores.")
    if isinstance(bins,bool) or not isinstance(bins,int) or bins < 1 or not np.isfinite(p).all() or ((p<0)|(p>1)).any():
        raise ValueError("Require finite probabilities in [0,1] and a positive bin count.")
    ids = np.minimum((p*bins).astype(int),bins-1)
    rows = []
    for bin_id in sorted(set(ids)):
        mask = ids == bin_id
        rows.append({"bin":int(bin_id),"lower":bin_id/bins,"upper":(bin_id+1)/bins,
                     "n":int(mask.sum()),"mean_probability":float(p[mask].mean()),"observed_rate":float(y[mask].mean())})
    return pd.DataFrame(rows)
