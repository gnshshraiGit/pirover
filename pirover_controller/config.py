#Global configurations

videoStreamingCommand=['ffmpeg', '-s', 'hd480', '-i', '/dev/video0', '-an', '<video feed stream>']
audioStreamingCommand=['ffmpeg', '-vn', '-f', 'alsa', '-ac', '1', '-i', 'hw:1', '<sound feed stream>']
