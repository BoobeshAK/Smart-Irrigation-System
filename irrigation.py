import spidev
import time
import RPi.GPIO as GPIO

# 1. Relay Configuration
RELAY_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# Initially keep pump OFF
GPIO.output(RELAY_PIN, GPIO.HIGH)

# 2. SPI Configuration for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# 3. Read Soil Moisture Sensor
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# 4. Sensor Configuration
MOISTURE_CHANNEL = 0
THRESHOLD = 500

# 5. Main Irrigation Program
try:
    print("SMART IRRIGATION SYSTEM STARTED")
    print("--------------------------------")

    while True:

        # Read moisture value
        moisture_value = read_channel(MOISTURE_CHANNEL)

        print(f"Soil Moisture Value: {moisture_value}")

        # Irrigation Decision
        if moisture_value < THRESHOLD:

            print("Decision: IRRIGATION NEEDED")

            GPIO.output(RELAY_PIN, GPIO.LOW)
            print("Pump ON")

        else:

            print("Decision: NO IRRIGATION (Soil Wet)")

            GPIO.output(RELAY_PIN, GPIO.HIGH)
            print("Pump OFF")

        print("--------------------------------")

        time.sleep(5)

except KeyboardInterrupt:

    print("\nSystem stopped by user")

finally:

    # Turn OFF pump before exit
    GPIO.output(RELAY_PIN, GPIO.HIGH)

    GPIO.cleanup()
    spi.close()

    print("System safely closed")
