# Honeycomb Image Compressor 

## Overview  
The Honeycomb Image Compressor is an image compression tool inspired by nature's most efficient structure: the hexagon. Unlike traditional image compression methods that rely on square or rectangular grids, this technique applies a hexagonal tiling system to reduce file sizes while maintaining visual quality. This repository contains a Django-based implementation of the compressor.  

## Features  
- Hexagonal grid-based compression for smoother image quality  
- Reduced file sizes without significant quality loss  
- Django-powered web interface for uploading and compressing images  
- Supports multiple image formats  
- Efficient processing with OpenCV and NumPy  

## Installation  

### 1. Download the Repository  
- Click on the **Code** button at the top right of the GitHub page  
- Select **Download ZIP**  
- Extract the ZIP file to your preferred directory  

### 2. Navigate to the Project Directory  
Open a terminal or command prompt and move into the extracted folder:  
```
cd path/to/honeycomb_compressor-main
```
### 3. Create a Virtual Environment
```
python -m venv venv
```
```
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 4. Install Dependencies
```
pip install -r requirements.txt
```

### 5. Apply Migrations
```
python manage.py migrate
```

### 6. Run the Development Server
```
python manage.py runserver
```

## Usage
- Open your browser and go to http://127.0.0.1:8000/
- Upload an image through the web interface
- The system applies the hexagonal compression algorithm
- Download the compressed image





