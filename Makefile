all:
	debuild -us -uc
	debclean

install:
	dpkg -i ../adapo*.deb
