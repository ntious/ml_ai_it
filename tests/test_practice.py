"""Regression checks for formative feedback, including plausible learner errors."""
import unittest

from practical_ml_ai.practice import check


class FormativeFeedbackTests(unittest.TestCase):
    def test_unfinished_is_not_a_pass(self):
        def unfinished(*args):
            raise NotImplementedError()
        self.assertEqual(check('m05_residuals', unfinished)['state'], 'not_attempted')

    def test_signed_average_is_not_mae(self):
        def wrong(actual, predicted):
            residuals = [a - p for a, p in zip(actual, predicted)]
            mean = sum(residuals) / len(residuals)
            return {'residuals': residuals, 'mae': abs(mean), 'mean_residual': mean}
        result = check('m05_residuals', wrong)
        self.assertEqual(result['state'], 'needs_revision')
        self.assertIn('cancel', result['feedback'])

    def test_target_day_is_not_a_lag(self):
        self.assertEqual(check('m05_persistence', lambda counts: [None] + list(counts[1:]))['state'], 'needs_revision')

    def test_equal_threshold_is_positive(self):
        def wrong(actual, probabilities, threshold):
            pairs = list(zip(actual, [p > threshold for p in probabilities]))
            return {key: sum(a == target and p == predicted for a, p in pairs)
                    for key, target, predicted in [('tp', 1, True), ('fp', 0, True), ('fn', 1, False), ('tn', 0, False)]}
        self.assertEqual(check('m06_confusion', wrong)['state'], 'needs_revision')

    def test_ignoring_error_costs_is_caught(self):
        self.assertEqual(check('m06_threshold', lambda *args: .5)['state'], 'needs_revision')

    def test_training_loss_does_not_choose_checkpoint(self):
        self.assertEqual(check('m08_checkpoint', lambda train, validation: min(range(len(train)), key=train.__getitem__) + 1)['state'], 'needs_revision')

    def test_imputer_fitted_on_later_rows_is_rejected(self):
        import numpy as np
        from sklearn.pipeline import Pipeline
        from sklearn.impute import SimpleImputer
        from sklearn.linear_model import LinearRegression
        def leaked(train_x, train_y, new_x):
            imputer = SimpleImputer(strategy='median').fit(np.vstack([train_x, new_x]))
            model = LinearRegression().fit(imputer.transform(train_x), train_y)
            pipeline = Pipeline([('imputer', imputer), ('model', model)])
            return pipeline, pipeline.predict(new_x)
        self.assertEqual(check('m05_pipeline', leaked)['state'], 'needs_revision')

    def test_unknown_check_is_actionable(self):
        with self.assertRaisesRegex(ValueError, 'Unknown practice check'):
            check('m99_missing', lambda: None)

    def test_matching_mean_does_not_satisfy_median_contract(self):
        from sklearn.pipeline import Pipeline
        from sklearn.impute import SimpleImputer
        from sklearn.linear_model import LinearRegression
        def wrong(train_x, train_y, new_x):
            model = Pipeline([('imputer', SimpleImputer()), ('model', LinearRegression())]).fit(train_x, train_y)
            return model, model.predict(new_x)
        result = check('m05_pipeline', wrong)
        self.assertEqual(result['state'], 'needs_revision')
        self.assertIn('median imputation', result['feedback'])

    def test_hard_labels_are_not_probability_scores(self):
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import LogisticRegression
        def wrong(train_x, train_y, new_x):
            model = Pipeline([('scaler', StandardScaler()), ('model', LogisticRegression())]).fit(train_x, train_y)
            return model, model.predict(new_x)
        result = check('m06_pipeline', wrong)
        self.assertEqual(result['state'], 'needs_revision')
        self.assertIn('predict_proba', result['feedback'])

    def test_list_based_checkpoint_implementation_is_valid(self):
        def valid(train, validation):
            return validation.index(min(validation)) + 1
        self.assertEqual(check('m08_checkpoint', valid)['state'], 'passed')


if __name__ == '__main__':
    unittest.main()
