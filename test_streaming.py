plt.rcParams["figure.figsize"] = (14,7)
f, axes = plt.subplots(2,2)

def gen():
	while True:
		
		f.canvas.draw()
		img = np.fromstring(f.canvas.tostring_rgb(), dtype=np.uint8, sep='')
		img  = img.reshape(f.canvas.get_width_height()[::-1] + (3,))
		img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
		_,jpeg = cv2.imencode('.jpg',img)

		frame = jpeg.tobytes()
		yield(b'--frame\r\n'
		b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def img(request):

	try:
		return StreamingHttpResponse(gen(),content_type="multipart/x-mixed-replace;boundary=frame")
	except HttpResponseServerError as e:
		print("aborted")

