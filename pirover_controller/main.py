from AVstreamer import avstreamer
from walker import walker
from piroversockets import Pirover_StreamerCmdSocket, Pirover_WalkerCmdSocket
from socketIO_client import SocketIO, LoggingNamespace
import piroversockets
import asyncio
import config as cfg
import time


def launchCleanup(timeSec):
        try:
                while True:
                        time.sleep(timeSec)
                        print('Check Cleanup')
                        print('Busy status {}'.format(piroversockets.isBusy))
                        if not piroversockets.isBusy:
                                print('Initializing Cleanup')
                                avstreamer.stopStream()
                                walker.cleanup()
        except KeyboardInterrupt:
            print("Key board interrupt")
        finally:
            walker.cleanup()                                

def setInterval(func,timeSec):
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None,func,timeSec)
        return loop

cleanUpLoop = setInterval(launchCleanup,cfg.cleanupTimeOut) #TODO:need to improve here , it should reset eventloop timer on every message recieved on socket

#start socket client

socketIO = SocketIO(cfg.socketIOHost, cfg.socketIOHostPort, LoggingNamespace)


streamCmdSock = socketIO.define(Pirover_StreamerCmdSocket,'/StreamCmdSock')
streamCmdSock.on('startstream',streamCmdSock.startStream)
streamCmdSock.on('stopstream',streamCmdSock.stopstream)
streamCmdSock.on('restream',streamCmdSock.restream)


walkCmdSock = socketIO.define(Pirover_WalkerCmdSocket,'/WalkCmdSock')
walkCmdSock.on('gofwd',walkCmdSock.goFwd)
walkCmdSock.on('gorit',walkCmdSock.goRit)
walkCmdSock.on('golft',walkCmdSock.goLft)
walkCmdSock.on('gobkd',walkCmdSock.goBkd)
walkCmdSock.on('stop',walkCmdSock.stop)
walkCmdSock.on('estop',walkCmdSock.estop)

socketIO.wait()
