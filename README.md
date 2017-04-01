AAA as a Service - Central Server Module
============================

The work presented here is the development of a module of Authentication, Authorisation and Accounting as a Service for the BIGSEA Project. This repository represents the usage of a central AAA Server serving developers and applications in need of the service.

![EUBRABIGSEA logo](docs/static_files/EUBRABIGSEA-logo.png "EUBRA BIGSEA")

## Disclaimer 

This repository is intended for development and testing purposes. The configurations currently available will only work with a specific DNS (eubrabigsea.dei.uc.pt). Additional configurations like localhost usage and specific DNS will be made available soon.

## Installation instructions



First you need to give the proper permissions to "start.sh" script:

```bash
chmod +x start.sh
```

After that, you can run the script which will delete all the docker containers in the system and make a clean install. Make sure you setup a proper enviroment for not to lose any previously created docker containers.

Run the script:

```bash
./start.sh
```

Wait while it gathers the necessary images and configures the containers. After a successfull initiation, the service should be up and running! 

## Usage Examples - Rest API Calls

Following there are examples of call to the AAA Server API. Additionally, you can consult the document with further instructions at /docs/AAAaaServiceDetails.pdf

To be added soon...
