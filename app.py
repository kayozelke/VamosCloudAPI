import os
from flask import Flask, request, jsonify
from src.database_module import init_db, TrackDb
from src.config_module import loadConfig

import argparse

parser = argparse.ArgumentParser(description='Run the Flask application.')
parser.add_argument('-p','--port', type=int, default=80, help='Port to run the application on.')
parser.add_argument('-d','--debug', action='store_true', help='Enable debug mode.')
args = parser.parse_args()



app = Flask(__name__)

# Create tables if they do not exist
with app.app_context():
    config = loadConfig(config_path="api_config.ini") 
    app.config['DATABASE'] = config['DATABASE']
    
    db_sqlalchemy = init_db(app)
    
    db_sqlalchemy.create_all()
    

@app.route('/', methods=['GET'])
def index():
    return '<h1>The API works fine!</h1>'
    

# -------------------- GET all tracks --------------------
@app.route('/objects', methods=['GET'])
def get_tracks():
    tracks = TrackDb.query.all()
    return jsonify([{ "id": track.id, "song": track.song, "artist": track.artist, "streams": track.streams, 
                        "daily_streams": track.daily_streams, "genre": track.genre, "release_year": track.release_year,
                        "peak_position": track.peak_position, "weeks_on_chart": track.weeks_on_chart,
                        "lyrics_sentiment": track.lyrics_sentiment, "tiktok_virality": track.tiktok_virality,
                        "danceability": track.danceability, "acousticness": track.acousticness, "energy": track.energy}
                    for track in tracks])

# -------------------- GET track by song name --------------------
@app.route('/object', methods=['GET'])
def get_track_by_name():
    name = request.args.get('name')
    exact_match = request.args.get('exact_match', 'false').lower() == 'true'

    if not name:
        return jsonify({"error": "Missing 'name' parameter"}), 400
    
    if exact_match:
        track = TrackDb.query.filter_by(song=name).first()
    else:
        track = TrackDb.query.filter(TrackDb.song.ilike(f"%{name}%")).first()
    
    if track:
        return jsonify({ 
            "id": track.id, "song": track.song, "artist": track.artist, "streams": track.streams, 
            "daily_streams": track.daily_streams, "genre": track.genre, "release_year": track.release_year,
            "peak_position": track.peak_position, "weeks_on_chart": track.weeks_on_chart,
            "lyrics_sentiment": track.lyrics_sentiment, "tiktok_virality": track.tiktok_virality,
            "danceability": track.danceability, "acousticness": track.acousticness, "energy": track.energy 
        })
    else:
        return jsonify({"error": "Track not found"}), 404

# -------------------- POST create new track --------------------
@app.route('/object', methods=['POST'])
def add_track():
    data = request.json
    if not data or not all(key in data for key in ["song", "artist", "streams", "daily_streams", "genre", "release_year", "peak_position", "weeks_on_chart", "lyrics_sentiment", "tiktok_virality", "danceability", "acousticness", "energy"]):
        return jsonify({"error": "Invalid data"}), 400

    new_track = TrackDb(**data)
    db_sqlalchemy.session.add(new_track)
    db_sqlalchemy.session.commit()
    
    return jsonify({"message": "Track created", "id": new_track.id}), 201

# -------------------- PUT update existing track --------------------
@app.route('/object', methods=['PUT'])
def update_track():
    data = request.json
    if not data or "id" not in data:
        return jsonify({"error": "Invalid data"}), 400

    track = TrackDb.query.get(data["id"])
    if not track:
        return jsonify({"error": "Track not found"}), 404

    for key, value in data.items():
        if hasattr(track, key):
            setattr(track, key, value)
    
    db_sqlalchemy.session.commit()
    return jsonify({"message": "Track updated"}), 200

# -------------------- Start Flask server --------------------
if __name__ == '__main__':
    if args.debug:
        app.run(debug=True, port=int(os.environ.get('PORT', args.port)))
    else:
        app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', args.port)))
