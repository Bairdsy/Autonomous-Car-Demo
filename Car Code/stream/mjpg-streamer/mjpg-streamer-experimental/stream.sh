./mjpg_streamer -i "input_uvc.so -rot 180 -r 640x480 -d /dev/video0 -f 30 -q 80" -o "output_http.so -p 8080 -w /usr/local/share/mjpg-streamer/www"

