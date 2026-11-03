# Radio-Warder-Evolution repository import plan

Target requested by the owner: `Evolution-by-Warder/Radio-Warder-Evolution`,
public, consistent with the existing FullHDGlass and GSU repositories.

The connected GitHub toolset supports writing repository content but does not
expose repository creation. The web fallback reached GitHub sign-in; the owner
reported that the cloud-browser route does not work and it was stopped. No new
repository has been created or claimed as created.

The current independent source is ready to import from this project's root:
`src`, `tools`, `tests`, `docs`, `update`, `README.md`, `COPYING` and `.gitignore`.
Use `ci/standalone-radio-test.yml` as `.github/workflows/radio-test.yml`; it is
prepared for a root-level standalone main branch. Do not import `dist`, Python
bytecode or test fixture downloads.

Once the empty target repository exists:

1. Initialize it through the GitHub contents API if it has no initial commit.
2. Import the project root and approved PNG assets, with provenance and tests.
3. Change the new updater's repository/feed base and release publication script
   to this repository. Keep the PiconHub catalogue source unchanged.
4. Publish the next test release in the new repository and verify its public
   IPK, hash, identity and update manifests.
5. Publish a migration IPK in the old FullHDGlass-hosted test release location,
   because installed old updaters validate exact repository URLs. Advance the
   old feed only after the bridge IPK is verified. Its installed updater then
   reads the new repository's feed. Do not simply point old manifests at a new
   host; those packages would correctly reject the foreign URL.
6. Update this handoff and README with the final verified source/download links.

Until migration is verified, the existing Warder Radio testing feed remains the
working distribution path. This has no effect on the FullHDGlass skin's stable
feed or the GSU/PiconHub production feeds.
