.PHONY: all build test install clean deb repo
PACKAGE=apt-install
SHELL=bash

all: build

build:
	@echo No build required

release:
	gbp dch --full --release --distribution stable --auto --git-author --commit

test:
	@echo No tests yet, please contribute some.

install:
	mkdir -p $(DESTDIR)/usr/bin $(DESTDIR)/usr/share/man/man1
	install -m 0755 apt-install.py $(DESTDIR)/usr/bin/apt-install
	ronn --pipe <apt-install.1.ronn | gzip -9 > $(DESTDIR)/usr/share/man/man1/apt-install.1.gz

clean:
	rm -Rf debian/$(PACKAGE)* debian/files out/*

deb: clean
	debuild -i -us -uc -b --lintian-opts --profile debian
	mkdir -p out
	mv ../$(PACKAGE)*.{deb,build,changes} out/
	dpkg -I out/*.deb
	dpkg -c out/*.deb

repo:
	../putinrepo.sh out/*.deb

# vim: set ts=4 sw=4 tw=0 noet :
