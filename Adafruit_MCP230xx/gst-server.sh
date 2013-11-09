
#!/bin/tcsh

set myip=192.168.5.125
set port=5001
set width=320
set height=240

gst-launch\
  v4l2src !\
  ffmpegcolorspace !\
  video/x-raw-yuv,width=${width},height=${height},framerate=\(fraction\)30/1 !\
  jpegenc !\
  tcpserversink host=${myip} port=${port} sync=false
