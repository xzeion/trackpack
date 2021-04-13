#TrackPack

<!-- ABOUT THE PROJECT -->
## About The Project
A simple flask based application for shipping and tracking packages.

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites
* If on windows install git for windows and use the git terminal to run the build script
* Regardless of system make sure you have docker and docker-compose installed
* Make sure your user is part of the docker group if you are running linux

### Installation

1. Clone the repo
   ```sh
   git clone https://git.gratton.us/brian/trackpack.git
   ```
2. Execute the build script
   ```sh
   sh build
   ```
* NOTE: the build script will also execute the testing suite



<!-- USAGE EXAMPLES -->
## Usage

This project allows for a few simple api calls that are documented below.

#### Loacations are stored as 5 decimal place lat and long coordinates
#### with the intent being to integrate google maps to aquire the actual addresses
```sh
# Create a new package in the system
curl -X POST \
  localhost:5000/api/v1/create \
  -d "shipper_name=Delivery Dans Custom T's",
  -d "shipper_location=45.12345,54.54321"
  -d "reciever_name=Brian Gratton",
  -d "reciever_location=43.34212,-83.88431"
```
This should return a json object letting you know a new package was added
and the package id for your records.
```json
{"Success": "New Package Added, PID: 62f29b1b-66b2-4adf-bc8a-0cb2f785b03f"}
```

<!-- ROADMAP -->
## Roadmap

###
