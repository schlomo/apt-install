DPKG=dpkg
DPKG_OPTS=-b
.PHONY: info repo deb

info: deb
	dpkg-deb -I out/*_all.deb
	dpkg-deb -c out/*_all.deb

deb:	clean
	rm -Rf build
	mkdir -p out build/usr/bin
	install -m 0755 apt-install.py build/usr/bin/apt-install
	cp -r DEBIAN build
	mkdir -p build/usr/share/doc/apt-install build/usr/share/man/man1
	ronn --pipe --date=$(shell date +%F) --roff apt-install.1.ronn | gzip -9 >build/usr/share/man/man1/apt-install.1.gz
	mv build/DEBIAN/copyright build/usr/share/doc/apt-install/copyright
	git log | gzip -9 >build/usr/share/doc/apt-install/changelog.gz
	chmod -R g-w build
	fakeroot ${DPKG} ${DPKG_OPTS} build out
	rm -Rf build
	lintian -i out/*_all.deb
	git add -A

repo: deb
	../putinrepo.sh out/*_all.deb

clean:
	rm -fr out build


