#!/usr/bin/env python2

# lserver.py: Web server for log visualization project 
# Arsh Chauhan 
#11/29/2016
# Last Edited: 12/6/2016

import SimpleHTTPServer
import BaseHTTPServer
import json
import threading
import argparse
import socket
import sqlite3
from datetime import datetime
from geoip import geolite2

import log_parser

def create_database(database):
	try:
		db_conn = sqlite3.connect(database)
		db_conn.execute("CREATE TABLE {tn} ({nf} {ft})"\
			.format(tn='attacks',nf='ip_address',ft='TEXT'))
		db_conn.execute("ALTER TABLE attacks ADD COLUMN time_stamp TEXT")
		db_conn.execute("ALTER TABLE attacks ADD COLUMN user TEXT")
		db_conn.execute("ALTER TABLE attacks ADD COLUMN lat TEXT")
		db_conn.execute("ALTER TABLE attacks ADD COLUMN long TEXT")
		db_conn.commit()
	except sqlite3.OperationalError as e:
		print (e)

#FIXME: Clean up timer on KeyboardInterrupt 
#FIXME: DO not insert already existing record in db
def parse_auth_log(log_file,seconds):
		#ip_addresses, invalid_users = log_parser.parse_auth_log("/var/log/auth.log")
		attacks, invalid_users = log_parser.parse_auth_log(log_file)
		db_conn = sqlite3.connect("attacks.sqlite")
		for attack in attacks:
			entry={'ip':attack["ip"],'time_stamp':attack['time_stamp'],'user':attack['user']}
			ip = attack["ip"].strip()
			if ip != '':
				socket.inet_aton(ip)
				geo_data = geolite2.lookup(ip)
				if geo_data is not None:
					entry["lat"] = geo_data.location[0]
					entry["long"] = geo_data.location[1]
					db_conn.execute("INSERT INTO attacks (ip_address,time_stamp,user,lat,long) VALUES (?,?,?,?,?)", \
					(entry["ip"],entry["time_stamp"],entry["user"],str(entry["lat"]),str(entry["long"])))
		db_conn.commit()

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
			db_conn = sqlite3.connect("attacks.sqlite")
			db_conn.row_factory = sqlite3.Row
			db = db_conn.cursor()
			rows = db.execute('''SELECT * FROM attacks GROUP BY ip_address''').fetchall()
			db_conn.commit()
			db_conn.close()
			response = []
			for entry in rows:
					response.append({'ip':entry['ip_address'],'lat':entry['lat'],'long':entry['long']})
			self.send_header('Content-type','application/json')
			self.end_headers()
			self.wfile.write(json.dumps(response))
			self.wfile.close()
		elif self.path == '/topip':
			print ("Work in Progress")
		elif self.path.endswith('scripts.js'):
			with open ('scripts.js') as scripts:
				self.send_response(200)
				self.send_header('Content-type','application/javascript')
				self.end_headers()
				self.wfile.write(scripts.read())
				self.wfile.close()
		elif self.path.endswith('style.css'):
			with open ('style.css') as styles:
				self.send_response(200)
				self.send_header('Content-type','text/css')
				self.end_headers()
				self.wfile.write(styles.read())
				self.wfile.close()

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
	cli_args.add_argument('--port',dest='port',type=int,help='Port to run this server',default=9000)
	cli_args.add_argument('--log',dest='log_file',type=str,help='File to parse as auth.log',default='logs/auth.log')
	args = cli_args.parse_args()

	create_database("attacks.sqlite")
	parse_auth_log(args.log_file,args.timer_sec)
	handler = web_logger_handler
	serverAddress = ('',args.port)
	server = BaseHTTPServer.HTTPServer(serverAddress,handler)
	server.serve_forever()