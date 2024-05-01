import { ListGroup } from "react-bootstrap";
import "./Event.css";

export class EventObj {
  event_id: number;
  location: string;
  time: string; // ISO 8601 formatted date-time string
  ticket_url?: string;
  map_url?: string;

  constructor(
    event_id: number,
    location: string,
    time: string,
    ticket_url?: string,
    map_url?: string,
  ) {
    this.event_id = event_id;
    this.location = location;
    this.time = time;
    this.ticket_url = ticket_url;
    this.map_url = map_url;
  }
}

interface EventProps {
  event: EventObj;
}

function Event(props: EventProps) {
  const event = props.event;
  const date = new Date(event.time);
  const dateString = date.toLocaleDateString(undefined, {
    month: "long",
    day: "numeric",
    weekday: "long",
  });
  const location = event.map_url ? (
    <>
      <a href={event.map_url} target="_blank" rel="noreferrer">
        {event.location}
      </a>
    </>
  ) : (
    event.location
  );
  const tickets = event.ticket_url ? (
    <>
      |{" "}
      <a href={event.ticket_url} target="_blank" rel="noreferrer">
        Tickets
      </a>
    </>
  ) : null;
  const timeString = date.toLocaleTimeString(undefined, {
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  });

  return (
    <ListGroup.Item className="event-list-item">
      <p>
        {dateString} {timeString.toLowerCase()} | {location} {tickets}
      </p>
    </ListGroup.Item>
  );
}

export default Event;
