from flask import Flask, jsonify, request
from AVrecorder import avrecorder

app=Flask(__name__)

@app.route('/',methods=['GET'])
def test():
	return jsonify({'state':'running'})
	

@app.route('/recordstream/<string:filename>',methods=['GET'])
def recordstream(filename):
	print("Request recieved to print {}".format(filename))
        newavRecorder = avrecorder(filename)
	newavRecorder.startRecording();
        return jsonify({'called':True})
	
@app.route('/downloadfile/<string:filename>',methods=['GET'])
def stopstream(filename):
        return jsonify({'terminated':True})
		
if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True,port=8080)
