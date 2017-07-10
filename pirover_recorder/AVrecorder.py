from subprocess import Popen
from threading import Thread
from azure.storage.file import FileService, FilePermissions
from azure.storage import SharedAccessSignature
from datetime import datetime,timedelta
import config as cfg
import time
import os

class avrecorder:
	
	def __init__(self,filename, sid, recorderSock):
		self.filename = filename
		self.sid = sid
		self.recorderSock = recorderSock
		
	def startRecording(self):
		def recordingProc(me):
			avrecordingCommand = list(cfg.avrecordingcommand)
			avrecordingCommand[-1] = avrecordingCommand[-1].format(me.filename)
			avrecordingCommand[-2] = avrecordingCommand[-2].format(cfg.timeToShoot)
			avrecordingHandle = Popen(avrecordingCommand)
			avrecordingHandle.wait()
			me.onRecordingComplete()
			return
		self.thread = Thread(target=recordingProc, args=(self,))
		self.thread.start()
		return

	def onRecordingComplete(self):
		print("recording completed {}".format(self.filename))
		file_service = FileService(account_name=cfg.storageAc, account_key=cfg.accountkey)
		file_service.create_file_from_path(cfg.fileShare, None,'{}.flv'.format(self.filename),'temp/{}.flv'.format(self.filename))
		sharedAccessStorage = SharedAccessSignature(cfg.storageAc,cfg.accountkey)
		sasKey = sharedAccessStorage.generate_file(cfg.fileShare,file_name='{}.flv'.format(self.filename), permission= FilePermissions.READ, 				start=datetime.utcnow(),expiry=datetime.utcnow()+timedelta(minutes=5))
		downloadLink = cfg.downloadLinkFormat.format(cfg.storageAcUrl,cfg.fileShare,self.filename,sasKey);
		self.recorderSock.emit('recordingcomplete',{'sid':self.sid,'download':downloadLink})
		os.remove('temp/{}.flv'.format(self.filename))		
		time.sleep(cfg.timeBeforeFileDelete)
		file_service.delete_file(cfg.fileShare, None,'{}.flv'.format(self.filename))
		return




