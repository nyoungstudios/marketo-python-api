# Marketo Python REST API
I worked a lot with the Marketo REST APIs in Python over the past 2 years. So, here is my code that I wrote to make those API requests easier.

## Usage
In order to use it, you need to get your Client Id, Client Secret, and the base part of the url endpoint (the format is 3 numbers, a dash, 3 letters, a dash, 3 numbers). And then store these in the environment variables `marketoClientID`, `marketoClientSecret`, and `baseCode` respectively.\
Alternatively, you can use the [python-dotenv library](https://pypi.org/project/python-dotenv/) to import the environment variables from a `.env` file.

If you need any help finding these, see the documentation here: https://developers.marketo.com/rest-api/authentication/

## Features
* CRUD on leads
* Describe lead
* CRUD on custom objects
* List custom objects
* Bulk Extract

## Notes
Bulk Import is not complete yet. Instead, I ended up passing 300 records (which is the max the API supports) at a time through the update on leads endpoint.

## Dependencies
I am using the [Requests library](https://requests.readthedocs.io/en/master/) for making the HTTP requests.
