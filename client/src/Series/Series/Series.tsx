import { Card, Col, Container, Row } from "react-bootstrap";
import { EventSeriesObj } from "../SeriesList";
import Events from "../Events.tsx/Events";
import SeriesPoster from "./SeriesPoster";
import EditButton from "../../Buttons/EditButton/EditButton";
import DeleteButton from "../../Buttons/DeleteButton/DeleteButton";
import { useEffect, useState } from "react";
import { faEdit } from "@fortawesome/free-solid-svg-icons";
import EditModal from "../../EditModals/EditModal";
import EventForm from "../../Forms/Event/EventForm";

interface SeriesProps {
  series: EventSeriesObj;
  setSeriesList: React.Dispatch<React.SetStateAction<EventSeriesObj[]>>;
  seriesList: EventSeriesObj[];
  token: string;
}

function Series(props: SeriesProps) {
  const [series, setSeries] = useState<EventSeriesObj>(props.series);
  const [modalShow, setModalShow] = useState(false);

  useEffect(() => {
    setSeries(props.series);
  }, [props.series]);

  const EditableSeries = (
    <Container>
      <Row>
        <Col>
          <Container className="text-center">
            <EditButton setModalShow={setModalShow} faIcon={faEdit} />
            <EditModal
              show={modalShow}
              onHide={() => setModalShow(false)}
              title="Edit Concert Series"
              entity={props.series}
              form={
                <EventForm
                  setModalShow={setModalShow}
                  setSeriesList={props.setSeriesList}
                  seriesList={props.seriesList}
                  series={series}
                  isNewSeries={false}
                  setSeries={setSeries}
                  token={props.token}
                />
              }
            />
          </Container>
        </Col>

        <Col>
          <Container className="text-center">
            <DeleteButton
              series={series}
              setSeriesList={props.setSeriesList}
              seriesList={props.seriesList}
              token={props.token}
            />
          </Container>
        </Col>
      </Row>
    </Container>
  );

  return (
    <Row id={`series-${series.series_id}-row`}>
      <Col>
        <SeriesPoster
          series={series}
          setSeries={setSeries}
          token={props.token}
        />
      </Col>
      <Col>
        <Container>
          <Card>
            <h4>{series.name}</h4>
            {props.token && EditableSeries}
            <p>{series.description}</p>
            <Events events={series.events} />
          </Card>
        </Container>
      </Col>
    </Row>
  );
}

export default Series;
