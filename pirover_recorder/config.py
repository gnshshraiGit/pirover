#Global configurations

avrecordingcommand=['ffmpeg', '-i', 'video stream', '-i', 'audio stream','-f', 'flv', '-vf', 'setpts=5*PTS', '-vcodec','libx264', '-acodec', 'copy', '-t', '{}', './temp/{}.flv']
storageAc = 'azure storage account'
storageAcUrl = 'azure storage account url'
accountkey='azure storage account key'
fileShare = 'videorecord'
downloadLinkFormat='{}/{}/{}.flv?{}'
socketIOHost = 'socketIO host'
socketIOHostPort = 'socketIO port'
timeBeforeFileDelete = 600
timeToShoot = 30
