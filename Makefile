#!/usr/bin/make -f

PACKAGE = ie_shell
VERSION = 0.0.3

FULLNAME = $(PACKAGE)-$(VERSION)

default:

dist:
	if test -d $(FULLNAME) ; then rm -rf $(FULLNAME); fi
	mkdir $(FULLNAME)
	cp README COPYING Makefile *.py $(FULLNAME)
	tar cvzf $(FULLNAME).tar.gz $(FULLNAME)
	if test -d $(FULLNAME) ; then rm -rf $(FULLNAME); fi

clean:
	rm -f *.pyc */*.pyc *~ */*~ $(FULLNAME).tar.gz

