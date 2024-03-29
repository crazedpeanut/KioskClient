'''
Author: John Kendall
Date: 18/12/14

Description: HTTP functions to send and recieve messages/data to and from a webserver
'''

import http.client
import urllib
import debug as dbug
import gzip
import settings
import requests

DATA_FILE = settings.STORED_REQUESTS_FILE
ENCODING = settings.ENCODING
HTTP_CONN_DEBUG_LVL = 0

def send_file(host, port, url, files):
    request_url = 'http://' + host + ':' + str(port) + url

    try:
        r = requests.post(request_url, files=files, timeout=settings.HTTP_TIMEOUT)

        return r.text
    except Exception as e:
        dbug.debug(str(e))
        return None

def http_request(params):
    host = params["host"]
    port = params["port"]
    method = params["method"]
    resource = params["resource"]
    data = params["data"]
    callback = params["result_callback"]
    connection_failed_callback = params["connection_failed_callback"];
	
    data = urllib.parse.urlencode(data)

    conn = http.client.HTTPConnection(host, port)
    conn.set_debuglevel(HTTP_CONN_DEBUG_LVL)

    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"} 
    try:	
        conn.request(method, resource, data, headers)
        
        response = conn.getresponse()
        result = response.read()
        print(result.decode(ENCODING))
        conn.close()
        
        f = open("tmp.txt.gz", "wb")
        f.write(result)

        f.close()
        f = gzip.open("tmp.txt.gz", "r")
        result = f.read()
        f.close()

        callback(result)

        f = open(DATA_FILE, "w")
        f.write("") #Clear file with queued messages

        f.close()
    
    except Exception as e:
        dbug.debug("Connection Failed: "+ str(e))
        connection_failed_callback(data)
        
def http_request_2(host, port, method, resource, data):

    print(data)
    data = urllib.parse.urlencode(data)
    print(data)
    conn = http.client.HTTPConnection(host, port)
    conn.set_debuglevel(HTTP_CONN_DEBUG_LVL)

    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"} 
    try:    
        conn.request(method, resource, data, headers)
        
        response = conn.getresponse()
        result = response.read()
        print(result) 
        conn.close() 
        return result
    
    except Exception as e:
        dbug.debug("Connection Failed: "+ str(e))
        return None
        

