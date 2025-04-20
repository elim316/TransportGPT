# TransportGPT – Generative AI for Traffic Management  
*Developed for the NUS NCIS Innovation Challenge 2024*  
![Innovation Challenge](https://img.shields.io/badge/Innovation-Challenge-orange)
![Python](https://img.shields.io/badge/Built%20With-Python-blue)
![LangChain](https://img.shields.io/badge/AI%20Framework-LangChain-green)
![Vision Model](https://img.shields.io/badge/CV-YOLOv3-red)

**Team TAB** – Elias Lim & collaborators

TransportGPT is an AI-powered prototype designed to enhance traffic flow insights and communication through the use of **Generative AI**. It integrates real-time traffic data, computer vision, and predictive modeling to generate natural-language traffic summaries, identify congestion patterns, and assist motorists through smart navigation suggestions.

---

## Project Overview

- Analyse historical and live traffic data from the Land Transport Authority (LTA)
- Use computer vision (YOLOv3) on real-time traffic camera images
- Predict near-term and long-term traffic conditions
- Generate human-readable traffic summaries via a Generative AI model
- Provide real-time routing suggestions to improve driving efficiency

---

## How It Works

### 1. Data Collection & Ingestion  
Real-time JSON datasets (travel time, traffic flow, camera feeds) are parsed and processed.

### 2. Vision-Based Traffic Analysis  
YOLOv3 is used to detect vehicles from traffic camera images and assess road congestion.

### 3. Traffic Pattern Analysis  
Historical and real-time data are analyzed to identify congestion trends and road anomalies.

### 4. LLM Integration  
Cleaned and structured traffic data is passed through a Large Language Model (e.g., GPT) to generate natural-language summaries and advisories.

### 5. Output Delivery  
Results can be displayed via CLI or an optional Streamlit interface.

---

## Tech Stack

- Python  
- OpenAI / LangChain  
- YOLOv3 (Computer Vision)  
- LTA Real-Time Traffic Data (mocked/tested)  
- JSON, OpenCV, NumPy  
- Docker (optional deployment)  
- Streamlit (optional interface)

---


## Getting Started

Clone the repo and install dependencies:

```bash
git clone https://github.com/elim316/TransportGPT.git
cd TransportGPT
pip install -r requirements.txt

## Getting started
run the command ```pip install -r requirements.txt```
```

## Project Structure
```
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
```

## Project Materials

### Final Report  
Comprehensive documentation of our design, model pipeline, and evaluation.  
[View the TransportGPT Project Report (PDF)](https://github.com/elim316/TransportGPT/blob/main/TransportGPT_Report.pdf)

### Presentation Slides  
Slides presented during the final round of the Innovation Challenge.  
[View the Presentation Slides (PDF)](https://github.com/elim316/TransportGPT/blob/main/TransportGPT_Presentation.pdf)
