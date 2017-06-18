#Global configurations

videoStreamingCommand=['ffmpeg', '-r', '15', '-s', '640x480', '-i', '/dev/video0', '-vf' ,'"setpts=1.5*PTS"', 'http://<media server>/<video feed>']
audioStreamingCommand=['ffmpeg', '-f', 'alsa', '-ac', '1', '-i', 'default', '-acodec', 'aac','http://<media server>/<sound feed>']
