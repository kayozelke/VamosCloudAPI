
import sqlalchemy as db
from sqlalchemy.orm import declarative_base

db_base = declarative_base()

# tables
class TrackDb(db_base):
    __tablename__ = 'tracks'
    # data is like below
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    streams = db.Column(db.BigInteger, nullable=False)
    daily_streams = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    peak_position = db.Column(db.Integer, nullable=False)
    weeks_on_chart = db.Column(db.Integer, nullable=False)
    lyrics_sentiment = db.Column(db.Float, nullable=False)
    tiktok_virality = db.Column(db.Integer, nullable=False)
    danceability = db.Column(db.Float, nullable=False)
    acousticness = db.Column(db.Float, nullable=False)
    energy = db.Column(db.Float, nullable=False)

def get_engine(username : str, password : str, host : str, port : int, database : str):
    return db.create_engine(
        url = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
    )
    
def get_engine_from_config(config: dict):
    return get_engine(
        username = config['DATABASE']['username'],
        password = config['DATABASE']['password'],
        host     = config['DATABASE']['host'],
        port     = config['DATABASE']['port'],
        database = config['DATABASE']['database']
    )
    
def create_tables(engine, db_base = db_base):
    db_base.metadata.create_all(engine)   
    print("Tables created.")
    
def check_and_create_tables(engine):
    inspector = db.inspect(engine)
    if 'tracks' not in inspector.get_table_names():
        create_tables(engine)
        
        
def get_tracks(engine):
    Session = db.orm.sessionmaker(bind=engine)
    session = Session()
    tracks = session.query(TrackDb).all()
    session.close()
    
    result = []
    for track in tracks:
        result.append({
            'id': track.id,
            'song': track.song,
            'artist': track.artist,
            'streams': track.streams,
            'daily_streams': track.daily_streams,
            'genre': track.genre,
            'release_year': track.release_year,
            'peak_position': track.peak_position,
            'weeks_on_chart': track.weeks_on_chart,
            'lyrics_sentiment': track.lyrics_sentiment,
            'tiktok_virality': track.tiktok_virality,
            'danceability': track.danceability,
            'acousticness': track.acousticness,
            'energy': track.energy
        })
    return result

    
    