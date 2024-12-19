The docker-compose setup can be started by running the following command in the same directory as the docker-compose.yml file:

`
docker compose up --build -d
`


if the connection is not working properly when running locally, try changing the values of MQTT_URL and INFLUXDB_URL to your local ip address in the influx-logger service

Once working, the services should be accessible:

MQTT Broker at http://localhost:1883

Influxdb at http://localhost:8086

Grafana at http://localhost:3000
