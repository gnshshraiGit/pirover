from subprocess import Popen
from threading import Thread
import config as cfg
import time

class avrecorder:
	
	def __init__(self,filename):
		self.filename = filename
		
	def startRecording(self):
		def recordingProc(me):
			avrecordingCommand = list(cfg.avrecordingcommand)
			avrecordingCommand[-1] = avrecordingCommand[-1].format(me.filename)
			avrecordingHandle = Popen(avrecordingCommand)
			avrecordingHandle.wait()
			me.onRecordingComplete()
			return
		self.thread = Thread(target=recordingProc, args=(self,))
		self.thread.start()
		return
	def onRecordingComplete(self):
		print("recording completed {}".format(self.filename))
		return




