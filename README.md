# minall

CLI tool and Python library to apply a suite of Minet's data-mining tools on a heterogenous set of URLs.

![Tests](https://github.com/medialab/minall/actions/workflows/tests.yml/badge.svg)

---

See full documentation here: [https://medialab.github.io/minall/](https://medialab.github.io/minall/)

---

New Releases:

1. Run tests locally.
2. Increment the version number in `minall/__version__.py`
3. `git add minall/__version__.py` Add the updated version file.
4. `git commit -m "Bump version x.y.z"` Commit the updated version file with a message.
5. `git push origin main` Push the updated version file to the remote repository, which is still governed by the old/current release.
6. `git tag vx.y.z -m "Release vx.y.z"` Create a tag for the new version.
7. `git push origin vx.y.z` Push the tag to the remote repository.
8. On the remote repository, publish a new release of the current version of the directory with the pushed tag `x.y.z`.
