# !/usr/bin/python
import sys
import Adafruit_DHT
import paho.mqtt.client as mqtt
from RPLCD import CharLCD
from RPi import GPIO
import time

topic_send = "r2l"
topic_rec  = "l2r"

readings=2

lcd = CharLCD(numbering_mode=GPIO.BOARD,cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

def send_data(client):
    try :
        humidity=float(sys.argv[1])
        temperature=float(sys.argv[2])
        client.publish(topic_send,str(temperature)+" "+str(humidity))
    except:
        l=[[0,0]]
        print("Temperature\tHumidity")
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(11, 4)

            print("    {}   \t  {}   ".format(temperature,humidity))

            l.append( [ temperature+l[-1][0] , humidity+l[-1][1] ] )
            if len(l)==readings+1:
                break;
        temperature=l[-1][0]/readings
        humidity=l[-1][1]/readings
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("Temp   : %0.1f C" % temperature)
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Humidity: %0.1f %%" % humidity)
        client.publish(topic_send,str(temperature)+" "+str(humidity))

def on_connect(client, userdata, flags, rc):

    print("Calculating Reading...")
    send_data(client)


def on_publish(client,userdata,mid):
    print("Readings Published")
    print("Waiting for Server...")
    client.subscribe(topic_rec)
    

def display(val):
    print("The expected value of water irrigation is {}%".format(round(val,2)))
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Required Flow :")
    lcd.cursor_pos = (1, 0)
    lcd.write_string(" %0.2f %%" % val)
    time.sleep(10)

def on_message(client,userdata,msg):
    value=float(msg.payload.decode("ascii"))
    time.sleep(4)
    display(value)
    client.disconnect()
    

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message
    client.connect("mqtt.eclipseprojects.io", 1883, 60)
    client.loop_forever()

if __name__=='__main__':
    main()