#Global configurations

avrecordingcommand=['ffmpeg', '-i', 'http://<streaming host>:<port>/<video stream name>', '-i', 'http://<streaming host>:<port>/<video stream name>','-f', 'flv', '-vf', 'setpts=5.0*PTS', '-vcodec','libx264', '-acodec', 'copy', '-t', '20', './temp/{}.flv']
