#Global configurations

videoStreamingCommand=['ffmpeg', '-s', 'hd480', '-i', '/dev/video0', '-an', 'http://xxxxxxxxxxxxxxxxxxxxxxxxxxxxx']
audioStreamingCommand=['ffmpeg', '-vn', '-f', 'alsa', '-ac', '1', '-i', 'hw:1', 'http://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx']
motor1DirectionOnePin = 5
motor1DirectionTwoPin = 6
motor2DirectionOnePin = 20
motor2DirectionTwoPin = 21
ultraSonicTrigger = 18
ultraSonicReciver = 24
