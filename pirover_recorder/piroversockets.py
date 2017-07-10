from AVrecorder import avrecorder
from socketIO_client import SocketIO, BaseNamespace

class Pirover_RecorderSocket(BaseNamespace):
	def on_connect(self):
		print('Recorder connected to Server')

	def startRecording(self, data):
		filename = data['filename']
		sid = data['sid']
		print("Request recieved to encode {}".format(filename))
        	newavRecorder = avrecorder(filename, sid, self)
		newavRecorder.startRecording();
