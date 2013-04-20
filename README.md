# Mako2Jinja

Converts a given mako template into a jinja template, badly.
It's just intended to help with the mechanical editing - you'll probably have to fixup anything complicated yourself.

	Usage:
	    mako2jinja.py FILE
	    mako2jinja.py (-h | --help)
	    mako2jinja.py --version

	Arguments:
	    FILE                      Input file.

	Options:
	    -h --help                 Show this screen.
	    --version                 Show version.

Currently knows how to handle and convert:

* blocks
* def -> macro's
* if, else, endif
* for, endfor
* namespace -> import
* inherit -> extends
* filters:
	* len(thing* ) -> thing|length
	* |h -> |e
* variable output
* single line comments

