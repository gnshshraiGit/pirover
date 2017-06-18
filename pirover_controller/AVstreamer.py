from subprocess import Popen
import config as cfg
import time

class avstreamer:
    sendVideoStreamHandle = False
    sendAudioStreamHandle = False
    
    @classmethod
    def startStream(cls):
        if avstreamer.isStreaming() == False:
            cls.sendVideoStreamHandle = Popen(cfg.videoStreamingCommand)
            cls.sendAudioStreamHandle = Popen(cfg.audioStreamingCommand)
            time.sleep(2)
            while cls.sendVideoStreamHandle.poll() == 1:
                    cls.sendVideoStreamHandle = Popen(cfg.videoStreamingCommand)
                    time.sleep(2)
            while cls.sendAudioStreamHandle.poll() == 1:	
                    cls.sendAudioStreamHandle = Popen(cfg.audioStreamingCommand)
                    time.sleep(2)
    
    @classmethod
    def stopStream(cls):
        if avstreamer.isStreaming() == True:
            while True:
                    if cls.sendVideoStreamHandle != False and cls.sendVideoStreamHandle.poll() is None:
                            cls.sendVideoStreamHandle.terminate()
                    else:
                            break
            while True:
                    if cls.sendAudioStreamHandle != False and cls.sendAudioStreamHandle.poll() is None:
                            cls.sendAudioStreamHandle.terminate()
                    else:
                            break
                        
    @classmethod               
    def isStreaming(cls):
        if cls.sendVideoStreamHandle == False or cls.sendAudioStreamHandle == False:
            return False;
        if cls.sendVideoStreamHandle.poll() is None and cls.sendAudioStreamHandle.poll() is None:
            return True
        else:
            return False;
