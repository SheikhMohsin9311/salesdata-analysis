# 📊 Sales Data Analysis Dashboard

An interactive Data Science application to analyze and forecast sales performance. Built with **Python**, **Streamlit**, and **Plotly**.

![Sales Dashboard](sales_dashboard.png)

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Technologies](#technologies)
- [Educational Purpose](#educational-purpose)

## 📖 Overview
This project transforms raw sales data into actionable insights. It serves as a comprehensive example of a modern data science workflow, moving from data cleaning and exploratory analysis to interactive visualization and machine learning-based forecasting.

## ✨ Key Features

### 1. Interactive Dashboard
-   **Dynamic Filtering**: Filter data by Year, Country, and Product Category.
-   **Real-time KPIs**: View Total Revenue, Profit, Order Count, and Average Unit Price instantly.
-   **Interactive Charts**: Zoom, pan, and hover over charts for detailed data points.

### 2. Advanced Analytics
-   **Revenue Analysis**: Breakdown of revenue by Category and Country.
-   **Profitability Analysis**: Identification of the top 10 most profitable sub-categories.
-   **Seasonal Trends**: Analysis of monthly sales trends across different years to identify seasonality.

### 3. Sales Forecasting
-   **Time Series Modeling**: Uses **Exponential Smoothing (Holt-Winters)** to predict future sales.
-   **Visual Forecast**: Overlays historical data with 6-month sales predictions.

## 📂 Project Structure
The project follows a modular architecture for scalability and maintainability.

```text
sales-analysis/
├── app.py                  # Main entry point for the Streamlit dashboard
├── analysis.py             # (Legacy) Standalone script for static analysis
├── requirements.txt        # Project dependencies
├── sales_data.csv          # Dataset file
├── sales_dashboard.png     # Static dashboard export
├── src/                    # Source code package
│   ├── __init__.py
│   ├── loader.py           # Data loading and preprocessing logic
│   ├── analysis.py         # Statistical analysis and transformation functions
│   └── forecasting.py      # Machine Learning forecasting module
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
Ensure the `sales_data.csv` file is present in the root directory. If not, it will be downloaded automatically by the legacy script or needs to be placed manually.

## 🚀 Usage

### Run the Dashboard
To launch the interactive web application:
```bash
streamlit run app.py
```
This will open the dashboard in your default web browser (usually at `http://localhost:8501`).

### Run Static Analysis
To generate a static PNG report (legacy mode):
```bash
python analysis.py
```

## 🛠️ Technologies
-   **Language**: Python 3.13
-   **Web Framework**: Streamlit
-   **Data Manipulation**: Pandas
-   **Visualization**: Plotly, Matplotlib
-   **Forecasting**: statsmodels

## 🎓 Educational Purpose
> [!IMPORTANT]
> **This project was created for educational purposes.**
> It demonstrates:
> *   Building modular Python applications.
> *   Creating interactive data dashboards.
> *   Implementing basic time-series forecasting.
> *   Structuring a data science project professionally.
