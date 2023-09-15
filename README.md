# Car Price Prediction App

**Submitted by: Sunil Prajapati**

**Student ID: 124073**

The current version of the app is running at: [st124073.ml2023.cs.ait.ac.th](https://st124073.ml2023.cs.ait.ac.th)

### App Directory Structure

<pre>
app
├── <a href="https://github.com/scherbatsky-jr/car_price_prediction/blob/main/app/Dockerfile">Dockerfile</a>
├── <a href="https://github.com/scherbatsky-jr/car_price_prediction/blob/main/app/docker-compose.yml">docker-compose.yml</a>
├── <a href="https://github.com/scherbatsky-jr/car_price_prediction/blob/main/app/code">code</a>
│   └── <a href="https://github.com/scherbatsky-jr/car_price_prediction/blob/main/app/code/main.py">main.py</a>
│   ├── <a href="https://github.com/scherbatsky-jr/car_price_prediction/blob/main/app/code/car_price_prediction.ipynb">car_price_prediction.ipynb</a>
│   ├── <a href="https://github.com/scherbatsky-jr/car_price_prediction/blob/main/app/code/linear-regression.ipynb">linear-regression.ipynb (Assignment 2)</a>
│   ├── assets
│       └── home.css
├── <a href="https://github.com/scherbatsky-jr/car_price_prediction/blob/main/app/dataset">dataset</a>
│   └── cars.csv
└── <a href="https://github.com/scherbatsky-jr/car_price_prediction/blob/main/app/model">model</a>
    ├── scaler.pkl
    └── selling-price.model
</pre>


### Requirements
- Docker
- Python


### Running the app

Run the following command to run the dash app

```make run```

The app will run at address http://localhost:80

To stop the app, run the following command

```make stop```
