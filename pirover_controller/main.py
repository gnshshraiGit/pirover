from flask import Flask, jsonify, request
from AVstreamer import avstreamer
from walker import walker
import asyncio
import time

isBusy = False

def launchCleanup(timeSec):
        try:
                while True:
                        time.sleep(timeSec)
                        if not isBusy:
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

cleanUpLoop = setInterval(launchCleanup,180)

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

@app.route('/restream',methods=['GET'])
def restream():
        avstreamer.reStream()
        return jsonify({'reStreamed':True})

@app.route('/goFwd',methods=['GET'])
def goFwd():
        global isBusy
        if not isBusy:
                isBusy = True
                walker.direction = 'w'
                walker.runRover()
                return jsonify({'walking':'Forward'})
        else:
                return jsonify({'isBusy':isBusy})

@app.route('/goRit',methods=['GET'])
def goRit():
        global isBusy
        if not isBusy:
                isBusy = True
                walker.direction = 'd'
                walker.runRover()
                return jsonify({'walking':'Right'})
        else:
                return jsonify({'isBusy':isBusy})

@app.route('/goLft',methods=['GET'])
def goLft():
        global isBusy
        if not isBusy:
                isBusy = True
                walker.direction = 'a'
                walker.runRover()
                return jsonify({'walking':'Left'})
        else:
                return jsonify({'isBusy':isBusy})

@app.route('/goBkd',methods=['GET'])
def goBkd():
        global isBusy
        if not isBusy:
                isBusy = True
                walker.direction = 's'
                walker.runRover()
                return jsonify({'walking':'Backward'})
        else:
                return jsonify({'isBusy':isBusy})

@app.route('/stop',methods=['GET'])
def stop():
        global isBusy
        if isBusy:
                isBusy = False
                walker.direction = 'l'
                walker.runRover()
                return jsonify({'walking':'Stoped'})
        else:
                return jsonify({'isBusy':isBusy})

@app.route('/estop',methods=['GET'])
def estop():
        global isBusy
        isBusy = False
        walker.direction = 'l'
        walker.runRover()
        walker.cleanup()
        return jsonify({'walking':'eStoped'})
        
		
if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True,port=8080)

