from flask import Flask, jsonify, request
from AVstreamer import avstreamer

app=Flask(__name__)

@app.route('/',methods=['GET'])
def test():
	return jsonify({'state':'running'})
	

@app.route('/startstream',methods=['GET'])
def startstream():
        avstreamer.startStream()     
        return jsonify({'called':True})
	
@app.route('/stopstream',methods=['GET'])
def stopstream():
        avstreamer.stopStream()
        return jsonify({'terminated':True})
		
if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True,port=8080)

