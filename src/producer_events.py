import requests
from cloudevents.http import CloudEvent
from cloudevents.conversion import to_structured
from datetime import datetime

# Class to handle the generation of event IDs (in-memory)
class EventIDManager:
    def __init__(self):
        self.current_id = 1  # Start from 1 or any initial value

    # Increment and return the next event ID
    def get_next_event_id(self):
        event_id = f"A234-1234-{self.current_id:04d}"  # Format ID
        self.current_id += 1  # Increment the counter
        return event_id

# Function to create and send events
def produce_event(event_id_manager):
    # Define the event attributes and data
    attributes = {
        "specversion": "1.0",
        "type": "com.example.object.created",
        "source": "/mycontext",
        "id": event_id_manager.get_next_event_id(),
        "time": str(datetime.utcnow()),  # Current timestamp
        "datacontenttype": "application/json"
    }

    data = {
        "message": "Hello, CloudEvents!"
    }

    # Create the CloudEvent
    event = CloudEvent(attributes, data)

    # Convert CloudEvent to structured format (JSON)
    headers, body = to_structured(event)

    # Send the event to the consumer
    response = requests.post(
        "http://localhost:5000/",  # The consumer endpoint
        headers=headers,
        data=body  # Sending the body in structured format
    )

    print(f"Sent event with ID: {attributes['id']}")
    print(f"Response from Consumer: {response.status_code}")

# Instantiate the ID manager (in-memory counter)
event_id_manager = EventIDManager()

# Produce multiple events
for _ in range(20):  # Send 20 events for demonstration
    produce_event(event_id_manager)
