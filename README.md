# NUS NCIS INNOVATION CHALLENGE 

Team TAB

## Getting started

## Project Structure
TransportGPT/
│
├── data/                        # Contains data files or datasets as well as associated pipelines
│   ├── EstTravelTimes.json      # File containing travel times
│   ├── EstTravelTimes.py        # Python pipeline of travel times
│   ├── Traffic-Imagesv/         # Directories for traffic images
│   │   ├── Traffic-Imagesv/     # File containing live traffic images
│   │   └── TrafficFlow.json     # Pipeline for traffic images
│   ├── TrafficFlow.json         # File containing traffic flow
│   └── TrafficFlow.py           # Python pipeline of traffic flow 
│
├── resources/                   # Additional resources
│   ├── __init__.py              # Python initialization file
│   ├── EstTravelTim.py          # Python script related to travel times
│   ├── geocoding.py             # Python script for geocoding
│   ├── image.py                 # Python script for image processing
│   ├── trafficFlow.py           # Python script related to traffic flow
│   ├── __init__.py              # Python initialization file
│   ├── cfg.xml                  # Configuration file (XML)
│   ├── coco.names               # File containing object names
│   ├── yolov3.cfg               # Configuration file for YOLOv3
│   ├── __init__.py              # Python initialization file
│   └── vision.py                # Python script related to vision
│
├── model/                       # Contains models
│   ├── __init__.py              # Python initialization file
│
├── main.py                      # Main entry point or script
│
├── .gitignore                   # Git ignore file
├── docker-compose.yml           # Docker Compose file
└── DockerFile                   # Dockerfile for containerization