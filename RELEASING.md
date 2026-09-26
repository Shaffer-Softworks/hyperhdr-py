# Releasing to PyPI

Steps to publish a new release to PyPI via GitHub Actions:

1. Create a PyPI API token
   - Log in to https://pypi.org, go to "Account settings" → "API tokens", and create a token scoped to the project or to the entire account.

2. Add the token to GitHub
   - In https://github.com/Shaffer-Softworks/hyperhdr-py → Settings → Secrets and variables → Actions → New repository secret.
   - Name the secret `PYPI_API_TOKEN` and paste the token value.

3. Bump the version in `pyproject.toml` (and `hyperhdr/__init__.py` `__version__` if present), commit, and merge to `main`.

4. Create a release tag and push
   - Locally, create an annotated tag:

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

   - Or publish a GitHub Release for that tag (also triggers the workflow).

5. GitHub Actions runs the `Upload Python Package` workflow and uploads the built distributions to PyPI.

Local alternative (using `build` and `twine`):

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine upload dist/* -u __token__ -p $PYPI_API_TOKEN
```
