This app monitors website/s availability periodically, produces metrics like status_code, 
HTTP response time, if a regexp exists etc. and passes this
information to Aiven PostgreSQL database via Aiven Kafka.

Prerequisite- 
- Need to create the Aiven PostgreSQL database and Aiven Kafka service.
- Kafka producer and consumer is using SSL auth, so need to download the 
  service.key, service.cert and ca.pem files from Aiven Kafka and add in 
  the /keys directory.
- This application uses the websites.json file to get the
  list of websites and regexp for monitoring. 

To build the docker image :

    sudo docker build -t IMAGE_NAME .

To run the docker image :

    sudo docker run -it IMAGE_NAME 