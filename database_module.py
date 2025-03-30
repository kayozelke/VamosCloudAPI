import sqlalchemy as db
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy

db_sqlalchemy = SQLAlchemy()

# tables
class TrackDb(db_sqlalchemy.Model):
    __tablename__ = 'tracks'
    
    id = db_sqlalchemy.Column(db.Integer, primary_key=True, autoincrement=True)
    song = db_sqlalchemy.Column(db_sqlalchemy.String(255), nullable=False)
    artist = db_sqlalchemy.Column(db_sqlalchemy.String(255), nullable=False)
    streams = db_sqlalchemy.Column(db_sqlalchemy.BigInteger, nullable=False)
    daily_streams = db_sqlalchemy.Column(db_sqlalchemy.Integer, nullable=False)
    genre = db_sqlalchemy.Column(db_sqlalchemy.String(100), nullable=False)
    release_year = db_sqlalchemy.Column(db_sqlalchemy.Integer, nullable=False)
    peak_position = db_sqlalchemy.Column(db_sqlalchemy.Integer, nullable=False)
    weeks_on_chart = db_sqlalchemy.Column(db_sqlalchemy.Integer, nullable=False)
    lyrics_sentiment = db_sqlalchemy.Column(db_sqlalchemy.Float, nullable=False)
    tiktok_virality = db_sqlalchemy.Column(db_sqlalchemy.Integer, nullable=False)
    danceability = db_sqlalchemy.Column(db_sqlalchemy.Float, nullable=False)
    acousticness = db_sqlalchemy.Column(db_sqlalchemy.Float, nullable=False)
    energy = db_sqlalchemy.Column(db_sqlalchemy.Float, nullable=False)


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{app.config['DATABASE']['username']}:{app.config['DATABASE']['password']}@{app.config['DATABASE']['host']}:{app.config['DATABASE']['port']}/{app.config['DATABASE']['database']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db_sqlalchemy.init_app(app)

    with app.app_context():
        db_sqlalchemy.create_all()

    return db_sqlalchemy



# def create_tables(engine, db_base = db_base):
#     db_base.metadata.create_all(engine)   
#     print("Tables created.")
    
# def check_and_create_tables(engine):
#     inspector = db.inspect(engine)
#     if 'tracks' not in inspector.get_table_names():
#         create_tables(engine)
        
        
# def get_tracks(engine):
#     Session = db.orm.sessionmaker(bind=engine)
#     session = Session()
#     tracks = session.query(TrackDb).all()
#     session.close()
    
#     result = []
#     for track in tracks:
#         result.append({
#             'id': track.id,
#             'song': track.song,
#             'artist': track.artist,
#             'streams': track.streams,
#             'daily_streams': track.daily_streams,
#             'genre': track.genre,
#             'release_year': track.release_year,
#             'peak_position': track.peak_position,
#             'weeks_on_chart': track.weeks_on_chart,
#             'lyrics_sentiment': track.lyrics_sentiment,
#             'tiktok_virality': track.tiktok_virality,
#             'danceability': track.danceability,
#             'acousticness': track.acousticness,
#             'energy': track.energy
#         })
#     return result

    
    