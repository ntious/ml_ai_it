# Advanced investigation: uncertainty, calibration and error costs

Use the [completed project](../../projects/phishing-triage/README.md) to compare
three questions: variability across fitted models, uncertainty in the observed
evaluation records, and the consequences of a decision rule.

## Training variation is not sampling uncertainty

final_seed_stability.csv describes several fits on fixed data. The separate
profile_bootstrap.csv resamples complete exact-profile groups from final records,
with the frozen ensemble and threshold unchanged. Repeated profile rows travel
together. The 2.5th and 97.5th percentiles form an illustrative interval for each
recorded metric under those resampling assumptions.

These are not universal population intervals. Exact profiles do not identify
sites, campaigns or people; selection bias and temporal shift remain. The
bootstrap does not include the entire tuning process or make correlated seed
runs independent. Nested evaluation, new external records or prospective data
may be needed for a stronger claim.

Inspect one error numerator/denominator before interpreting an interval. Explain
which uncertainty this resampling varies and which parts it keeps fixed.

## A probability score is not automatically calibrated

Brier loss scores the squared difference between predicted probabilities and
binary outcomes; lower is better for that scoring rule. final_calibration.csv
groups probabilities into reliability bins with actual counts and observed
positive rates. A high classification score can coexist with overconfident
probabilities. Small bins can be noisy.

The exemplar diagnoses probability behavior; it does **not** fit a post-hoc
calibrator. Fitting sigmoid or isotonic calibration is an advanced extension:
use development-only data or suitable grouped cross-fitting, preserve a final
evaluation boundary and record its additional computational cost. Do not fit
calibration on the final reliability table and report the same table as unbiased
evaluation afterward.

## Error costs are assumptions that need an owner

The default project's false-negative:false-positive ratio is 5:1 in illustrative
units. Validation chooses a threshold by mean cost across the training seeds.
For a final table with FN false negatives and FP false positives, the cost per
1,000 records is `1000 * (5*FN + FP) / n`. Independently reproduce that calculation.

This ratio is not an empirically measured security loss or financial saving.
An operational owner must establish costs, analyst capacity, permitted action
and escalation requirements. A threshold with high recall may overwhelm a
review queue. Source benchmark prevalence need not match deployment prevalence.

For a sensitivity exercise, copy the configuration and compare declared ratios
1:1, 2:1 and 5:1 on **development** evidence in separate runs. Explain threshold
and queue-size tradeoffs. Do not select a ratio from final-test performance.

## Model comparison and practical significance

Models score the same final records, so their errors are paired. Overlap of
separate intervals is not a test of the difference. A planned paired/grouped
bootstrap can estimate metric differences by using the same resampled groups
for both methods. This comparison procedure is an extension, not an implemented
claim in the current project.

Even a statistically distinguishable difference may be operationally unhelpful.
Compare absolute errors, review volume, computation and governance requirements.
A defensible final project can recommend collecting better data or retaining a
simple baseline rather than deploying its most sophisticated model.
