from datetime import datetime
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
    print(f"{datetime.now().strftime('%H:%M:%S.%f')} - Objects GET called") 
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
    id = request.args.get('id')
    exact_match = request.args.get('exact_match', 'false').lower() == 'true'

    if not name and not id:
        return jsonify({"error": "Missing 'name' or 'id' parameter"}), 400
    
    if name and id:
        return jsonify({"error": "Use 'name' or 'id' parameter, not both"}), 400
    
    if name:
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
    elif id:
        track = TrackDb.query.get(id)
        if track:
            return jsonify({ 
                "id": track.id, "song": track.song, "artist": track.artist, "streams": track.streams, 
                "daily_streams": track.daily_streams, "genre": track.genre, "release_year": track.release_year,
                "peak_position": track.peak_position, "weeks_on_chart": track.weeks_on_chart,
                "lyrics_sentiment": track.lyrics_sentiment, "tiktok_virality": track.tiktok_virality,
                "danceability": track.danceability, "acousticness": track.acousticness, "energy": track.energy 
            })
    
    return jsonify({"error": "Track not found"}), 404

# -------------------- POST create new track --------------------
@app.route('/object', methods=['POST'])
def add_track():
    data_list = request.json
    if not isinstance(data_list, list):
        return jsonify({"error": "Expected a list of track data"}), 400
    
    if not data_list or not all(isinstance(data, dict) for data in data_list):
        return jsonify({"error": "Invalid data format. Expected a list of dictionaries."}), 400

    for data in data_list:
        if not all(key in data for key in ["song", "artist", "streams", "daily_streams", "genre", "release_year", "peak_position", "weeks_on_chart", "lyrics_sentiment", "tiktok_virality", "danceability", "acousticness", "energy"]):
            return jsonify({"error": "Invalid data. Missing required keys in one of the track data"}), 400

    new_tracks = [TrackDb(**data) for data in data_list]
    db_sqlalchemy.session.add_all(new_tracks)
    db_sqlalchemy.session.commit()
    
    track_ids = [track.id for track in new_tracks]
    
    return jsonify({"message": "Tracks created", "ids": track_ids}), 201


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


# -------------------- DELETE remove track by id --------------------
@app.route('/object', methods=['DELETE'])
def delete_track():
    track_id = request.args.get('id')
    if not track_id:
        return jsonify({"error": "Missing 'id' parameter"}), 400

    track = TrackDb.query.get(track_id)
    if not track:
        return jsonify({"error": "Track not found"}), 404

    db_sqlalchemy.session.delete(track)
    db_sqlalchemy.session.commit()
    return jsonify({"message": "Track deleted"}), 200

# -------------------- DELETE remove all tracks --------------------
@app.route('/objects', methods=['DELETE'])
def delete_all_tracks():
    try:
        num_rows_deleted = db_sqlalchemy.session.query(TrackDb).delete()
        db_sqlalchemy.session.commit()
        return jsonify({"message": f"{num_rows_deleted} tracks deleted"}), 200
    except Exception as e:
        db_sqlalchemy.session.rollback()
        return jsonify({"error": str(e)}), 500



# -------------------- Start Flask server --------------------
if __name__ == '__main__':
    if args.debug:
        app.run(debug=True, port=int(os.environ.get('PORT', args.port)))
    else:
        app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', args.port)))
