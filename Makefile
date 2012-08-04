# Makefile

.PHONY: zip

zip: auto_capitalize.zip

auto_capitalize.zip: manifest.ini __init__.py plugin.py
	rm auto_capitalize.zip > /dev/null || true
	(TEMPDIR=$$(mktemp -d); CURDIR=$$(pwd); \
	 mkdir $$TEMPDIR/auto_capitalize; \
	 cp COPYING.txt manifest.ini __init__.py plugin.py $$TEMPDIR/auto_capitalize; \
	 cd $$TEMPDIR; zip -0r auto_capitalize.zip auto_capitalize; \
	 cd $$CURDIR; mv $$TEMPDIR/auto_capitalize.zip ./; \
	 rm -rf $$TEMPDIR)
