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

## Semi-automatic process using Git and GitHub actions

- Ensure you have the latest version from upstream and update your fork

```bash
git pull upstream master
git push origin master
```

- Clean the repo (select option 1)

```bash
git clean -xfdi
```

- Update `CHANGELOG.md` using loghub

```bash
loghub spyder-ide/qtsass -m <vX.X.X>
```

- Update version in `__init__.py` (set release version, remove 'dev0')

- Commit and push changes

```bash
git add .
git commit -m "Release X.X.X"
git push upstream master
git push origin master
```

- Make a [new release](https://github.com/spyder-ide/qtsass/releases) with tag name `vX.X.X`

- Check that [the CI workflow](https://github.com/spyder-ide/qtsass/actions) for `vX.X.X` 
  successfully deployed the new release

- Update `__init__.py` (add 'dev0' and increment minor)

- Commit and push changes

```bash
git add .
git commit -m "Back to work"
git push upstream master
git push origin master
```

## To release a new version of **qtsass** on conda-forge

- Update recipe on the [qtsass feedstock](https://github.com/conda-forge/qtsass-feedstock)
