apt-install
===========

Update APT cache and install package(s) with progress GUI.

I hacked it together in order to learn a bit about the aptdaemon, GLib, asynchronous programming etc.

Python code is ugly but works. Needs more error handling. Could probably be written much nicer.

Usage:
```
$ apt-install.py <package-name> [...]
```
