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


# # Create tables if they do not exist
# with app.app_context():
#     db_engine = db.get_engine_from_config(config)
#     db.check_and_create_tables(engine=db_engine)

# # -------------------- GET all tracks --------------------
# @app.route('/objects', methods=['GET'])
# def get_tracks():
#     return jsonify(db.get_tracks(engine=db_engine))

# # -------------------- GET track by song name --------------------
# @app.route('/object', methods=['GET'])
# def get_track_by_name():
#     name = request.args.get('name')
#     if not name:
#         return jsonify({"error": "Missing 'name' parameter"}), 400
    
#     track = db.TrackDb.query.filter_by(song=name).first()
#     if track:
#         return jsonify({ "id": track.id, "song": track.song, "artist": track.artist, "streams": track.streams, 
#                             "daily_streams": track.daily_streams, "genre": track.genre, "release_year": track.release_year,
#                             "peak_position": track.peak_position, "weeks_on_chart": track.weeks_on_chart,
#                             "lyrics_sentiment": track.lyrics_sentiment, "tiktok_virality": track.tiktok_virality,
#                             "danceability": track.danceability, "acousticness": track.acousticness, "energy": track.energy })
#     else:
#         return jsonify({"error": "Track not found"}), 404


# # -------------------- POST create new track --------------------
# @app.route('/track', methods=['POST'])
# def add_track():
#     data = request.json
#     if not data or not all(key in data for key in ["song", "artist", "streams", "daily_streams", "genre", "release_year", "peak_position", "weeks_on_chart", "lyrics_sentiment", "tiktok_virality", "danceability", "acousticness", "energy"]):
#         return jsonify({"error": "Invalid data"}), 400

#     new_track = TrackDb(**data)
#     db.session.add(new_track)
#     db.session.commit()
    
#     return jsonify({"message": "Track created", "id": new_track.id}), 201

# # -------------------- PUT update existing track --------------------
# @app.route('/track', methods=['PUT'])
# def update_track():
#     data = request.json
#     if not data or "id" not in data:
#         return jsonify({"error": "Invalid data"}), 400

#     track = TrackDb.query.get(data["id"])
#     if not track:
#         return jsonify({"error": "Track not found"}), 404

#     for key, value in data.items():
#         if hasattr(track, key):
#             setattr(track, key, value)
    
#     db.session.commit()
#     return jsonify({"message": "Track updated"}), 200


# -------------------- Start Flask server --------------------
if __name__ == '__main__':
    app.run(debug=True)
