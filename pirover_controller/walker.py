import RPi.GPIO as GPIO
import time
import asyncio
import sys
import config as cfg

class walker:

    isInitialized = False

    @classmethod    
    def init(cls):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(cfg.motor1DirectionOnePin, GPIO.OUT)
        GPIO.setup(cfg.motor1DirectionTwoPin, GPIO.OUT)
        GPIO.setup(cfg.motor2DirectionOnePin, GPIO.OUT)
        GPIO.setup(cfg.motor2DirectionTwoPin, GPIO.OUT)
        GPIO.setup(cfg.ultraSonicTrigger, GPIO.OUT)
        GPIO.setup(cfg.ultraSonicReciver, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        print ("Motor 1 Direction one")
        GPIO.output(cfg.motor1DirectionOnePin, False)

        print ("Motor 1 Direction two")
        GPIO.output(cfg.motor1DirectionTwoPin, False)

        print ("Motor 2 Direction one")
        GPIO.output(cfg.motor2DirectionOnePin, False)

        print ("Motor 2 Direction two")
        GPIO.output(cfg.motor2DirectionTwoPin, False)

        print("Setting False Sonar trigger")
        GPIO.output(cfg.ultraSonicTrigger, False)

        #Mapping keys to movement functions
        cls.movement = {
                    'w':cls.goFwd,
                    's':cls.goBkd,
                    'a':cls.goLft,
                    'd':cls.goRit,
                    'l':cls.stop,
                    'c':cls.cleanup
                }
        print('initializing IO Loop')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        cls.ioloop = asyncio.get_event_loop()
        cls.ioloop.run_in_executor(None,cls.hndlObstacle)
        cls.isObstacle = False
        cls.isInitialized = True

    @asyncio.coroutine
    def goFwd(cls):
        GPIO.output(cfg.motor1DirectionTwoPin, False)
        GPIO.output(cfg.motor2DirectionTwoPin, False)
        GPIO.output(cfg.motor1DirectionOnePin, True)
        GPIO.output(cfg.motor2DirectionOnePin, True)

    @asyncio.coroutine
    def goBkd(cls):
        GPIO.output(cfg.motor1DirectionOnePin, False)
        GPIO.output(cfg.motor2DirectionOnePin, False)
        GPIO.output(cfg.motor1DirectionTwoPin, True)
        GPIO.output(cfg.motor2DirectionTwoPin, True)

    @asyncio.coroutine
    def goLft(cls):
        GPIO.output(cfg.motor1DirectionOnePin, False)
        GPIO.output(cfg.motor2DirectionOnePin, True)
        GPIO.output(cfg.motor1DirectionTwoPin, True)
        GPIO.output(cfg.motor2DirectionTwoPin, False)

    @asyncio.coroutine
    def goRit(cls):
        GPIO.output(cfg.motor1DirectionOnePin, True)
        GPIO.output(cfg.motor2DirectionOnePin, False)
        GPIO.output(cfg.motor1DirectionTwoPin, False)
        GPIO.output(cfg.motor2DirectionTwoPin, True)

    @asyncio.coroutine
    def stop(cls):
        GPIO.output(cfg.motor1DirectionOnePin, False)
        GPIO.output(cfg.motor2DirectionOnePin, False)
        GPIO.output(cfg.motor1DirectionTwoPin, False)
        GPIO.output(cfg.motor2DirectionTwoPin, False)


    @classmethod
    def cleanup(cls):
        if cls.isInitialized is True:
            try:
                cls.ioloop.stop()
            finally:
                GPIO.cleanup()
                cls.ioloop.close()
                cls.isInitialized = False

    @classmethod
    def hndlObstacle(cls):
        #pdb.set_trace()
        while True:
            time.sleep(0.5)
            GPIO.output(cfg.ultraSonicTrigger, True)
            time.sleep(0.00001)
            GPIO.output(cfg.ultraSonicTrigger, False)
            while GPIO.input(cfg.ultraSonicReciver) == 0:
                            StartTime = time.time()
            while GPIO.input(cfg.ultraSonicReciver) == 1:
                            StopTime = time.time()
            TimeElapsed = StopTime - StartTime
            distance = (TimeElapsed * 17150)
            print(distance)
            if distance <= 15 or distance > 600:
                cls.ioloop.run_until_complete(cls.goBkd(cls))
                time.sleep(0.5)
                cls.ioloop.run_until_complete(cls.goRit(cls))
                time.sleep(0.5)
                cls.ioloop.run_until_complete(cls.goFwd(cls))

    @classmethod
    def runRover(cls):
        if not cls.isInitialized:
            cls.init()
        if cls.isObstacle == False:
            if cls.direction != None:
                cls.ioloop.run_until_complete(cls.movement[cls.direction](cls))
                time.sleep(0.2)
                cls.direction = None
        else:
            pass
