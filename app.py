from flask import Flask, Response
import cv2
from main import SignLanguageInterpreter 

app = Flask(__name__)
#inherit sign language class
interpreter = SignLanguageInterpreter()

#method to read from webcam video feed and process video
def generate_frames():
    while True:
        ret, frame = interpreter.cap.read()
        processed_frame, prediction = interpreter.process_frame(frame)
        
        if ret:
            _, buffer = cv2.imencode('.jpg', processed_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
