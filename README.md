# ClutterFree


## Project Overview

ClutterFree is a user-friendly application designed to help organize and manage files efficiently. The project aims to reduce digital clutter by providing an intuitive interface for file management and generating reports on file usage or structure. This tool is built with Python and offers a web interface for easy interaction.


## Features

- Organized file management through a web interface.
- Detailed usage reports generated automatically.
- Simple, clean design for ease of use.
- Docker support for easy containerized deployment.


## Project Structure

ClutterFree/
├── app.py  # Main application code
├── requirements.txt # Project dependencies
├── Dockerfile # Docker setup for containerization
├── report.log # Runtime generated report logs
├── static/
│ └── clutterfree_icon.png # Project icon
└── templates/
├── index.html # Home page template
├── report.html # Report display template
└── help.html # Help/FAQ page template

## Installation

1. Clone the repository:
git clone <https://github.com/CactusAaron05/ClutterFree.git>
cd ClutterFree

2. (Optional) Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install required dependencies:
pip install -r requirements.txt


## Running the Application

### Locally

Run the application with:
python app.py

Open your browser and go to `http://localhost:5000` to access the ClutterFree interface.

### Using Docker

Build the Docker container:
docker build -t clutterfree .

Run the Docker container:
docker run -p 5000:5000 clutterfree

Now access the application at `http://localhost:5000`.


## Usage

- Use the homepage to upload and manage files.
- Generate detailed reports on file structure and usage.
- View help and FAQs under the Help page.
