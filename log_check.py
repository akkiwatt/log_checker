import sys
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,send_file
from werkzeug import secure_filename
from geoip import geolite2


app = Flask(__name__)

#app.config['UPLOAD_FOLDER'] = 'static'

app.config['ALLOWED_EXTENSIONS'] = set(['txt','log','csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('sample.html')



@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        
        filename = secure_filename(file.filename)
	print filename
	file.save(filename)
	total_entry = list()
	all_dict = []	
	file_header =['HTTP_METHOD', 'URL', 'HTTP_VERSION', 'ORIGIN_HEADER', 'SSL_CIPHER', 'SSL_PROTOCOL', 'timestamp', 'elb', 'CLIENT_IP:port', 'BACKEND_IP:port', 'request_processing_time', 'backend_processing_time', 'response_processing_time', 'elb_status_code', 'backend_status_code', 'received_bytes', 'sent_bytes']
	print file_header
	log_entries = []
	input_file = open(filename)
	for i in input_file:
		i = i.replace("  "," ")
		#print i
		if "B R" in i:		
			i = i.replace("B R","B_R")
		#print i
		entry = i.split(" ")	
		log_entries.append(entry)	
		
	
	#print log_entries

	for i in log_entries:
		dict_temp ={}
		dict_temp["Log_Entry"]=str(i)	
		for j in range(len(i)):
			#print file_header[j]
			#print i[j]
			dict_temp[file_header[j]]=i[j]
		all_dict.append(dict_temp)

	output_file = open("result.csv","w")
	for i in all_dict:
		if 'MATLAB_R2013a'  in i["ORIGIN_HEADER"]:
			output_file.write('"%s","%s"\n'%						
				        ("Yes",i["Log_Entry"]))
		else:
			#index = i["CLIENT_IP:port"].index(':')
			#print index
			print i["CLIENT_IP:port"]
		
			
			match = geolite2.lookup(i["CLIENT_IP:port"].split(":")[0])
			
			print match.country
			if 'IN' in match.country:
				print match.country
				output_file.write('"%s","%s"\n'%						
			        ("No",i["Log_Entry"]))
			else:
				
				output_file.write('"%s","%s"\n'%						
			        ("Yes",i["Log_Entry"]))

		
	output_file.close()

	csv = "result.csv"

	#return send_file('static/result.csv',attachment_filename='log_information.csv')		
	return render_template("test.html",csv_name=csv)
    else:
	return "Please enter valid file format file should be in .csv,.txt and .log  "

@app.route('/processed_file', methods=['POST'])
def uploaded_file():
    	return send_file('result.csv')
	 

if __name__ == '__main__':
    app.run()
