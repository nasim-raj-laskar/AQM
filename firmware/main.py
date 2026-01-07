from machine import ADC, Pin, I2C
import network, time, gc, urequests
import dht
import ssd1306

#CONFIG
WIFI_SSID = "WIFISSID"
WIFI_PASS = "WIFIPASSWORD"

BACKEND_URL = "http://<HOST:ip>/infer"
LOG_INTERVAL = 5  # seconds


#MQ135
mq = ADC(Pin(34))
mq.atten(ADC.ATTN_11DB)

#DHT11
dht_sensor = dht.DHT11(Pin(4))

#OLED 
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#OLED
def oled_clear():
    oled.fill(0)
    oled.show()

def oled_error(msg):
    oled.fill(0)
    oled.text("ERROR", 0, 0)
    oled.text(msg, 0, 16)
    oled.show()

def oled_display(temp, hum, mq, resp):
    oled.fill(0)
    oled.text("AIR QUALITY", 0, 0)

    oled.text("T:{}C".format(temp), 0, 16)
    oled.text("H:{}%".format(hum), 64, 16)
    oled.text("MQ:{}".format(mq), 0, 28)

    if resp:
        oled.text("AQ:", 0, 44)
        oled.text(resp["aq_label"], 32, 44)

        if resp["anomaly"]:
            oled.text("ANOMALY!", 0, 56)
        else:
            oled.text("Normal", 0, 56)
    else:
        oled.text("BACKEND ERR", 0, 44)

    oled.show()

#WIFI
def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        oled_clear()
        oled.text("Connecting WiFi", 0, 0)
        oled.show()

        wlan.connect(WIFI_SSID, WIFI_PASS)

        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        oled.text("WiFi OK", 0, 16)
        oled.text(ip, 0, 28)
        oled.show()
        print("WiFi connected:", wlan.ifconfig())
        return True
    else:
        oled_error("WiFi FAIL")
        return False

#BACKEND
def send_to_backend(temp, hum, mq):
    payload = {
        "temp": temp,
        "hum": hum,
        "mq": mq
    }

    try:
        r = urequests.post(
            BACKEND_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if r.status_code == 200:
            data = r.json()
            r.close()
            return data
        else:
            r.close()
            return None

    except Exception as e:
        print("HTTP error:", e)
        return None

oled_clear()
oled.text("Booting...", 0, 0)
oled.show()
time.sleep(1)

wifi_connect()

if not wifi_connect():
    while True:
        time.sleep(5)
        
while True:
    try:
        dht_sensor.measure()

        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        mq_val = mq.read()

        response = send_to_backend(temp, hum, mq_val)

        oled_display(temp, hum, mq_val, response)

        print("Sent:", temp, hum, mq_val)
        print("Resp:", response)

    except Exception as e:
        print("Loop error:", e)
        oled_error("SENSOR ERR")

    gc.collect()
    time.sleep(LOG_INTERVAL)
