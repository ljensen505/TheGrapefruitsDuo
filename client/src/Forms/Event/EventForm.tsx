import { useState } from "react";
import { Button, Container, Form } from "react-bootstrap";
import { postSeries, putSeries } from "../../api";
import { EventSeriesObj } from "../../Series/SeriesList";
import { EventObj } from "../../Series/Events.tsx/Event/Event";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash } from "@fortawesome/free-solid-svg-icons";
import "./EventForm.css";

interface AddEventFormProps {
  setModalShow: React.Dispatch<React.SetStateAction<boolean>>;
  setSeriesList: React.Dispatch<React.SetStateAction<EventSeriesObj[]>>;
  seriesList: EventSeriesObj[];
  isNewSeries: boolean;
  series?: EventSeriesObj;
  setSeries?: React.Dispatch<React.SetStateAction<EventSeriesObj>>;
  token: string;
}

function EventForm(props: AddEventFormProps) {
  /*
  this form serves two purposes:
  1. Create a new series
  2. Edit an existing series

  if isNewSeries is true,an empty form will be rendered to create a new series and post it to the server
  if isNewSeries is false, the form will be populated with existing series data and will be used to edit the series
  */
  if (props.series && props.isNewSeries) {
    throw new Error("series provided for new series form");
  }
  const [formEvents, setFormEvents] = useState<(EventObj | undefined)[]>(
    props.series === undefined
      ? [undefined]
      : props.series.events.map((event) => event),
  );
  const [postError, setPostError] = useState<string>("");
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const form = event.target as HTMLFormElement;
    const formElements = form.elements as HTMLFormControlsCollection;
    const seriesNameElement = formElements.namedItem(
      "formSeriesName",
    ) as HTMLInputElement;

    const seriesName = seriesNameElement.value;
    const seriesDescriptionElement = formElements.namedItem(
      "formSeriesDescription",
    ) as HTMLInputElement;
    const seriesDescription = seriesDescriptionElement.value;
    const eventObjects: EventObj[] = findEventElements(formElements);

    const series = new EventSeriesObj(
      (props.series && props.series.series_id) || 0,
      seriesName,
      seriesDescription,
      eventObjects,
      (props.series && props.series.poster_id) || undefined,
    );

    if (!props.token) {
      console.error("no access token");
      return;
    }
    if (props.isNewSeries) {
      postSeries(series, props.token)
        .then((newSeries) => {
          props.setSeriesList([...props.seriesList, newSeries]);
          props.setModalShow(false);
        })
        .catch((error) => {
          console.error(error);
          setPostError(
            "Failed to create series: " + error.response.data.detail,
          );
        });
    } else {
      putSeries(series, props.token)
        .then((updatedSeries) => {
          props.setSeries?.(updatedSeries);
          props.setModalShow(false);
        })
        .catch((error) => {
          console.error(error);
          setPostError(
            "Failed to update series: " + error.response.data.detail,
          );
        });
    }
  };

  function findEventElements(
    formElements: HTMLFormControlsCollection,
  ): EventObj[] {
    const events: EventObj[] = [];
    for (let idx = 0; idx < formEvents.length; idx++) {
      const locationElement = formElements.namedItem(
        `formEvent${idx}Location`,
      ) as HTMLInputElement;
      const timeElement = formElements.namedItem(
        `formEvent${idx}Time`,
      ) as HTMLInputElement;
      const ticketUrlElement = formElements.namedItem(
        `formEvent${idx}TicketUrl`,
      ) as HTMLInputElement;
      const mapUrlElement = formElements.namedItem(
        `formEvent${idx}MapUrl`,
      ) as HTMLInputElement;
      const location = locationElement.value;
      const time = timeElement.value;
      const ticketUrl = ticketUrlElement.value
        ? ticketUrlElement.value
        : undefined;
      const mapUrl = mapUrlElement.value ? mapUrlElement.value : undefined;
      const event = new EventObj(0, location, time, ticketUrl, mapUrl);
      events.push(event);
    }
    return events;
  }

  const AddEventButton = (
    <Container className="d-flex justify-content-end mt-2">
      <Button
        variant="primary"
        onClick={() => setFormEvents([...formEvents, undefined])}
      >
        Add Event to Series
      </Button>
    </Container>
  );

  const SubmitButton = (
    <Button variant="primary" type="submit">
      Submit
    </Button>
  );

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3" controlId="formSeriesName">
        <Form.Label>Series Name *</Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter series name"
          required
          name="name"
          {...(props.series && { defaultValue: props.series.name })}
        />
      </Form.Group>
      <Form.Group className="mb-3" controlId="formSeriesDescription">
        <Form.Label>Series Description *</Form.Label>
        <Form.Control
          as="textarea"
          rows={3}
          placeholder="Enter series description"
          required
          name="description"
          {...(props.series && { defaultValue: props.series.description })}
        />
      </Form.Group>

      {formEvents.map((event, idx) => (
        <Container
          key={event ? event.event_id : `temp-${idx}`}
          className="event-form-container"
        >
          <Form.Text className="mb-3">{`Event ${idx}`}</Form.Text>
          <Form.Group className="mb-3" controlId={`formEvent${idx}Location`}>
            <Form.Label>Event Location *</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter event location"
              required
              name="location"
              {...(event && {
                defaultValue: event.location,
              })}
            />
          </Form.Group>
          <Form.Group className="mb-3" controlId={`formEvent${idx}Time`}>
            <Form.Label>Event Time *</Form.Label>
            <Form.Control
              type="datetime-local"
              required
              name="time"
              {...(event && {
                defaultValue: event.time,
              })}
            />
          </Form.Group>
          <Form.Group className="mb-3" controlId={`formEvent${idx}TicketUrl`}>
            <Form.Label>Event Ticket URL</Form.Label>
            <Form.Control
              type="url"
              name="ticket_url"
              {...(event && {
                defaultValue: event.ticket_url,
              })}
            />
          </Form.Group>
          <Form.Group className="mb-3" controlId={`formEvent${idx}MapUrl`}>
            <Form.Label>Event Map URL</Form.Label>
            <Form.Control
              type="url"
              name="map_url"
              {...(event && {
                defaultValue: event.map_url,
              })}
            />
          </Form.Group>
          <Container className="d-flex justify-content-end mb-1">
            <Button
              variant="danger"
              onClick={() => {
                if (event) {
                  setFormEvents(
                    formEvents.filter((e) => e?.event_id !== event.event_id),
                  );
                } else {
                  setFormEvents(formEvents.filter((_, i) => i !== idx));
                }
              }}
            >
              <FontAwesomeIcon icon={faTrash} />
            </Button>
          </Container>
        </Container>
      ))}

      {AddEventButton}

      <Form.Text>
        A poster can be added after returning to the homepage.
      </Form.Text>
      {postError && (
        <Form.Text className="text-danger error-text">{postError}</Form.Text>
      )}

      <Container className="d-flex justify-content-end">
        {SubmitButton}
      </Container>
    </Form>
  );
}

export default EventForm;
