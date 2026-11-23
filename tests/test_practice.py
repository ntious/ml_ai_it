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

    def test_windows_and_path_objects_are_accepted(self):
        from pathlib import PureWindowsPath
        for function in [lambda root, run: str(PureWindowsPath(root)/'runs'/run/'summary.json'),
                         lambda root, run: PureWindowsPath(root)/'runs'/run/'summary.json']:
            self.assertEqual(check('m02_output_path', function)['state'], 'passed')

    def test_swapped_error_counts_are_rejected(self):
        def swapped(actual, predicted):
            return [sum(a and not p for a,p in zip(actual,predicted)), sum(not a and p for a,p in zip(actual,predicted))]
        self.assertEqual(check('m01_error_counts', swapped)['state'], 'needs_revision')

    def test_nan_lag_is_unavailable(self):
        self.assertEqual(check('m05_persistence', lambda values: [float('nan')]+values[:-1])['state'], 'passed')

    def test_visible_feedback_includes_expected_value(self):
        self.assertIn('expected:', check('m01_partition_role', lambda name: 'Fit')['feedback'])

    def test_posix_spellings_pass_and_wrong_or_missing_paths_are_explained(self):
        from pathlib import Path, PurePosixPath
        for function in [lambda root, run: (Path(root)/'runs'/run/'summary.json').as_posix(),
                         lambda root, run: PurePosixPath(root, 'runs', run, 'summary.json')]:
            self.assertEqual(check('m02_output_path', function)['state'], 'passed')
        hardcoded = check('m02_output_path', lambda root, run: 'course/runs/trial-2/summary.json')
        self.assertEqual(hardcoded['state'], 'needs_revision')
        self.assertIn("expected: 'class/runs/baseline/summary.json'", hardcoded['feedback'])
        self.assertEqual(check('m02_output_path', lambda root, run: None)['state'], 'needs_revision')

    def test_feedback_names_the_failing_call(self):
        def partition_role(name):
            return 'Fit'
        self.assertIn("Call: partition_role('train')", check('m01_partition_role', partition_role)['feedback'])

    def test_non_numeric_result_gets_case_feedback_not_a_type_error(self):
        feedback = check('m04_error_rate', lambda errors, requests: f'{errors}/{requests}')['feedback']
        self.assertIn('zero denominator', feedback)
        self.assertNotIn('float()', feedback)

    def test_zero_first_lag_is_not_unavailable(self):
        self.assertEqual(check('m05_persistence', lambda values: [0] + list(values[:-1]))['state'], 'needs_revision')

    def test_generated_pipeline_step_names_are_explained(self):
        from sklearn.impute import SimpleImputer
        from sklearn.linear_model import LinearRegression
        from sklearn.pipeline import make_pipeline
        def unnamed(train_x, train_y, new_x):
            model = make_pipeline(SimpleImputer(strategy='median'), LinearRegression()).fit(train_x, train_y)
            return model, model.predict(new_x)
        result = check('m05_pipeline', unnamed)
        self.assertEqual(result['state'], 'needs_revision')
        self.assertIn('make_pipeline', result['feedback'])

    def test_authoring_record_matches_visible_cases(self):
        import json
        from pathlib import Path
        from practical_ml_ai.practice_cases import CASES
        record = json.loads((Path(__file__).resolve().parents[1] / 'curriculum/exercises.json').read_text(encoding='utf-8'))
        self.assertEqual(set(record), set(CASES))
        for name, case in CASES.items():
            self.assertEqual((record[name]['cases'], record[name]['feedback']), (case['cases'], case['feedback']), name)


if __name__ == '__main__':
    unittest.main()
