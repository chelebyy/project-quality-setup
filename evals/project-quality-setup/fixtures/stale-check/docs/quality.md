# Quality decisions

This is a synthetic offline backend snapshot with no web UI, production service or deployment.

Selected check: `python -m unittest discover -s tests`; `.github/workflows/quality.yml`, job `unit` (required as `unit`, strict up-to-date branches).
Risk: only the owner can read a record. Positive and denied-access assertions exist in `tests/test_app.py`.
No real CI runs, repository rule enforcement or live entitlements have been verified from this fixture.
