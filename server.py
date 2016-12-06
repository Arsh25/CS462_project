#!/usr/bin/env python2

# lserver.py: Web server for log visualization project 
# Arsh Chauhan 
#11/29/2016
# Last Edited: 12/5/2016

import SimpleHTTPServer
import BaseHTTPServer
import json
import threading
import argparse
from datetime import datetime


import log_parser

#FIXME: Clean up timer on KeyboardInterrupt 
def parse_auth_log(log_file,seconds):
		#ip_addresses, invalid_users = log_parser.parse_auth_log("/var/log/auth.log")
		ip_addresses, invalid_users = log_parser.parse_auth_log(log_file)
		with open('auth_log_ips','a') as ip_file:
			for ip in ip_addresses:
				ip_file.write(ip+'\n')			
		ip_file.closed
		with open('logs/update.log','a') as parser_log:
			parser_log.write("Ran parse_auth_log at: " + str(datetime.now())+'\n')
		parser_log.closed
		self_timer = threading.Timer(seconds,parse_auth_log,args=[log_file,seconds])
		self_timer.start()
	
class web_logger_handler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path =='/':
			with open ('index.html') as index:
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				self.wfile.write(index.read())
				self.wfile.close()
		elif self.path == '/live':
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			with open('auth_log_ips','r') as ip_file:
				ip_addresses = ip_file.read().splitlines()
				unique_ips = set(ip_addresses) #Convert list to set to get unique IP's
				response = list(unique_ips) # Convert unique IP's set back to list
				self.wfile.write(json.dumps(response))
				self.wfile.close()
			ip_file.closed
		else:
			server_log = open('logs/server.log','a')
			server_log.write("Invalid URL visited: "+self.path+"\n");
			self.send_response(404)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body><h1>404 Page Not Found\
							 <br> \
							 <img src="http://thecatapi.com/api/images/get?format=src&type=gif"\>\
							 <br> </h1><a href="/">Home Page</a> </body></html>')
			self.wfile.close()
			server_log.close()


	def do_POST(self):
		self.send_response(405)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write("This server does not support POST yet")

if __name__ == '__main__':
	cli_args = argparse.ArgumentParser(description='Parse common *nix logs and map on a webpage')
	cli_args.add_argument('--timer',dest='timer_sec',type=int,help='Parse log file every --timer seconds',default=300)
	cli_args.add_argument('--port',dest='port',type=int,help='Port to run this server',default=8080)
	cli_args.add_argument('--log',dest='log_file',type=str,help='File to parse as auth.log',default='logs/auth.log')
	args = cli_args.parse_args()

	parse_auth_log(args.log_file,args.timer_sec)
	handler = web_logger_handler
	serverAddress = ('',args.port)
	server = BaseHTTPServer.HTTPServer(serverAddress,handler)
	server.serve_forever()