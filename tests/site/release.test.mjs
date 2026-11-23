// These checks exercise release boundaries; they do not deploy a site.
import test from 'node:test';
import assert from 'node:assert/strict';
import { validateRelease, validateManifest } from '../../scripts/pages_release.mjs';
const sha = 'a'.repeat(40);
const run = { repository: { full_name: 'ntious/ml_ai_it' }, status: 'completed', conclusion: 'success', event: 'push', head_branch: 'main', head_sha: sha, path: '.github/workflows/checks.yml' };
const artifacts = [{ id: 12, name: 'complete-reading-site', expired: false, size_in_bytes: 1000 }];
const validate = (value = run, files = artifacts, reviewed = sha) => validateRelease(value, files, reviewed, 'ntious/ml_ai_it', 'main');

test('a successful reviewed default-branch verification selects the actual artifact', () => assert.equal(validate().id, 12));
test('pull-request artifacts cannot become releases', () => assert.throws(() => validate({ ...run, event: 'pull_request' }), /default-branch push/));
test('a failed run is rejected', () => assert.throws(() => validate({ ...run, conclusion: 'failure' }), /successfully/));
test('a different source SHA is rejected', () => assert.throws(() => validate(run, artifacts, 'b'.repeat(40)), /does not match/));
test('a different repository is rejected', () => assert.throws(() => validate({ ...run, repository: { full_name: 'someone/else' } }), /another repository/));
test('a different workflow is rejected', () => assert.throws(() => validate({ ...run, path: '.github/workflows/other.yml' }), /complete learning/));
test('expired and ambiguous artifacts are rejected', () => {
  assert.throws(() => validate(run, [{ ...artifacts[0], expired: true }]), /unexpired/);
  assert.throws(() => validate(run, [...artifacts, { ...artifacts[0], id: 13 }]), /unexpired/);
});
test('artifact contents must match both the run and source revision', () => {
  const manifest = { source_ref: sha, workflow_run_id: '123', repository: 'https://github.com/ntious/ml_ai_it', modules: 14 };
  assert.doesNotThrow(() => validateManifest(manifest, sha, 123, manifest.repository));
  assert.throws(() => validateManifest({ ...manifest, source_ref: 'b'.repeat(40) }, sha, 123, manifest.repository), /does not match/);
  assert.throws(() => validateManifest(manifest, sha, 456, manifest.repository), /does not match/);
});
