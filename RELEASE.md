# Release process

## Using rever

You need to have `conda` install since the process relies on conda environments.

Make sure your current environment has [rever](https://regro.github.io/rever-docs/) installed.

```bash
conda install rever -c conda-forge
```

Run checks before to make sure things are in order.

```bash
rever check
```

Delete the `rever/` folder to start a clean release.

```bash
rm -rf rever/
```

Run rever with the type version (major|minor|patch|MAJOR.MINOR.PATCH) to update.

### Major release

If the current version is `3.0.0.dev0`, running:

```bash
rever major
```

Will produce version `4.0.0` and update the dev version to `4.0.0.dev0`

### Minor release

If the current version is `3.0.0.dev0`, running:

```bash
rever minor
```

Will produce version `3.1.0` and update the dev version to `3.1.0.dev0`

### Patch release

If the current version is `3.0.0.dev0`, running:

```bash
rever patch
```

Will produce version `3.0.1` and update the dev version to `3.0.1.dev0`

### MAJOR.MINOR.PATCH release

If the current version is `3.0.0.dev0`, running:

```bash
rever 5.0.1
```

Will produce version `5.0.1` and update the dev version to `5.0.1.dev0`

### Important

- In case some of the steps appear as completed, delete the `rever` folder.

```bash
rm -rf rever/
```

- Some of the intermediate steps may ask for feedback, like checking the changelog.

## Manual process

- Ensure you have the latest version from upstream and update your fork

```bash
git pull upstream master
git push origin master
```

- Clean the repo

```bash
git clean -xfdi
```

- Update CHANGELOG.md using loghub

```bash
loghub spyder-ide/qtsass -zr <release>
```

- Update version in `__init__.py` (set release version, remove 'dev0')

- Commit changes

```bash
git add .
git commit -m "Release X.X.X"
```

- Create distributions

```bash
python setup.py sdist bdist_wheel
```

- Upload distributions

```bash
twine upload dist/* -u <username> -p <password>
```

- Add release tag

```bash
git tag -a vX.X.X -m "Release X.X.X"
```

- Update `__init__.py` (add 'dev0' and increment minor)

- Commint changes

```bash
git add .
git commit -m "Back to work"
```

- Push changes

```bash
git push upstream master
git push origin master
git push --tags
```

## To release a new version of **qtsass** on conda-forge

- Update recipe on the [qtsass feedstock](https://github.com/conda-forge/qtsass-feedstock)
