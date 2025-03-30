# VamosCloud API - Music Track Database

This API was used as a practical example to pass a PUT course during the authors' studies. The current project provides an example RESTful API for managing a database of music tracks. It allows you to retrieve, add, and update track information.

## Features

* **Retrieve All Tracks:** Get a list of all tracks in the database.
* **Retrieve Track by Name:** Fetch details of a specific track by its song name.
* **Create New Track:** Add a new track to the database with its associated information.
* **Update Existing Track:** Modify the details of an existing track.

## Requirements

* **Python 3.x**
* **Flask:** A micro web framework for Python.
* **SQLAlchemy:** An SQL toolkit and Object-Relational Mapper (ORM).
* **MySQL/MariaDB:** A relational database management system.


## Database Setup (MySQL/MariaDB)

Ensure you have MySQL or MariaDB installed and running.

Create a database for the application (e.g., `vamoscloud_db`).

Update the `api_config.ini` file with your database credentials:

```ini
[DATABASE]
username = admin
password = admin
host = localhost
port = 3306
database = vamos_cloud_app
```

## API Methods

### GET `/objects`

**Description:** Retrieves all tracks from the database.

**Method:** GET

**Request:** None
**Response (JSON):**

```json
[
{
"id": 1,
"song": "Song Title 1",
"artist": "Artist Name 1",
"streams": 1000000,
"daily_streams": 10000,
"genre": "Pop",
"release_year": 2023,
"peak_position": 1,
"weeks_on_chart": 10,
"lyrics_sentiment": 0.8,
"tiktok_virality": 0.9,
"danceability": 0.7,
"acousticness": 0.2,
"energy": 0.8
},
// ... more tracks
]
```

### GET `/object`

**Description:** Retrieves a specific track by its song name.

**Method:** GET

**Request:**
Query Parameter: `name` (string, required) - The name of the song.

**Response (JSON):**

**Success (200 OK):**

```json
{
"id": 1,
"song": "Song Title 1",
"artist": "Artist Name 1",
"streams": 1000000,
"daily_streams": 10000,
"genre": "Pop",
"release_year": 2023,
"peak_position": 1,
"weeks_on_chart": 10,
"lyrics_sentiment": 0.8,
"tiktok_virality": 0.9,
"danceability": 0.7,
"acousticness": 0.2,
"energy": 0.8
}
```

**Not Found (404 Not Found):**

```json
{
"error": "Track not found"
}
```

**Bad Request (400 Bad Request):**

```json
{
"error": "Missing 'name' parameter"
}
```

### POST `/object`

**Description:** Creates a new track in the database.

**Method:** POST

**Request (JSON):**

```json
{
"song": "New Song",
"artist": "New Artist",
"streams": 500000,
"daily_streams": 5000,
"genre": "Rock",
"release_year": 2022,
"peak_position": 5,
"weeks_on_chart": 5,
"lyrics_sentiment": 0.7,
"tiktok_virality": 0.6,
"danceability": 0.5,
"acousticness": 0.4,
"energy": 0.7
}
```

**Response (JSON):**

**Created (201 Created):**

```json
{
"message": "Track created",
"id": 123 // id of created track
}
```

**Bad Request (400 Bad Request):**

```json
{
"error": "Invalid data"
}
```

### PUT `/object`

**Description:** Updates an existing track in the database.

**Method:** PUT

**Request (JSON):**

```json
{
"id": 1,
"streams": 1500000,
"daily_streams": 15000
}
```

**Response (JSON):**

**OK (200 OK):**

```json
{
"message": "Track updated"
}
```

**Not Found (404 Not Found):**

```json
{
"error": "Track not found"
}
```

**Bad Request (400 Bad Request):**

```json
{
"error": "Invalid data"
}
```

## Run Options

You can run the application using the following command:

```bash
python webserver.py
```

**Command-line arguments:**

- `-p` or `--port`: Specifies the port number to run the application on (default: 80).
- `-d` or `--debug`: Enables debug mode (default: disabled).

**Examples:**

**Run on port 5000 with debug mode:**

```bash
python webserver.py -p 5000 -d
```

**Run on port 8080 without debug mode:**

```bash
python webserver.py -p 8080
```

**Run on port 80 with debug mode:**

```bash
python webserver.py -d
```

**Run on port 80 without debug mode:**

```bash
python webserver.py
```

**Environment Variables:**

- `PORT`: If set, this environment variable will override the port specified by the `-p` or `--port` command-line argument.

## Project Structure

- `app.py`: Main Flask application file.
- `webserver.py`: Entry point to run the application.
- `src/`:
- `database_module.py`: Contains database initialization and model definitions.
- `config_module.py`: Contains configuration loading logic.
- `api_config.ini`: Configuration file for database settings.

## Notes

- The database tables are created automatically when the application starts.
- Error handling is implemented for common issues like missing parameters, invalid data, and not found resources.
- The code is designed to be easily extended with more API methods and features.
- The project is designed to be run on a server, so it is recommended to use a production-ready WSGI server like Gunicorn or uWSGI.
