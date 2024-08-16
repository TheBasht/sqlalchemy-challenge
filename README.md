# sqlalchemy-challenge

Surfs Up API
Welcome to the Surfs Up API! This Flask-based web service provides access to weather data collected from various weather stations. It's designed to help you analyze precipitation and temperature data for the past year and more.

Table of Contents
Features
Getting Started
API Endpoints
Data Sources
Contributing
License
Features
Precipitation Data: Retrieve precipitation data for the past year.
Station Information: Get a list of all weather stations and their names.
Temperature Observations: Access temperature data from the most active station over the last year.
Temperature Statistics: Obtain minimum, average, and maximum temperatures for a given date range.
Getting Started
To get started with the Surfs Up API, follow these steps:

Clone the Repository

sh
Copy code
git clone https://github.com/your-username/surfs-up-api.git
Navigate to the Project Directory

sh
Copy code
cd surfs-up-api
Install Dependencies

Ensure you have Python and pip installed, then install the required packages:

sh
Copy code
pip install -r requirements.txt
Run the Application

Start the Flask application:

sh
Copy code
python app.py
By default, the app will be available at http://127.0.0.1:5000/.

API Endpoints
Here are the available routes for the API:

Home Page

GET /
Description: Welcome message and list of available routes.
Precipitation Data

GET /api/v1.0/precipitation
Description: Returns precipitation data for the last 12 months in JSON format.
Station Information

GET /api/v1.0/stations
Description: Returns a list of all weather stations and their names.
Temperature Observations

GET /api/v1.0/tobs
Description: Returns temperature observations from the most active station for the past year.
Temperature Statistics by Start Date

GET /api/v1.0/<start>
Description: Returns the minimum, average, and maximum temperatures from a given start date to the present.
Temperature Statistics by Date Range

GET /api/v1.0/<start>/<end>
Description: Returns the minimum, average, and maximum temperatures for a specified date range.
Data Sources
The application uses data from a SQLite database located at Resources/hawaii.sqlite. This database contains weather measurement data and station information.
