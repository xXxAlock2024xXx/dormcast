import json
import serial

SERIAL_PORT = "/dev/cu.usbserial-120"
BAUD_RATE = 9600



def main():

    print(f"Connecting to serial port {SERIAL_PORT} at {BAUD_RATE} baud rate...")

    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as connection:
        print("Connected to serial port.")

        while True:
            line = connection.readline().decode("utf-8", errors="ignore").strip()

            if not line:
                continue
            try:

                reading = json.loads(line)

                temperature = reading["temperature_c"]
                humidity = reading["humidity_percent"]

                print(f"Temperature: {temperature:.1f} °C | Humidity: {humidity:.1f} %")

            except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                if line.startswith("{"):
                    print(f"Skipping invalid reading: {line}")


if __name__ == "__main__":
    main()

