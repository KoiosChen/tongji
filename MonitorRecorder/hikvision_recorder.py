import cv2
import uuid
import datetime
import os
import uuid

cap = cv2.VideoCapture("rtsp://admin:Admin123@10.170.0.100:554//Streaming/Channels/1")
# cap = cv2.VideoCapture("rtsp://username:passport@ip:port/Streaming/Channels/1")
fps = int(cap.get(cv2.CAP_PROP_FPS))
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

filename = str(uuid.uuid1())
start_time = datetime.datetime.now()

videoWriter = cv2.VideoWriter('video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
ret,frame = cap.read()
while ret:
	ret,frame = cap.read()
	#cv2.imshow("frame",frame)
	videoWriter.write(frame)
	if cv2.waitKey(1) & 0xFF == ord('q') or datetime.datetime.now() - start_time > datetime.timedelta(seconds=6):
		break

videoWriter.release()
cap.release()
os.system('ffmpeg -i video.mp4 -vcodec libx264 -f mp4 {}.mp4'.format(str(uuid.uuid1())))
