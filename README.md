# pm25datasci-project
This project is a part of *2110446 Data Science and Data Engineering class, Chulalongkorn University.* 

## Background
We are given these dataset:
- Wind data: wind direction, wind speed
- Temperature data
- Fire hotspot data

In this project, we will be using the information to make predictions. We will forecast at 00:00, 06:00, 12:00, 18:00 of everyday, each time we predict 72 hours in advance.

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
    - `4.Fire.ipynb` : prepare the fire data.
    - `5.model_playground.ipynb` : doing model experiment.
    - `6.evaluation.ipynb` : evaluating model with Test data.
    - `7.submission.ipynb` : prediction and make submission file.
    - `packages.txt` : packages and dependencies used in this project.
    - `util.py` : keep the utility functions.

## User guide
- Notebook `1, 2, 3, 4` do **preprocessing steps**
- Notebook `5` do **train models with train data**
- Notebook `6` do **evaluate models' performance with Test data**
- Notebook `7` do **making submission file**

- Notebook `1, 2, 3, 4` need functions defined in `util_get_data.py` and `util_handle_missing.py`
- Notebook `5, 6, 7` need function defined in `util_input_output_model.py`

## Results
- These models below have *720* timesteps as an input, each timestep contains 4 features(PM2.5, Wind direction, Wind Speed, Temp) and give RMSE = **10.56**
    - Bangkok : Models\Bangkok_run_2021_05_07-20_31_15_chckpoint.h5
    - Chanthaburi : Models\Chanthaburi_run_2021_05_08-12_58_02_chckpoint.h5
    - Songkhla : Models\Songkhla_run_2021_05_08-19_56_09_chckpoint.h5
    - Kanchanaburi : Models\Kanchanaburi_run_2021_05_08-15_58_45_chckpoint.h5
    - Khon Kaen : Models\Khon Kaen_run_2021_05_07-23_38_36_chckpoint.h5
    - Chiang Mai : Models\Chiang Mai_run_2021_05_08-07_41_04_chckpoint.h5
- These models below have *360* timesteps as an input, each timestep contains all features(PM2.5, Wind direction, Wind Speed, Temp, fire from 4 countries) and give RMSE = **10.96**
    - Bangkok : Models\Bangkok_run_2021_04_30-14_43_39.h5
    - Chanthaburi : Models\Chanthaburi_run_2021_04_26-10_42_58_final_26Apr1155.h5
    - Songkhla : Models\Songkhla_run_2021_04_25-22_41_22.h5
    - Kanchanaburi : Models\Kanchanaburi_run_2021_04_30-16_22_11.h5
    - Khon Kaen : Models\Khon Kaen_run_2021_04_27-16_20_46_kind_of_final.h5
    - Chiang Mai : Models\Chiang Mai_run_2021_04_30-15_37_01.h5


