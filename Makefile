all:
	debuild -us -uc

install:
	dpkg -i ../adapo*.deb
