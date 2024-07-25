# Map Application

This repository contains a simple map application built with folium and a backend API to process GeoJSON polygon file . The application allows users to draw polygons on a map and fetch population data for the selected area.



## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Folium
- Bootstrap 5

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/map-application.git
    cd map-application
    ```

2. Install the required Python packages:
    ```bash
    pip install flask
    ```

### Running the Application

1. Start the Flask backend:
    ```bash
    python app.py
    ```

## File Structure

- `app.py`: The Flask backend application.
- `index.html`: The frontend application containing the map and drawing tools.

## Usage

- Open a web browser and go to `http://127.0.0.1:5000` to access the map application.
- Use the drawing tools to draw a polygon on the map.
- Click the "Export GeoJSON" button to send the drawn polygon data to the backend and fetch population data.

##Example
![WhatsApp Image 2024-07-25 at 20 47 07_22e5e533](https://github.com/user-attachments/assets/38d11ae3-f346-4183-8753-e6d69e1111aa)


## Acknowledgments

- [Leaflet.js](https://leafletjs.com/)
- [Leaflet.draw](https://leaflet.github.io/Leaflet.draw/)
- [Kontur](https://www.kontur.io/portfolio/population-dataset/)
