from flask import Flask, request
from cloudevents.http import from_http

app = Flask(__name__)

@app.route("/", methods=["POST"])
def receive_cloudevent():
    # Parse the incoming CloudEvent from HTTP request
    event = from_http(request.headers, request.get_data())

    # Access and print event attributes and data
    print(f"Received CloudEvent: {event['specversion']}")
    print(f"Type: {event['type']}")
    print(f"Source: {event['source']}")
    print(f"ID: {event['id']}")
    print(f"Time: {event['time']}")
    print(f"Content Type: {event['datacontenttype']}")
    print(f"Data: {event.data}")

    # Respond to the producer
    return "Event received", 200

if __name__ == "__main__":
    app.run(port=5000)
