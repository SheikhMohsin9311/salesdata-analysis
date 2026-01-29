# 🎬 Movie Analytics Dashboard

An interactive Data Science application to analyze trends in the IMDB 5000 movie dataset. Built with **Python**, **Streamlit**, and **Plotly**.

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Technologies](#technologies)
- [Educational Purpose](#educational-purpose)

## 📖 Overview
This project transforms raw IMDB movie metadata into actionable insights. It serves as a comprehensive example of a modern data science workflow, moving from data cleaning and exploratory analysis to interactive visualization.

## ✨ Key Features

### 1. Interactive Dashboard
-   **Dynamic Filtering**: Filter data by Release Year, Genre, and Director.
-   **Real-time KPIs**: View Total Movies, Total Box Office, Avg IMDB Score, and Avg Budget.
-   **Interactive Charts**: Zoom, pan, and hover over charts for detailed data points.

### 2. Advanced Analytics
-   **Director Analysis**: Top 10 highest-grossing directors.
-   **Genre Trends**: Average Imdb scores by genre.
-   **Financial Analysis**: Budget vs. Gross Revenue correlation (log scale).
-   **Temporal Trends**: Number of movies released per year.

## 📂 Project Structure
The project follows a modular architecture for scalability and maintainability.

```text
movie-analytics/
├── app.py                  # Main entry point for the Streamlit dashboard
├── requirements.txt        # Project dependencies
├── movie_metadata.csv      # Dataset file (IMDB 5000)
├── src/                    # Source code package
│   ├── __init__.py
│   ├── loader.py           # Data loading and preprocessing logic
│   └── analysis.py         # Statistical analysis and transformation functions
└── README.md               # Project documentation
```

## ⚙️ Setup & Installation

### Prerequisites
-   Python 3.8 or higher

### Step 1: Clone the Repository
If you haven't already, navigate to the project directory.

### Step 2: Create a Virtual Environment
It is best practice to run Python projects in a virtual environment.
```bash
# Create the environment
python3 -m venv venv

# Activate the environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download Data
Ensure the `movie_metadata.csv` file is present in the root directory.

## 🚀 Usage

### Run the Dashboard
To launch the interactive web application:
```bash
streamlit run app.py
```
This will open the dashboard in your default web browser (usually at `http://localhost:8501`).

## 🛠️ Technologies
-   **Language**: Python 3.13
-   **Web Framework**: Streamlit
-   **Data Manipulation**: Pandas
-   **Visualization**: Plotly
-   **Source Data**: IMDB 5000 Movie Dataset

## 🎓 Educational Purpose
> [!IMPORTANT]
> **This project was created for educational purposes.**
> It demonstrates:
> *   Building modular Python applications.
> *   Creating interactive data dashboards.
> *   Exploratory Data Analysis (EDA) on real-world datasets.
> *   Structuring a data science project professionally.
