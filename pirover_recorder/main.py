from piroversockets import Pirover_RecorderSocket
from socketIO_client import SocketIO, LoggingNamespace
import config as cfg

socketIO = SocketIO(cfg.socketIOHost, cfg.socketIOHostPort, LoggingNamespace)

recorderSock = socketIO.define(Pirover_RecorderSocket, '/RecorderCmdSock')
recorderSock.on('startrecording', recorderSock.startRecording)

socketIO.wait()
