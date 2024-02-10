#  Phonepe Pulse Data Visualization

Introduction

  The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics. The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.

Table of Contents

1.	Key Technologies
2.	Installation
3.	Usage
4.	Workflow

Key Technologies

  • Python scripting 
  • plotly 
  • Streamlit 
  • Postgresql
  • Pandas
  

Installation

  To run this project, you will need to install the following packages
    pip install streamlit
    pip install psycopg2
    pip install streamlit_option_menu
    pip install pandas
    pip install plotly
   

Usage

To use this project, kindly follow the following steps:

    1.	Clone the repository: git clone https://github.com/Theressac/Streamlit-app-youtube-data
    2.	Install the required packages
    3.  Run "python phonepe.py" to manipulate the data and create the CSV files
    3.	Run the Streamlit app: streamlit visualization.py
    4.	Access the app in your browser at http://localhost:8501

Workflow

    Data Retrieval and Transformation:
      Fetched PhonePe Pulse data from PhonePe's Repo via Git Clone.
      Transformed JSON data to Pandas DataFrames.
      Converted data to CSV format and downloaded to the local environment.

    SQL Integration:
      Created six tables in SQL to store CSV data.
      Transferred CSV data to SQL tables using Python with PostgreSQL connection.

    Streamlit Application:
      Utilized Streamlit for the front-end interface.
      Implemented dynamic visualizations using Plotly, including Choropleth maps.
      Enabled user interaction to select options, triggering back-end queries to fetch and process data from SQL.
      Presented visual representations in the Streamlit interface based on user selections.

    User Interaction and Query Processing:
        Enabled user selection options in the Streamlit interface.
        Executed back-end queries based on user selections to fetch and process data from SQL.

    Visualization:
        Presented visual insights in real-time within the Streamlit interface.
        Utilized Choropleth maps and other Plotly visualizations for effective data representation.


Author

@Theressac

