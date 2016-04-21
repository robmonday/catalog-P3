# Server configuration
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# SQLalchemy code configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from database_setup import Base, Restaurant, MenuItem # importing table schema and declarative base
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Hello!</h1>"
				output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
				<h2>What would you like me to say?</h2><input name='message' type='text'>
				<input type='submit' value='Submit'></form>"""	
				output += "</body></html>"	
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1> &#161Hola! </h1><a href='/hello'>Back to Hello</a>"				
				output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
				<h2>What would you like me to say?</h2><input name='message' type='text'>
				<input type='submit' value='Submit'></form>"""	
				output += "</body></html>"	
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/restaurant"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>List of Restaurants:</h1>"

				restaurants = session.query(Restaurant).all()	# SQLalchemy request for restaurant list
				for restaurant in restaurants:					# Add to output
					output += '<li>'+restaurant.name+'</li>'
					
				output += "</body></html>"	
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/menuitem"):  # Rob added this as extra credit
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>List of Menu Items:</h1>"
				output += "<table style='width:80%'><tr><th>Name</th><th>Price</th><th>Course</th><th>Description</th></tr>"

				items = session.query(MenuItem).all()	# SQLalchemy request for restaurant list
				for item in items:				
					output += '<tr><td>'+item.name+'</td><td> '+item.price+'</td><td> '+item.course+'</td><td> '+item.description+'</td></tr>'
				output += "</table>"
				output += "</body></html>"	
				self.wfile.write(output)
				print output
				return	

		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			self.send_response(301)
			self.end_headers()
			ctype, pdict = cgi.parse_header(
				self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')
			output = ""
			output += "<html><body>"
			output += "<h2> Okay, how about this: </h2>"
			output += "<h1> %s </h1>" % messagecontent[0]
			output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
			<h2>What would you like me to say?</h2><input name='message' type='text'>
			<input type='submit' value='Submit'></form>"""	
			output += "</body></html>"	
			self.wfile.write(output)
			print output
		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webServerHandler)
		print "Web server running on port %s" % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()  #runs main method