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
- [Microservices Overview and API Endpoints](#microservices-overview-and-api-endpoints)
  - [Shamzam Service](#shamzam-service)
  - [Catalogue Management Service](#catalogue-management-service)
  - [Music Identification Service](#music-identification-service)
- [Setup and Usage](#setup-and-usage)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Setting Up Each Microservice](#setting-up-each-microservice)
    - [Using Conda](#using-conda)
    - [Using Python venv](#using-python-venv)
- [Music](#music)
  - [The Music Folder](#the-music-folder)
  - [The Playlist Folder](#the-playlist-folder)
- [Testing](#testing)
  - [Setting up Testing Environment](#setting-up-testing-environment)
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
├── documents/
│   ├── AI Declaration.pdf
│   ├── ca enterprise .pdf
│   └── Shamzam Project Design.pdf
│
├── .vscode/
│   └── launch.json *NOTE: tool used in testing*
│
├── .gitignore
└── README.md
```


## Microservices Overview and API Endpoints
![Shamzam Architecture](documents/architecture.png)
### Shamzam Service
- **URL**: `http://localhost:5000`
- **Overview**: The Shamzam Service acts as the main entry point for users and administrators. It verifies that requests are in the correct format and forwards these to the appropriate microservices to perform various tasks related to music identification and catalogue management.
- **API Endpoints**:
  - `POST /catalogue/add`: Forwards request to Catalogue Management Service to add a new track to the catalogue.
  - `DELETE /catalogue/delete`: Forwards request to Catalogue Management Service to delete a track from the catalogue.
  - `GET /catalogue/list`: Forwards request to Catalogue Management Service to list all tracks in the catalogue.
  - `POST /catalogue/search`: Forwards request to Catalogue Management Service to search for a track in the catalogue.
  - `POST /music/identify`: Identifies a song fragment using the Music Identification Service.

### Catalogue Managment Service 
- **URL**: `http://localhost:5002`
- **Overview**: The Catalogue Management Service is responsible for managing the music tracks in the catalogue. It provides endpoints for administrators to add, delete, list, and search for tracks.
- **API Endpoints**:
  - `POST /add`: Add a new track to the catalogue.
  - `DELETE /delete`: Delete a track from the catalogue.
  - `GET /tracks`: List all tracks in the catalogue.
  - `POST /search`: Search for a track in the catalogue.
  - `DELETE /clear_database`: Clear all tracks from the database.

## Music Identification Service
- **URL**: `http://localhost:5001`
- **Overview**: The Music Identification Service is responsible for identifying music fragments. It uses the external API Audd.io to match the provided music fragment with a known track.
- **API Endpoints**:
  - `POST /identify`: Identify a music fragment.

See Shamzam Project Design file to see how the services interact and the full Rest API endpoint diagrams. 

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
Depending on what type of virtual environemnt you would like to use there are slight variations in how to set them up. Here are the instructions for using conda and python venv. 
#### Using conda 
  1. Open a new conda terminal for each service and cd into the service:
      ```sh
      cd src/shamzam_service
      ```
  2. Start a conda environement in each service:
      ```sh
      conda create -y --prefix ./.conda
      ```

  2. Activate the environment:
      ```sh
      conda activate ./.conda
      ```

  3. Install python:
      ```sh
      conda install python
      ```

  4. Install dependances for each environment:
      ```sh
      pip install -r requirements.txt
      ```

  5. For music identification service only: export your Audd.io API key (should be saved in an env.txt file in the service):
      ```sh
      set AUDD_API_KEY=your-key
      ```

  6. Run the service flask app:
      ```sh
      python app.py
      ```

  7. Deactivate the environemnt when done:
      ```sh
      deactivate
      ```


#### Using python venv
1. Open a new terminal for each service and cd into the service:
    ```sh
    cd src/shamzam_service
    ```

2. Set up a virtual environement in each service:
    ```sh
    python3 -m venv venv
    ```
    ```sh
    source venv/bin/activate
    ```

3. Install dependenices for each service:
    ```sh
    pip install -r requirements.txt
    ```

4. For music identification service only: export your Audd.io API key (should be saved in an env.txt file in the service):
    ```sh
    export AUDD_API_KEY='your-key'
    ```

5. Run the service flask app:
    ```sh
    python app.py
    ```

6. Deactivate the environemnt when done:
    ```sh
    deactivate
    ```

## Music
### The Music Folder
The project assumes .wav files of songs are present in the music folder in the main directory, and uses these to pull from for testing. The fragment folder should contain short clips of songs around 4 seconds long. The track folder should contain longer clips songs to simulate the whole song (but is actually around 8 seconds long in this instance). 

### The Playlist Folder
The playlist folder is where the resultant full length .wav sond files will be outputted to after running the test_us4 happy path test. This takes a fragment and returns the corresponding full track with the artist and song title as the name of the .wav file. 

## Testing
### Setting up testing enviornment
Requirements are also needed to run the tests, so to start open a virtual environment in the tests directory - using the steps above depending depending on your prefered environement.

Then you can install the requirments.txt file
```sh
pip install -r requirements.txt
```

### Running the tests
To run all the tests you can type the following command in the terminal:
```sh
python -m unittest discover 
```
Once completed deactivate the environment. 
