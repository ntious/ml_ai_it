// Validate release provenance before downloading an artifact with Pages rights.
// The caller obtains these objects from GitHub's authenticated REST API.
export function validateRelease(run, artifacts, requestedSHA, repository, defaultBranch) {
  const fail = message => { throw new Error(message); };
  if (!/^[0-9a-f]{40}$/.test(requestedSHA)) fail('Supply the full reviewed commit SHA.');
  if (run.repository?.full_name !== repository) fail('The run belongs to another repository.');
  if (run.status !== 'completed' || run.conclusion !== 'success') fail('The verification run must have completed successfully.');
  if (run.event !== 'push' || run.head_branch !== defaultBranch) fail('Publish only a verified default-branch push, not a pull-request artifact.');
  if (run.head_sha !== requestedSHA) fail('The reviewed commit does not match the artifact run.');
  if (run.path?.split('@')[0] !== '.github/workflows/checks.yml') fail('The artifact must come from the complete learning-resource verification workflow.');
  const matches = artifacts.filter(item => item.name === 'complete-reading-site');
  if (matches.length !== 1 || matches[0].expired || matches[0].size_in_bytes <= 0) fail('One unexpired complete-reading-site artifact is required.');
  return matches[0];
}

export function validateManifest(manifest, requestedSHA, runID, repositoryURL) {
  if (manifest.source_ref !== requestedSHA || String(manifest.workflow_run_id) !== String(runID) ||
      manifest.repository !== repositoryURL || manifest.modules !== 14) {
    throw new Error('The downloaded site manifest does not match the reviewed run and source.');
  }
}
