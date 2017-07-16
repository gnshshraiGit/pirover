from AVstreamer import avstreamer
from walker import walker
from socketIO_client import BaseNamespace

isBusy = False
curntServing = None

class Pirover_StreamerCmdSocket(BaseNamespace):
        def on_connect(self):
                print('Pi rover connected to server')
                
        def startStream(self, data):
                avstreamer.startStream()
        
        def stopstream(self, data):
                avstreamer.stopStream()

        def restream(self, data):
                avstreamer.reStream()
                

class Pirover_WalkerCmdSocket(BaseNamespace):
        def on_connect(self):
                print('Pi rover connected to server')
                
        def goFwd(self, data):
                global isBusy
                global curntServing
                if not isBusy:
                        curntServing = data['sid']
                        isBusy = True
                        walker.direction = 'w'
                        walker.runRover(self,curntServing)
                        return
                else:
                        self.emit('status',{'sid': data['sid'],'err':'Rover is busy serving another user'})
                        return

        def goRit(self, data):
                global isBusy
                global curntServing
                if not isBusy:
                        curntServing = data['sid']
                        isBusy = True
                        walker.direction = 'd'
                        walker.runRover(self,curntServing)
                        return
                else:
                        self.emit('status',{'sid': data['sid'],'err':'Rover is busy serving another user'})
                        return

        def goLft(self, data):
                global isBusy
                global curntServing
                if not isBusy:
                        curntServing = data['sid']
                        isBusy = True
                        walker.direction = 'a'
                        walker.runRover(self,curntServing)
                        return
                else:
                        self.emit('status',{'sid': data['sid'],'err':'Rover is busy serving another user'})
                        return

        def goBkd(self, data):
                global isBusy
                global curntServing
                if not isBusy:
                        curntServing = data['sid']
                        isBusy = True
                        walker.direction = 's'
                        walker.runRover(self,curntServing)
                        return
                else:
                        self.emit('status',{'sid': data['sid'],'err':'Rover is busy serving another user'})
                        return
                        
        def stop(self, data):
                global isBusy
                global curntServing
                if curntServing != data['sid']:
                        self.emit('status',{'sid': data['sid'],'err':'Rover is busy serving another user'})
                        return
                if isBusy:
                        walker.direction = 'l'
                        walker.runRover(self,curntServing)
                        isBusy = False
                        curntServing = None
                        return

        def estop(self, data):
                global isBusy
                global curntServing
                if curntServing == None:
                        walker.direction = 'l'
                        walker.runRover(self,curntServing)
                        isBusy = False
                        curntServing = None
                        walker.cleanup()
                return
