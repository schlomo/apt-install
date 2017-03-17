apt-install
===========

Update APT cache and install package(s) with progress GUI.

I hacked it together in order to learn a bit about the aptdaemon, GLib, asynchronous programming etc.

Python code is ugly but works. Needs more error handling. Could probably be written much nicer.

Usage:
```
$ apt-install.py <package-name> [...]
```

Building & Installation
-----------------------

Simply run `make` to create a DEB package in `out/`.
Build Requirements are debuild(1), git-dch(1) and [ronn](http://rtomayko.github.io/ronn/). For Ubuntu/Debian install the `devscripts git-buildpackage ruby-ronn make debhelper` packages.

To create a release [github-release](https://github.com/c4milo/github-release) needs to be in your PATH.
