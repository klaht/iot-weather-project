The docker-compose setup can be started by running the following command in the same directory as the docker-compose.yml file:

`
docker compose up --build -d
`


if the connection is not working properly when running locally, try changing the values of MQTT_URL and INFLUXDB_URL to your local ip address in the influx-logger service
