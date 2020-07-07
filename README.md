# WobbleWatch
WobbleWatch is a prototype app designed to provide daily feedback to elderly users at risk of falling using data that could be collected from a smartphone. An active instance of the app can be found at http://wobblewatch.xyz. 

## Overview
Wobblewatch identifies "stumble" events and summarizes them on a daily basis as feedback for the user. These events are identified using either a CNN, a CNN-LSTM, or a more simple classifier. Jupyter was used for EDA and training, and the associated files can be found in `notebooks`.

## Training Data
WobbleWatch detects "stumble" events using data from the enhanced SisFall dataset that provides labeled time-series data regarding falls. Anyone can clone `wobblewatch` and download the training data to then utilize Jupyter notebooks found in `notebooks`. 

## Deployment Data
While it is not a proper way to validate the model, for the sake of showing the use case, I have utilized the Long-term Movement Monitoring database from Physionet. One can utilize the EDA notebook for this found in `notebooks`.

## References
Model design and training drew directly from work reported in *A novel hybrid deep neural network to predict pre-impact fall for older people based on wearable inertial sensors* by Xiaoqun Yu, Hai Qiu and Shuping Xiong published in Frontiers in Bioenginerring and Biotechnology, February, 2020 (https://doi.org/10.3389/fbioe.2020.00063).
