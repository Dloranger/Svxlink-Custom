#!/usr/bin/env python
''' simple python server example; 
    output format supported = html, raw or json '''
import sys
import json
import ConfigParser, os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

svxstatusfile="/usr/share/svxlink/events.d/local/SVXCard/svx_status.conf"   #File of live status of SVXLink Repeater

FORMATS = ('html','json','raw')
format = FORMATS[1]

class Handler(BaseHTTPRequestHandler):

    #handle GET command
    def do_GET(self):

	#print self.path
	if self.path=='/favicon.ico':
        	return
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header('Content-type','text-html')
            self.end_headers()
            self.wfile.write("body")
        elif self.path == '/json':
			config = ConfigParser.ConfigParser()
		#while 1:
		        config.read(svxstatusfile)
		        callsign = config.get('CONFIG', 'REP_CALLSIGN')
		        tx = config.get('STATUS', 'TX')
		        rx = config.get('STATUS', 'RX')
		        tone = config.get('STATUS', 'TONE')
		        longb = config.get('STATUS', 'LONGBEACON')
		        shortb = config.get('STATUS', 'SHORTBEACON')
			cpu_temp= config.get('STATUS', 'CPU_TEMP')
			svx_run= config.get('STATUS', 'SVXLINK_RUN')
			self.send_response(200)
			self.send_header("Access-Control-Allow-Origin", "*");
			self.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin");
			self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
			self.end_headers()
			self.request.sendall(json.dumps({"callsign":callsign,"tx":tx,"rx":rx,"tone":tone,"longb":longb,"shortb":shortb, "cpu_temp":float(cpu_temp),"svx_run":svx_run,}))
			#self.request.sendall(json.dumps({"tx":tx , "callsign":callsign}))
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header('Content-type','text-html')
            self.end_headers()
            self.wfile.write("This server give a dashboard (reach by /) and status in json (reach by /json)")
            self.request.sendall("%s\t%s" %('path', self.path))
        return

def run(port=80):

    print('http server is starting...')
    #ip and port of server
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, Handler)
    print('http server is running...listening on port %s' %port)
    httpd.serve_forever()

if __name__ == '__main__':
#    from optparse import OptionParser
#    op = OptionParser(__doc__)

#    op.add_option("-p", default=80, type="int", dest="port", 
#                  help="port #")
#    op.add_option("-f", default='json', dest="format", 
#                  help="format available %s" %str(FORMATS))
#    op.add_option("--no_filter", default=True, action='store_false', 
#                  dest="filter", help="don't filter")

#    opts, args = op.parse_args(sys.argv)

#    format = opts.format
    run(8080)
