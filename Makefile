.PHONY: all build test install clean deb repo
PACKAGE=apt-install
SHELL=bash
VERSION=$(shell git rev-list HEAD --count --no-merges)

all: build

build:
	@echo No build required

commit-release:
	gbp dch --full --release --new-version=$(VERSION) --distribution stable --auto --git-author --commit

release: commit-release deb
	@latest_tag=$$(git describe --tags `git rev-list --tags --max-count=1`); \
	comparison="$$latest_tag..HEAD"; \
	if [ -z "$$latest_tag" ]; then comparison=""; fi; \
	changelog=$$(git log $$comparison --oneline --no-merges --reverse); \
	github-release schlomo/$(PACKAGE) v$(VERSION) "$$(git rev-parse --abbrev-ref HEAD)" "**Changelog**<br/>$$changelog" 'out/*.debx'; \
	git pull

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
