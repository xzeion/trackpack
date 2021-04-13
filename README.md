#TrackPack

<!-- ABOUT THE PROJECT -->
## About The Project
A simple flask based application for shipping and tracking packages.

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites
* If on windows install git for windows and use the git terminal to run the build script
* Regardless of your OS, make sure you have docker and docker-compose installed
* Make sure your user is part of the docker group if you are running linux

### Installation

1. Clone the repo
   ```
   git clone https://git.gratton.us/brian/trackpack.git
   ```
2. Execute the build script
   ```
   sh build
   ```
* NOTE: the build script will also execute the testing suite



<!-- USAGE EXAMPLES -->
## Usage

This project allows for a few simple api calls that are documented below.

Loacations are stored as 5 decimal place lat and long coordinates
with the intent being to integrate google maps to aquire the actual addresses
```sh
# Create a new package in the system
curl -X POST \
  localhost:5000/api/v1/create \
  -d "shipper_name=Delivery Dans Custom T's" \
  -d "shipper_loc=45.12345,54.54321" \
  -d "reciever_name=Brian Gratton" \
  -d "reciever_loc=43.34212,-83.88431"
```
This should return a json object letting you know a new package was added
and the package id.
```json
{"Success": "New Package Added, PID: {PACKAGE_ID}"}
```

Next lets go ahead and add a checkpoint to the package
```sh
# Add a stop to an existing package
curl -X POST \
  localhost:5000/api/v1/progress \
  -d "id={PACKAGE_ID}" \
  -d "name=Bill and Ted's Delivery Service" \
  -d "location=20.12345,-43.54321"
```

This should return a json object with the details of the checkin
```json
{
  "arrival":"2021-04-13T04:35:05.333801",
  "check_in":"successful",
  "delivered":false,
  "location":"{LOCATION_ID}",
  "package_id":"{PACKAGE_ID}"
}
```

Great! Lets check our packages progress by pulling up its history
```sh
curl -X GET localhost:5000/api/v1/progress?id={PACKAGE_ID}
```
```json
{
  "package_id": "e1fd8a39-dc03-432e-b28f-9d5f155ca383",
  "package": {
    "updated_at": "2021-04-13T04:20:43.712088",
    "eta": null,
    "delivered": false,
    "created_at": "2021-04-13T04:20:43.712078"
  },
  "shipper": {
    "name": "Delivery Dan's Custom T's",
    "id": "e1e1c166-5338-43a1-8a54-b7b67ce12857", 
    "latitude": 45.12345,
    "longitude": 54.54321
  },
  "reciever": {
    "name": "Brian Gratton",
    "id": "602b9cc3-7147-413a-8c7b-f35f61081da2",
    "latitude": 43.34212,
    "longitude": -83.88431
  },
  "history": [
    {
      "arrival": "2021-04-13T04:20:43.727826",
      "location": "{LOCATION_ID}"
    },
    {
      "arrival": "2021-04-13T04:35:05.333801",
      "location": "{LOCATION_ID}"
    }
  ]
}
```

As you can see above we have our two points, the initial element that was created when the package was,
and the second we just created with the `/progress` endpoint.

We are going to add one more stop to our package so that the location matches the recievers location.
```sh
# Add a stop to an existing package
curl -X POST \
  localhost:5000/api/v1/progress \
  -d "id={PACKAGE_ID}" \
  -d "name=Destination" \
  -d "location=43.34212,-83.88431"
```

As you can see from the resulting json the packages `delivered` status is now set to true.
```json
{
  "arrival":"2021-04-13T04:48:41.256196",
  "check_in":"successful",
  "delivered":true,
  "location":"{LOCATION_ID}",
  "package_id":"{PACKAGE_ID}"
}
```
NOTE: 
* you can not add any more stops to a package once its delivery status is set to true.
* the finall arrival time from the history suffices as the time of delivery. no need to duplicate the data.

<!-- ROADMAP -->
## Future Improvements
* If lat lon is off by even a single decimal point the locations could be duplicated.
* if lat lon is off by even a single decimal point the package wont be marked as delivered.
* there is no attention given to preventing the duplication of packages.
* no authorizaion of any kind.
* Class based views are a bit of a mess and could use cleanup.
* add a data generator to create a few dummy packages.
