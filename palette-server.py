import urllib, cStringIO
from bin import roygbiv
import webcolors
from bin import shannon
import json
import cgi
import Image
import logging
from cStringIO import StringIO
logging.basicConfig(level=logging.DEBUG)

html = """
<html>
<body>
	<form id="mainform" enctype="multipart/form-data" action="/" method="post" >
	<label for="imageupload">Image file:</label>
	<input name="imageupload" id="imageupload" type="file" /><br />
	<input name="submit" id="submit" type="submit" value="submit"> 
	</form>
</body>
</html>
"""

def app(environ, start_response):

    # https://bitbucket.org/ubernostrum/webcolors/src/b93975d4507fbf0a500656cb475dbd8ddae7a549/webcolors.py?at=default#cl-191

    def closest_colour(requested_colour):
        min_colours = {}

        for key, name in webcolors.css3_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]

    def get_closest(hex):

        rgb = webcolors.hex_to_rgb(hex)

        try:
            closest_name = actual_name = webcolors.rgb_to_name(rgb)
        except ValueError:
            closest_name = closest_colour(rgb)
            actual_name = None

        if actual_name:
            actual = webcolors.name_to_hex(actual_name)
        else:
            actual = None

        closest = webcolors.name_to_hex(closest_name)

        return actual, closest

    def prep(hex):

        web_actual, web_closest = get_closest(hex)

        return {
            'colour': hex,
            'closest': web_closest,
            }

    def get_palette(URL):

        roy = roygbiv.Roygbiv(URL)
        average = roy.get_average_hex()
        palette = roy.get_palette_hex()

        average = prep(average)
        palette = map(prep, palette)

        return { 'reference-closest': 'css3', 'average': average, 'palette': palette }

    def get_shannon(img):

	    shan = shannon.image_entropy(img)
	
	    return shan
	
    def open_image(URL):
	
	    filename = cStringIO.StringIO(urllib.urlopen(URL).read())
	    img = Image.open(filename)
	
	    return img
	
    def open_data(data):
	
	    img = Image.open(data)
	
	    return img
	

    status = '200 OK'
    body = ''
    rsp = {}
    try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
		request_body_size = 0
		
    if request_body_size!=0:
        form = cgi.FieldStorage(fp=environ['wsgi.input'], 
		                        environ=environ)
        fileitem = form['imageupload']
        
        try:
            im = open_data(fileitem.file)
            rsp = get_palette(im)
            rsp['stat']  = 'ok'
            rsp['shannon'] = get_shannon(im)
        except Exception, e:
            logging.error(e)
            rsp = {'stat': 'error', 'error': "failed to process image: %s" % e}
	
        if rsp['stat'] != 'ok':
            status = "500 SERVER ERROR"

        rsp = json.dumps(rsp)

        #logging.debug("%s : %s" % (path, status))

        start_response(status, [
                    ("Content-Type", "text/javascript"),
                    ("Content-Length", str(len(rsp)))
                    ])

        return iter([rsp])
        

    else:
        params = cgi.parse_qs(environ.get('QUERY_STRING', ''))
        path = params.get('path', None)
		
        if not path:
            start_response(status, [
                    ("Content-Type", "text/html"),
                    ("Content-Length", str(len(html)))
                    ])
	        
            return iter([html])
        else:
            path = path[0]
            try:
                data = open_image(path)
                rsp = get_palette(data)
                rsp['stat']  = 'ok'
                rsp['shannon'] = get_shannon(data)
            except Exception, e:
                logging.error(e)
                rsp = {'stat': 'error', 'error': "failed to process image: %s" % e}
			        
        if rsp['stat'] != 'ok':
            status = "500 SERVER ERROR"

        rsp = json.dumps(rsp)

        logging.debug("%s : %s" % (path, status))

        start_response(status, [
                ("Content-Type", "text/javascript"),
                ("Content-Length", str(len(rsp)))
                ])

        return iter([rsp])
			


