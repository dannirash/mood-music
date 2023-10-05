from flask import Flask, Response, request, send_file
#from camera import VideoCamera
from image_processing import process_image
import pandas as pd
from flask_cors import CORS, cross_origin
from markupsafe import escape
import tkinter as tk

app = Flask(__name__)
cors = CORS(app)
DataFrame = pd.read_csv(r"data_moods.csv")

def choose_genre(pred_class):
    if( pred_class=='disgust' ):
        return 'sad' 
    elif( pred_class=='happy' or pred_class=='sad' ):
            return 'happy' 
    elif( pred_class=='scared' or pred_class=='angry' ):
            return 'calm' 
    elif( pred_class=='surprised' or pred_class=='neutral' ):
            return 'energetic'
    else:
        return pred_class
    
@app.route('/songs', methods=['GET'])
@cross_origin()
def DataSort():
    user_mood = request.args.get('arg1').lower()
    genre = choose_genre(user_mood) 
    print("Suggesting:" + genre)
    sortedDF = DataFrame[DataFrame["mood"].str.lower() == genre]
    sortedDF = sortedDF.sort_values(by="popularity", ascending=False)
    return Response(sortedDF[["name", "album", "artist", "id", "mood"]].to_json(orient='records'), status=200, mimetype='application/json')

@app.route('/camera', methods=['POST'])
def process_image_endpoint():
    try:
        snapshot_file = request.files['snapshot']
        if snapshot_file:
            # Save the snapshot to a specific path
            snapshot_path = 'pics/snapshot.jpg'
            snapshot_file.save(snapshot_path)
             # Call the image processing function
            annotated_snapshot_path, label = process_image(snapshot_path)
            # Return the annotated image
            print("You are Feeling:")
            print(label)
            return Response(label, status=200, mimetype="text/plain") 
        else:
            return 'Snapshot file not found', 400
    except Exception as e:
        return f'Error processing image: {str(e)}', 500

if __name__ == "__main__":
    app.run(debug=True)

'''    
# Route to access the camera feed
@app.route('/camera', methods=['GET'])
def camera_feed():
    # Create an instance of VideoCamera
    root = tk.Tk()
    video_camera = VideoCamera(root)
    root.mainloop()
    
    def generate():
        video_camera.start()  # Start the camera when the feed is requested
        try:
            while True:
                frame = video_camera.update()
                if frame is not None:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except GeneratorExit:
            # Clean up when the generator is closed (e.g., client disconnects)
            video_camera.stop()

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
'''