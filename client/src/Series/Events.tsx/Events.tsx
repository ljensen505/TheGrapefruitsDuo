import { ListGroup } from "react-bootstrap";
import Event, { EventObj } from "./Event/Event";
import "./Events.css";

interface EventsProps {
  events: EventObj[];
}

function Events(props: EventsProps) {
  const events = props.events;

  return (
    <>
      <ListGroup className="event-list">
        {events.map((event) => (
          <Event key={event.event_id} event={event} />
        ))}
      </ListGroup>
    </>
  );
}

export default Events;
