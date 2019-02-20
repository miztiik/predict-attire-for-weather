# Predict Attire for Weather
We will use the Dark Sky Weather API to get our weather data. Based on that we will make a prediction on what the attire should for a comfortable outdoor activity.

0. ## Get DarkSky API Key
    - Get your own [DarkSkey API Key](https://darksky.net/dev)

1. ## Setting up the environment
    - Get the application code
        ```sh
        yum -y install git
        git clone https://github.com/miztiik/predict-attire-for-weather.git
        ```
    - Update your API key

        In the file `src/configs/prod_config.json` update your `api key`

1. ## Run applicaion on linux Machine
    - Get the application code from GIT
        ```sh
        cd /var/predict-attire-for-weather
        gunicorn --bind 0.0.0.0:80 wsgi:application --access-logfile - --error-logfile - --capture-output --enable-stdio-inheritance
        ```

1. ## Run as Docker Image
    Assuming you have docker host ready, Run the [Setting up the environment](#setting-up-the-environment) instructions, and then execute the below,
    ```sh
    cd /var/predict-attire-for-weather
    ### Build the image
    docker build --tag="predict-attire-for-weather" .

    ### Run the Image   
    docker run -dti -p 80:80 --name attire_recommender predict-attire-for-weather
    ```

1. ## Test the app
    Access the linux server IP/Docker Host IP in your browser, you should be seeing something like this,
    ![Predict Attire for Weather](https://raw.githubusercontent.com/miztiik/predict-attire-for-weather/master/images/predict-attire-for-weather.png)

## Support
Please open a [GitHub issue](https://github.com/miztiik/predict-attire-for-weather/issues/new).

## Feeddack
Please open a [GitHub issue](https://github.com/miztiik/predict-attire-for-weather/issues/new). I do encourage you to contribute your changes and send me pull request.