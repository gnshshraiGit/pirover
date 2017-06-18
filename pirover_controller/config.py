#Global configurations

videoStreamingCommand=['ffmpeg', '-r', '15', '-s', '640x480', '-i', '/dev/video0', '-vf' ,'"setpts=1.5*PTS"', 'http://<hostrunning ffserver>:<port>/<feed name>']
audioStreamingCommand=['ffmpeg', '-f', 'alsa', '-ac', '1', '-i', 'hw:1', '-acodec', 'aac','http://<hostrunning ffserver>:<port>/<audiofeed name>']
