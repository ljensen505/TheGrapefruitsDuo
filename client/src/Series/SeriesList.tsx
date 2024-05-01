import { Col, Container } from "react-bootstrap";
import { EventObj } from "./Events.tsx/Event/Event";
import Series from "./Series/Series";
import "./SeriesList.css";
import EditButton from "../Buttons/EditButton/EditButton";
import { useState } from "react";
import { faAdd } from "@fortawesome/free-solid-svg-icons";
import EditModal from "../EditModals/EditModal";
import EventForm from "../Forms/Event/EventForm";

export class EventSeriesObj {
  series_id: number;
  name: string;
  description: string;
  events: EventObj[];
  poster_id?: string; // Cloudinary public ID

  constructor(
    series_id: number,
    name: string,
    description: string,
    events: EventObj[],
    poster_id?: string,
  ) {
    this.series_id = series_id;
    this.name = name;
    this.description = description;
    this.events = events;
    this.poster_id = poster_id;
  }
}

interface SeriesListProps {
  seriesList: EventSeriesObj[];
  setSeriesList: React.Dispatch<React.SetStateAction<EventSeriesObj[]>>;
  token: string;
}

function SeriesList(props: SeriesListProps) {
  const seriesList = props.seriesList;
  const [modalShow, setModalShow] = useState(false);

  const AddableSeries = (
    <Container className="text-end">
      <EditButton
        setModalShow={setModalShow}
        faIcon={faAdd}
        actionName=" Event"
      />
      <EditModal
        show={modalShow}
        onHide={() => setModalShow(false)}
        title="Add Concert Series"
        form={
          <EventForm
            setModalShow={setModalShow}
            setSeriesList={props.setSeriesList}
            seriesList={props.seriesList}
            isNewSeries={true}
            token={props.token}
          />
        }
      />
    </Container>
  );

  if (seriesList.length === 0) {
    return (
      <section id="events">
        <Col>
          <Container>
            <h3 className="display-3 text-end events-title">Upcoming Events</h3>
            {props.token && AddableSeries}
          </Container>
          <Container>
            <h3 className="display-4 text-center events-title">Stay tuned!</h3>
          </Container>
        </Col>
      </section>
    );
  }

  return (
    <section id="events">
      <Col>
        <Container>
          <h3 className="display-3 text-end events-title">Upcoming Events</h3>
          {props.token && AddableSeries}
        </Container>
        {seriesList.map((series, idx) => (
          <Container key={series.series_id}>
            <Series
              series={series}
              setSeriesList={props.setSeriesList}
              seriesList={props.seriesList}
              token={props.token}
            />
            {idx < seriesList.length - 1 && <hr className="series-divider" />}
          </Container>
        ))}
      </Col>
    </section>
  );
}

export default SeriesList;
