import paho.mqtt.client as mqtt
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import matplotlib.pyplot as p
import model

topic_send = "l2r"
topic_rec  = "r2l"

regr=MLPRegressor(activation="relu",max_iter=15000,hidden_layer_sizes=(2,2),solver="lbfgs")


def send_val(client,val):
    print("Sending Prediction  :",round(val,2),"%")
    client.publish(topic_send,str(val),2)

def process(temp,humid):
    return ml.pred(temp,humid)


def on_connect(client, userdata, flags, rc):
    print("Waiting for Sensor to send readings...")
    client.subscribe(topic_rec)

def on_message(client, userdata, msg):
    payload=str(msg.payload.decode("ascii")).split()
    temp=float(payload[0])
    humid=float(payload[1])
    print("Average Temperature : {} C\nAverage Humidity    : {} %".format(temp,humid))
    send_val(client,process(temp,humid))

def on_publish(client,userdata,mid):
    print("Sent.")
    print("Waiting for Sensor to send readings...")

def plot(d1,d2):
    x=[a[0] for a in d1]
    y=[a[1] for a in d1]
    fig=p.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.scatter(x,y,d2)
    p.show()

def main():
    # model.train()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.connect("mqtt.eclipseprojects.io", 1883, 60)
    client.loop_forever()

if __name__=='__main__':
    main()