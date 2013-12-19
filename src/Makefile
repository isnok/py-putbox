# A collection of useful oneliners

clean:
	find . -type f \( -name "*.pyc" -or -name "dropin.cache" \) -exec rm {} \;

serve: clean
	ps fax | grep -v grep | grep -q 'putbox\.py' || { ./putbox.py & }

debian-deps:
	apt-get install python-twisted python-stdlib sqlite3
