all: # nothing to build

install:
	# copy python files
	mkdir -p $(DESTDIR)/usr/lib/python2.7/dist-packages/adapo
	cp -r adapo/*.py $(DESTDIR)/usr/lib/python2.7/dist-packages/adapo
	# copy bin
	mkdir -p $(DESTDIR)/usr/bin
	cp -r adapo/core.py $(DESTDIR)/usr/bin/adapo
	# copy example data directory
	mkdir -p $(DESTDIR)/usr/share/adapo
	cp -r data $(DESTDIR)/usr/share/adapo
