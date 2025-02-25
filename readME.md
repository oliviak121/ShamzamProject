# Shamzam - Audio Identification Project 

## Project Descrition
Shamzam is a music identification service consisting of three microservices: Catalogue Management Service, Music Identification Service, and Shamzam Service; using Flask and SQLite to perform user and admin tasks. 

Capabilities:
- Add a music track to the catalogue, so that a user can listen to it.
- Remove a music track from the catalogue, so that a user cannot listen to it.
- List the names of the music tracks in the catalogue, to know what it contains.
- Convert a music fragment to a music track in the catalogue, to listen to it.

## Table of Contents
- [Directory Structure](#directory-structure)
- [Microservice Overview and API Endpoints](#overview-and-endpoints)
- [Setup and Usage](#installation-and-usage)
- [Testing](#testing)

## Directory Structure


## Microservice Ovewview and API Endpoints
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

5. Run the service flask app
    ```terminal
    python app.py
    ```

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

To run all the tests you can type the following command in the terminal:
```terminal
python -m unittest discover tests
```