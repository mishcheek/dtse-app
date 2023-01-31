## DTSE Full-Stack Developer assignment
>This project is an application built using the Flask and Dash. With Flask, the application is able to handle server-side functionality as it serves as a backend for the application and handles the prediction calculations using the pre-trained model, while Dash provides a user-friendly interface for visualizing and interacting with data. The application is designed to provide insights and information to users through an intuitive, easy-to-use interface.
### This repo contains two folders:
- **api** - REST API
- **app** - Dash Web App
### Running the app locally
1. Clone this repository. `git clone https://github.com/mishcheek/dtse.git`
2. Create a virtual environment in each directory: `python3 -m venv venv`
3. Activate the virtual environments: `source venv/bin/activate`
4. Install the required packages for each dir.: `pip install -r requirements.txt`
5. Run the respective python files using:  
- `python run.py` for the REST API
- `python app.py` for the Dash Web App
6. Access the app in your browser at `http://127.0.0.1:5002/`

### Running the app with Docker Compose
1. Clone this repository.
2. Navigate to the project directory: `cd dtse`
3. Build and start the Docker containers: `docker-compose up`
4. Access the app in your browser at `http://localhost:8081`

> In both cases, please make sure that the right port configuration is selected.
- `api/run.py`  - _lines 4-5_
- `app/app.py`  - _lines 17-18 and 292-293_