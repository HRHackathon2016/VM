from sklearn.ensemble import RandomForestClassifier as rfc
from urlparse import urlparse
from urlparse import parse_qs
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json

PORT_NUMBER = 8081

total_data = []
total_target = []


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        result = {'success': False}
        if self.path.startswith("/feed?"):
            query = parse_qs(urlparse(self.path).query)
            data = map(int, query['data'][0].split(','))
            target = query['target'][0]
            total_data.append(data)
            total_target.append(target)
            result = {'success': True}
        if self.path.startswith("/predict?"):
            query = parse_qs(urlparse(self.path).query)
            data = map(int, query['data'][0].split(','))
            clf = rfc(random_state=4)
            clf.fit(total_data, total_target)
            result = {}
            prediction = map(float, clf.predict_proba([data])[0])
            for p in prediction:
                result[clf.classes_[len(result)]] = p
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # Send the html message
        self.wfile.write(json.dumps(result))
        return

try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), MyHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
