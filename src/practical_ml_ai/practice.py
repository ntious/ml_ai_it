"""Visible formative checks for learner-written functions, not a grading service.

Only explicitly selected trusted course notebooks call these checks. Each case
uses small authored examples; passing does not establish independent mastery.
"""
import numpy as np


def _close(actual, expected, message):
    assert np.shape(actual) == np.shape(expected), message + " Check the output shape."
    assert np.allclose(actual, expected, rtol=1e-6, atol=1e-7), message


def _residuals(function):
    for actual, predicted, residuals, mae, mean in [
        ([110, 125], [100, 140], [10, -15], 12.5, -2.5),
        ([1, 4, 10], [3, 4, 4], [-2, 0, 6], 8 / 3, 4 / 3),
    ]:
        result = function(actual, predicted)
        _close(result['residuals'], residuals, 'Residual means actual minus predicted.')
        _close(result['mae'], mae, 'Take absolute errors before averaging; signed errors cancel.')
        _close(result['mean_residual'], mean, 'Mean residual retains the signs and original units.')


def _persistence(function):
    for counts, expected in [([10, 13, 9], [None, 10, 13]), ([4, 0, 7, 2], [None, 4, 0, 7])]:
        result = list(function(counts))
        assert len(result) == len(counts) and result[0] is None, 'Keep one row per day; the first lag is unavailable, not zero.'
        _close(result[1:], expected[1:], 'Use the preceding count, never the target-day or following count.')


def _regression(function):
    from sklearn.pipeline import Pipeline
    train = np.array([[1.], [3.], [np.nan], [5.]])
    model, predicted = function(train.copy(), np.array([2., 6., 6., 10.]), np.array([[np.nan], [100.]]))
    assert isinstance(model, Pipeline), 'Return a fitted sklearn Pipeline and its predictions.'
    assert model.named_steps['imputer'].strategy == 'median', 'Use median imputation explicitly; a matching training mean in this fixture is not the requested strategy.'
    _close(model.named_steps['imputer'].statistics_, [3.], 'Fit the imputer on training only; new inputs must not change its median.')
    _close(predicted, [6., 200.], 'Apply the fitted transformation/model to new inputs, without refitting.')


def _confusion(function):
    cases = [([0, 1, 0, 1], [.2, .4, .5, .8], .5, {'tp': 1, 'fp': 1, 'fn': 1, 'tn': 1}),
             ([0, 0, 1], [.1, .8, .6], .5, {'tp': 1, 'fp': 1, 'fn': 0, 'tn': 1}),
             ([1, 1], [.2, .5], .5, {'tp': 1, 'fp': 0, 'fn': 1, 'tn': 0})]
    for actual, probability, threshold, expected in cases:
        assert function(actual, probability, threshold) == expected, 'Use score >= threshold; positive means actual label 1. Count each row once.'


def _threshold(function):
    actual, probability, thresholds = [0, 1, 0, 1], [.2, .4, .5, .8], [.3, .5, .7]
    _close(function(actual, probability, thresholds, 3, 1), .3, 'Minimize miss_cost*FN + false_alarm_cost*FP on validation.')
    _close(function(actual, probability, thresholds, 1, 5), .7, 'Recompute the decision when the declared costs change.')
    _close(function([0, 1], [.1, .9], [.7, .3], 1, 1), .3, 'For equal costs choose the smallest threshold, independent of candidate order.')


def _classifier(function):
    from sklearn.pipeline import Pipeline
    train = np.array([[0.], [2.], [4.], [6.]])
    model, probability = function(train.copy(), np.array([0, 0, 1, 1]), np.array([[-2.], [100.]]))
    assert isinstance(model, Pipeline), 'Return the fitted scaler/classifier Pipeline and positive-class probabilities.'
    _close(model.named_steps['scaler'].mean_, [3.], 'The scaler must learn its mean from training only.')
    assert np.shape(probability) == (2,), 'Return one positive-class probability per new row, not both class columns.'
    expected = model.predict_proba(np.array([[-2.], [100.]]))[:, list(model.classes_).index(1)]
    _close(probability, expected, 'Return class-1 predict_proba values, not hard labels from predict; thresholds need the scores.')
    assert 0 <= probability[0] < .5 < probability[1] <= 1, 'Find the probability column corresponding to class 1.'


def _dense(function):
    _close(function(np.array([[1., 2.], [0., 1.]]), np.array([[.5, 1.], [-1., 0.]]), np.array([.5, -2.])),
           [[0., 0.], [0., 0.]], 'Multiply a batch by weights, add one bias per hidden unit, then apply ReLU.')
    _close(function(np.array([[2., 1.]]), np.array([[1., -1.], [0., 1.]]), np.array([0., 2.])),
           [[2., 1.]], 'ReLU keeps positive values; it is not a sigmoid or a sum over the batch.')


def _checkpoint(function):
    assert function([.65, .5, .38, .3], [.69, .51, .48, .55]) == 3, 'Return a one-based epoch chosen by minimum validation loss, not training loss.'
    assert function([.8, .7, .6], [.4, .3, .3]) == 2, 'For equal minimum validation loss retain the earliest epoch.'


def _network(function):
    for inputs, width in [(11, 16), (3, 4)]:
        model = function(inputs, width)
        assert model.input_shape == (None, inputs) and model.output_shape == (None, 1), 'Keep the batch dimension flexible and return one probability per row.'
        assert model.count_params() == inputs * width + width + width + 1, 'Count input-hidden weights, hidden biases, output weights and output bias.'
        assert model.layers[0].activation.__name__ == 'relu' and model.layers[-1].activation.__name__ == 'sigmoid', 'Use a ReLU hidden layer and sigmoid output for this binary contract.'
        probability = np.asarray(model(np.zeros((2, inputs)), training=False))
        assert probability.shape == (2, 1) and np.all((probability >= 0) & (probability <= 1)), 'Inference returns one bounded probability for each row.'


CHECKS = {'m05_residuals': _residuals, 'm05_persistence': _persistence, 'm05_pipeline': _regression,
          'm06_confusion': _confusion, 'm06_threshold': _threshold, 'm06_pipeline': _classifier,
          'm08_dense': _dense, 'm08_checkpoint': _checkpoint, 'm08_network': _network}


def _fixture_check(specification):
    from copy import deepcopy
    import math

    def equivalent(actual, expected):
        if expected is None or isinstance(expected, (str, bool)):
            return type(actual) is type(expected) and actual == expected
        if isinstance(expected, dict):
            return isinstance(actual, dict) and actual.keys() == expected.keys() and all(equivalent(actual[k], v) for k, v in expected.items())
        if isinstance(expected, list):
            return isinstance(actual, (list, tuple)) and len(actual) == len(expected) and all(equivalent(a, b) for a, b in zip(actual, expected))
        return not isinstance(actual, bool) and math.isclose(float(actual), expected, rel_tol=1e-6, abs_tol=1e-7)

    def verify(function):
        for arguments, expected in specification['cases']:
            actual = function(*deepcopy(arguments))
            assert equivalent(actual, expected), specification['feedback'] + f" Input: {arguments!r}; observed: {actual!r}."
    return verify


from .practice_cases import CASES
CHECKS.update({name: _fixture_check(specification) for name, specification in CASES.items()})


def check(name, function):
    """Return readable formative feedback; unfinished work stays visibly unfinished."""
    if name not in CHECKS:
        raise ValueError(f'Unknown practice check: {name}')
    try:
        CHECKS[name](function)
    except NotImplementedError:
        result = {'check': name, 'state': 'not_attempted', 'feedback': 'Replace the function body, rerun it, then rerun this check. Try the first hint on the practice page.'}
    except Exception as error:
        result = {'check': name, 'state': 'needs_revision', 'feedback': str(error) or type(error).__name__}
    else:
        result = {'check': name, 'state': 'passed', 'feedback': 'These visible cases pass. Explain why, try changed inputs, and complete the transfer task.'}
    print(f"{result['check']}: {result['state']} — {result['feedback']}")
    return result
