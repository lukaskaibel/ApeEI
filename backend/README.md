# ApeEI Backend

[![Flask](https://img.shields.io/badge/Framework-Flask-blue)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Language-Python-blueviolet)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The backend of ApeEI is a Flask server. It uses an AI model to facilitate various features such as reflection analysis, event detection, and Wikipedia entry suggestions.

## Directory Structure

- `/backend`
  - `/features`: This directory contains the primary features of the assistant like reflection analysis (assistant_pt.py), event detection (event_pt.py), and Wikipedia entry suggestions (wiki_pt.py).
  - `/utils`: This directory holds utility functions used across the application.
  - `main.py`: This is the main server file that contains the Flask application and the endpoints.
  - `routes.py`: This file holds the Flask routes for the API.

## Getting Started

### Prerequisites

- Conda (Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution))

### Installation

1. Clone the repository:

```bash
git clone https://github.com/lukaskaibel/ApeEI.git
cd backend
```

2. Create Conda environment from environment.yml:

```bash
conda env create -f environment.yml
```

### API Keys Setup

In order for the application to function correctly, you will need to set up some API keys. Make sure `config.json` and `credentials.json` are included in the projects `.gitignore` file, as including them in source control would leak private key information.

#### OpenAI API Key

1. Go to [OpenAI's website](https://www.openai.com/), create an account or log in.
2. Once logged in, navigate to the API section to create a new API key.
3. After you've obtained your API key, create a file named `config.json` in the root directory of the backend application.
4. Inside this file, create a JSON object that looks like the following (replace `<Your OpenAI Key>` with your actual OpenAI key):

```json
{
  "openai-key": "<Your OpenAI Key>"
}
```

#### Google Calendar API

1. Navigate to the [Google Cloud Platform Console](https://console.cloud.google.com/).
2. Create a new project, or select an existing project.
3. In the sidebar on the left, select APIs & Services -> Library.
4. Search for 'Google Calendar API', select it, and enable the API for your project.
5. Now navigate to APIs & Services -> Credentials in the left sidebar, and create new credentials.
6. Once you've created your credentials, download them as a JSON file.
7. Rename this file to `credentials.json` and place it in the root directory of the backend application.

### Usage

Follow these steps to start the server:

1. Active the conda environment:

```bash
conda activate ape-ei
```

2. Start the server:

```bash
python main.py
```

The server should now be running on `localhost:5000`.

## API Endpoints

- `POST /api/chat`: This endpoint receives a user message as input and returns the assistant's response. If the message is analyzed as a reflection, it also returns a Wikipedia entry suggestion and an event if detected.

- `POST /api/create_event`: This endpoint receives event data and creates a Google Calendar event based on the provided information.
