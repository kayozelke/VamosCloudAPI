from flask import Flask, request, jsonify
from database_module import init_db, TrackDb

app = Flask(__name__)

# Database configuration (using MySQL from config)
app.config['DATABASE'] = {
    'username': 'flask_test',
    'password': 'flask_test',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'vamos_cloud_app'
}

# Inicjalizujemy SQLAlchemy i model TrackDb
db_sqlalchemy = init_db(app)

# Create tables if they do not exist
with app.app_context():
    db_sqlalchemy.create_all()

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
    if not name:
        return jsonify({"error": "Missing 'name' parameter"}), 400
    
    track = TrackDb.query.filter_by(song=name).first()
    
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
    app.run(debug=True)
