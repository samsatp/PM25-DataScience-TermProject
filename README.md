# pm25datasci-project
This project is a part of *2110446 Data Science and Data Engineering class, Chulalongkorn University.* 

## Background
Over the past few years...
We are given these dataset:
- Wind data: wind direction, wind speed
- Temperature data
- Fire hotspot data
In this project, we will be using the information to predict the level of PM2.5 of the next 72 hours.

## Project structure
- Folders
    - `Models` : Contain all the model we built in `.h5` format.
    - `Data` : The preprocessed data, ready to be fed to the model.
    - `Extracted` : The raw data extracted from the raw files.
    - `Predictions` : The submission files.
- Files
    - `1.proj_init.ipynb` : extract data from raw files and join the relevant data together.
    - `2.pivot.ipynb` : prepare data to visualize in Tableau.
    - `3.fillna.ipynb` : handle the missing data.
    - `4.Fire.ipynb` : prepare the fire data*
    - `5.model_playground.ipynb` : doing model experiment
    - `6.evaluation.ipynb` : evaluating model with Test data
    - `packages.txt` : packages and dependencies used in this project
    - `util.py` : keep the utility functions
