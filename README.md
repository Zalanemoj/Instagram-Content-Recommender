# 📸 Instagram Content Recommender & Analytics

![Banner](Images/Logo-Dashboard.jpg)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Keras-orange?logo=tensorflow&logoColor=white)
![Tableau](https://img.shields.io/badge/Tableau-Dashboard-blue?logo=tableau&logoColor=white)
![XGBoost](https://img.shields.io/badge/ML-XGBoost-green)
![Streamlit](https://img.shields.io/badge/App-Streamlit-red?logo=streamlit&logoColor=white)

## 📖 Project Overview

The **Instagram Content Recommender** is an end-to-end data science project designed to help content creators optimize their strategy. By analyzing historical Instagram data, this project provides actionable insights via a Tableau dashboard and utilizes Machine Learning models (ANN & XGBoost) to predict the reach and engagement (Likes) of future posts based on content type, timing, and category.

Additionally, the application integrates **Google Gemini AI** to provide qualitative strategy advice based on the model's numerical predictions.

Based on the analysis of the repository files, here is a detailed description of the project that you can use in your `README.md` file (specifically in the "About" or "Project Overview" section).

### **Project Description**

The **Instagram Content Recommender** is an end-to-end data analytics and machine learning solution designed to help content creators optimize their social media strategy. This project bridges the gap between raw data and actionable insights by analyzing historical engagement metrics (Likes, Reach, Comments) to predict the success of future posts.

The system operates through a complete data pipeline:
1.  **Data Processing:** Raw Instagram analytics data is processed using **SQL** and **Python** to handle duplicates, clean features, and aggregate performance metrics by category and media type.
2.  **Visualization:** A **Tableau Dashboard** provides a visual narrative of month-over-month growth and category comparisons, allowing users to identify trends in "Reels" vs. "Static" content performance.
3.  **Predictive Modeling:** The project utilizes advanced Machine Learning algorithms, specifically **XGBoost** and **Artificial Neural Networks (ANN)**, to forecast engagement rates based on input features like hashtags, caption length, and posting time.
4.  **AI-Powered Application:** A **Streamlit** web application serves as the user interface. It integrates **Google Gemini AI** to interpret the model's numerical predictions and generate qualitative, text-based strategy reports, offering users specific advice on how to improve their content's reach.

This repository serves as a comprehensive guide to building a predictive analytics tool, covering data engineering, model training, and application deployment.


## 📂 Repository Structure

```text
├── App.py                       # Streamlit Application (AI Strategist & Predictor)
├── Images/                      # Project assets, diagrams, and logos
├── Models/                      # Saved ML models (.h5, .pkl) and Encoders
├── Scripts-ML/                  # Jupyter Notebooks for EDA, Training, and Prediction
├── SQL-Scripts/                 # SQL scripts for data profiling and insights
├── Tableau-Dashboard/           # Tableau workbooks and analytics screenshots
├── Splitted-Data/               # Train/Test CSV datasets
├── instagram-analytics-dataset/ # Raw dataset
└── requirements.txt             # Python dependencies
