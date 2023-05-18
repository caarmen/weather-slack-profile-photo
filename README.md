# Slack profile photo weather updater

This project updates your slack profile photo with a photo based on the weather.

The weather background images were generated by Bing.

## Configuration
You need to provide:
* A profile photo with a transparent background. By default, place it in `photo.png` in the project folder.
* Environment variables:
  - Copy the `.env.template` file to `.env`.
  - Edit the variables:
    - `WEATHERSTACK_API_ACCESS_KEY`: the api key for your account on weatherstack.com.
    - `SLACK_WORKSPACE`: the slack workspace where you want to change your profile photo
    - `SLACK_TOKEN`, `SLACK_COOKIE_D`: see below.
    - `LOCATION`: the location for the weather conditions that will be used to fill in the background in your profile photo.

### Retrieving the slack token and cookie values
* Log into slack in a browser on a computer.
* Enable developer tools in the browser, and open the network tab.
* Manually change your profile photo to any photo you want.
* Inspect the request in the developer tools network tab on the `/api/users.setPhoto` endpoint.
  - Copy the value of the `token` parameter into `SLACK_TOKEN` in your `.env` file.
  - For the `SLACK_COOKIE_D` env var, look at the `cookie` header, and extract the value of the `d=` part of the cookie.

### Optional parameters
* `PROFILE_PHOTO_PATH`: the path to your profile photo with the transparent background. Default value is `photo.png` in the project folder.
* `POLLING_INTERVAL_S`: The frequency in seconds to update the profile photo.

## Running the program
* Follow the setup described just above

### Locally
* Setup a python environment
* Run `python main.py`

### With Docker

Retrieve the docker image:
```
docker pull ghcr.io/caarmen/weather-slack-profile-photo:latest
```

Run the docker image. Change the host path to your photo if it's not `photo.png` in the root of the project:
```
docker run --detach -v `pwd`/.env:/app/.env -v `pwd`/photo.png:/app/photo.png ghcr.io/caarmen/weather-slack-profile-photo
```



