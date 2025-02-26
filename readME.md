# Shamzam - Audio Identification Project 

## Project Descrition
Shamzam is a music identification service consisting of three microservices: Catalogue Management Service, Music Identification Service, and Shamzam Service; using Flask REST API and SQLite to perform user and admin tasks. 

Capabilities:
- Administrator: Add a music track to the catalogue, so that a user can listen to it.
- Administrator: Remove a music track from the catalogue, so that a user cannot listen to it.
- Administrator: List the names of the music tracks in the catalogue, to know what it contains.
- User: Convert a music fragment to a music track in the catalogue, to listen to it.

## Table of Contents
- [Directory Structure](#directory-structure)
- [Microservice Overview and API Endpoints](#microservice-overview-and-api-endpoints)
  - [Catalogue Management Service](#catalogue-management-service)
  - [Music Identification Service](#music-identification-service)
  - [Shamzam Service](#shamzam-service)
- [Setup and Usage](#setup-and-usage)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Setting Up Each Microservice](#setting-up-each-microservice)
- [Testing](#testing)
  - [Setting up testing environment](#setting-up-testing-environment)
  - [Running Tests](#running-tests)

## Directory Structure
```tree
ShamzamProject/
├── src/
│   ├── catalogue_management_service/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── catalogue.db
│   │ 
│   ├── music_identification_service/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── requirements.txt
│   │ 
│   └── shamzam_service/
│       ├── __init__.py
│       ├── app.py
│       └── requirements.txt
│ 
├── tests/
│   ├── __init__.py
│   ├── test_helpers.py
│   ├── test_us1.py
│   ├── test_us2.py
│   ├── test_us3.py
│   ├── test_us4.py
│   └── requirements.txt
│
├── music/
│   ├── fragments/
│   │   └── [*Note: INSERT FRAGMENT .WAV FILES HERE*]
│   └── tracks/
│       └── [*Note: INSERT TRACK .WAV FILES HERE*]
│ 
├── playlist/
│   └── [*Note: WHERE THE FOUND TRACKS WILL BE OUTPUTTED FROM test_us4.py*]
│
├── .vscode/
│   └── launch.json
│
├── .gitignore
└── README.md
```


## Microservice Overview and API Endpoints
### Catalogue Managment Service 
- **URL**: `http://localhost:5002`
- **API Endpoints**:
  - `POST /add`: Add a new track to the catalogue.
  - `DELETE /delete`: Delete a track from the catalogue.
  - `GET /tracks`: List all tracks in the catalogue.
  - `GET /search`: Search for a track in the catalogue.

## Music Identification Service
- **URL**: `http://localhost:5001`
- **API Endpoints**:
  - `POST /identify`: Identify a music fragment.

### Shamzam Service
- **URL**: `http://localhost:5000`
- **API Endpoints**:
  - `POST /catalogue/add`: Add a new track to the catalogue.
  - `DELETE /catalogue/delete`: Delete a track from the catalogue.
  - `GET /catalogue/list`: List all tracks in the catalogue.
  - `GET /catalogue/search`: Search for a track in the catalogue.
  - `POST /music/identify`: Identify a music fragment.


## Setup and Usage
### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Clone the Repositiory
```bash
git clone https://github.com/oliviak121/ShamzamProject.git
cd ShamzamProject
```

### Setting Up Each Microservice
1. Open a new terminal for each service and cd into the service
    ```terminal
    cd src/shamzam_service
    ```

2. Set up a virtual environement in each service
    ```terminal
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependenices for each service
    ```terminal
    pip install -r requirements.txt
    ```

4. For music identification service only: export your Audd.io API key (should be saved in an env.txt file in the service)
    ```terminal
    export AUDD_API_KEY='your key'
    ```

5. Run the service flask app
    ```terminal
    python app.py
    ```

## Music
### The Music Folder
The project assumes .wav files of songs are present in the music folder in the main directory, and uses these to pull from for testing. The fragment folder should contain short clips of songs around 4 seconds long. The track folder should contain longer clips songs to simulate the whole song (but is actually around 8 seconds long in this instance). 

### The Playlist Folder
The playlist folder is where the resultant full length .wav sond files will be outputted to after running the test_us4 happy path test. This takes a fragment and returns the corresponding full track with the artist and song title as the name of the .wav file. 

## Testing
### Setting up testing enviornment
Requirements are also needed to run the tests, so to start open a virtual environment in the main ShamzamProject directory
```terminal
python3 -m venv venv
source venv/bin/activate 
```

Then you can install the requirments.txt file
```terminal
pip install -r requirements.txt
```

### Running the tests
To run all the tests you can type the following command in the terminal:
```terminal
python -m unittest discover tests
```
