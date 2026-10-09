#include <Arduino.h>
#include <DHT.h>

#define DHT_PIN 2
#define DHT_TYPE DHT11

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
    Serial.begin(9600);
    dht.begin();

    delay(2000);
    Serial.println("DormCast sensor bridge starting");
}

void loop() {
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();

    if (isnan(humidity) || isnan(temperature)) {
        Serial.println("{\"error\":\"sensor_read_failed\"}");
    } else {
        Serial.print("{\"temperature_c\":");
        Serial.print(temperature, 1);
        Serial.print(",\"humidity_percent\":");
        Serial.print(humidity, 1);
        Serial.println("}");
    }

    delay(5000);
}