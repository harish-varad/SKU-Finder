# SKU Streamer

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/harish-varad/SKU-Finder)

SKU Streamer is an API developed in Python on Flask Framework. 
There are 3 end points in this api and complete guide to run it as a standalone .py or with docker container, is given below.

**This Tutorial has two parts for Host (to start web service) and Client (to make rest calls to the web service). Please follow accordingly.**

# Table of Contents
- **[Host](#Host)**
- **[Client](#Client)**
- **[Swagger-Documentation](#Swagger-Documentation)**
- **[API-Documentation](#API-Documentation)**

# Host 
**(To start web-service)**
You have two methods to run the application,

1. [Run with Docker](#Run-with-Docker)
2. [Run with Native Python](#Running-with-Native-Python)

### Run-with-Docker

1. Pull the docker image `harishvaradarajan/sku_streamer` from docker hub
    ```sh
    docker pull harishvaradarajan/sku_streamer
    ```
    
2. Start the docker container (You may also directly run this command without running the above command)
    ```sh
    docker run -dp 9000:9000 harishvaradarajan/sku_streamer
    ```


### Running-with-Native-Python

Please follow the below steps to run on your favourite editor 
1. Clone this git repo
    ```sh
        git clone https://github.com/harish-varad/SKU-Finder.git
    ```
    
2. Install the Python Libraries: Flask, Pandas and Flasgger. 
    You may install it using requirements.txt, which is included in the repo.
    
    From the cloned directory, hit the below syntax in command line
     ```sh
        pip3 install -r requirements.txt
    ```
3. Run `app.py`
4. The API service starts on your `localhost` at port `9000`
5. You can access the API documentation on URL `http://localhost:9000/apidocs/`



# Client 
**(To access the data through API calls)**

### API Usage
###### Endpoint 1
> /transaction/<transaction_id>

###### Endpoint 2
> /transaction-summary-bySKU/<last_n_days>

###### Endpoint 3
> /transaction-summary-bycategory/<last_n_days>

# Swagger-Documentation
#
**The swagger documentation is created to aid the usage of endpoints.**
#
**Once you start the service with any of the above methods, open your browser and hit the below URL to try the APIs**
#
***http://localhost:9000/apidocs/***
#
#
# API-Documentation

**This is a web service that has 3 endpoints, with which you will be able to get the SKU data and other related details**

**[Enpoint 1: GET]** `"/transaction/<transaction_id>"  `
With this, you can get the  below details based on the Transaction ID that you provide with the url.
- transaction_id
- sku_name
- sku_price
- transaction_datetime
###### EXAMPLE :
#
> Getting transaction details for the transaction_id : ***1***
#
> Request URL: `http://localhost:9000/transaction-summary-bySKU/1`
#
###### Expected Response :
#
```sh
{
  "sku_name": "S1",
  "sku_price": "63.8",
  "transaction_datetime": "26/01/2022",
  "transaction_id": "1"
}
```
#
#
**[Enpoint 2: GET]** `/transaction-summary-bySKU/<last_n_days>` 
With this, you can filter out the data for last "n" days and get the total price in that "n" time period for  ***SKU Name***.

###### EXAMPLE :
#
> Getting total price for last ***10*** days.
#
> Request URL: `http://localhost:9000/transaction-summary-bySKU/10`
#
###### Expected Response :
#
```sh
{
  "summary": [
    {
      "sku_name": "S3",
      "total_amount": 634
    },
    {
      "sku_name": "S1",
      "total_amount": 4320.05
    }
  ]
}
```
#
#
**[Enpoint 3: GET]** `/transaction-summary-bycategory/10` 
With this, you can filter out the data for last "n" days and get the total price in that "n" time period for  ***SKU Category***.

###### EXAMPLE :
#
> Getting total price for last ***10*** days.
#
>  Request URL: `http://localhost:9000/transaction-summary-bycategory/10`
#
###### Expected Response :
#
```sh
{
  "summary": [
    {
      "sku_category": "C3",
      "total_amount": 634
    },
    {
      "sku_category": "C1",
      "total_amount": 4320.05
    }
  ]
}
```


#### -

## License
MIT
