# Python 3 server example
import json
import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

import numpy
from pyngrok import ngrok
import cgi
from Predictor import predict

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        import urllib
        currDemand = urllib.parse.parse_qs(self.path)
        new_dict = {}
        for key in currDemand.keys():
            if  key.startswith("/?"):
                new_key = key[2:]
            else:
                new_key = key
            new_dict[new_key] = currDemand[key]
        print(new_dict)

        if "vec" in list(new_dict.keys()):
            value_vec = (new_dict["vec"][0])[1:-1].split(",")
            features = numpy.array([int(val) for val in value_vec])
            difficulty, time = predict(features)
            print(difficulty)
            print(time)
            json_str = json.dumps([difficulty, time])
            self.send_response(200, f"{difficulty},{time}")
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json_str.encode(encoding='utf_8'))



    def do_POST(self):
        length = int(self.headers['content-length'])
        if length > 10000000:
            read = 0
            while read < length:
                read += len(self.rfile.read(min(66556, length - read)))
            self.respond("file to big")
            return
        else:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            print(form.keys())
            features = 0
            result = predict(features)
            json_str = json.dumps(result)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json_str.encode(encoding='utf_8'))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    ssh_tunnel = ngrok.connect(8080)
    print(ssh_tunnel)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")