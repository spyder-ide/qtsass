# Release process

## To release a new version of **qtsass** on PyPI:

* Ensure you have the latest version from upstream and update your fork

      git pull upstream master
      git push origin master

* Clean the repo

      git clean -xfdi

* Update CHANGELOG.md

* Update version in `__init__.py` (set release version, remove 'dev0')

* Commit changes

      git add .
      git commit -m "Release X.X.X"

* Create distributions

      python setup.py sdist bdist_wheel

* Upload distributions

      twine upload dist/* -u <username> -p <password>

* Add release tag

      git tag -a vX.X.X -m "Release X.X.X"

* Update `__init__.py` (add 'dev0' and increment minor)

* Commint changes

      git add .
      git commit -m "Back to work"

* Push changes
    
      git push upstream master
      git push origin master
      git push --tags


## To release a new version of **qtsass** on conda-forge:

* Update recipe on the qtsass feedstock: https://github.com/conda-forge/qtsass-feedstock
