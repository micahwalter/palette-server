palette-server
==

palette-server is a small little WSGI-compliant httpony to extract colours from an image.

locally with Gunicorn
--

	$> cd palette-server/bin
	$> gunicorn palette-server:app

	$>curl  'http://localhost:8000?path=http://mysite.com/cat.jpg' | python -m json.tool

	{
		"shannon": 3.1487854270660875,
		"reference-closest": "css3",
		"average": {
			"closest": "#808080", 
			"colour": "#8e895a", 
		}, 
		"palette": [
			{
				"closest": "#a0522d", 
				"colour": "#957d34", 
		        }, 
        		{
				"closest": "#556b2f", 
				"colour": "#786438", 
		        }, 
		        {
				"closest": "#bdb76b", 
				"colour": "#b0a370", 
		        }, 
		        {
				"closest": "#556b2f", 
				"colour": "#576710", 
		        }, 
		        {
				"closest": "#808080", 
				"colour": "#827968", 
		        }
		], 
		"stat": "ok"
	}

To do
--

* Unbundle all the private/locally scoped functions inside of the `app` function. It works but it's kind of stupid.
 
* Import the [colour-utils colour.py
  code](https://github.com/straup/colour-utils/blob/master/python/colour.py) and
  allow for custom palettes when calculating the closest colour(s) for a
  palette. Currently the server is hard-coded to "snap to grid" using the CSS3
  palette.

* A proper `setup.py` script for installing dependencies (see below).

* A proper `init.d` script (or equivalent) for starting and stopping the
  palette-server.

* Shouldn't have to load the image twice for palette AND shannon calc

Dependencies
--

* [numpy](http://pypi.python.org/pypi/numpy)

* [webcolors](http://pypi.python.org/pypi/webcolors/)

* [colormath](http://pypi.python.org/pypi/colormath/)

* [RoyGBiv](https://github.com/givp/RoyGBiv)

* [gunicorn](http://www.gunicorn.org/)

See also
--

* [All your color are belong to Giv](http://labs.cooperhewitt.org/2013/giv-do/)	
