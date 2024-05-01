import { Container, Image } from "react-bootstrap";
import { EventSeriesObj } from "../SeriesList";
import cld from "../../Cld/CloudinaryConfig";
import { useState } from "react";
import EditButton from "../../Buttons/EditButton/EditButton";
import { faUpload } from "@fortawesome/free-solid-svg-icons";
import EditModal from "../../EditModals/EditModal";
import PosterUploadForm from "../../Forms/PosterUpload/PosterUploadForm";

interface SeriesPosterProps {
  series: EventSeriesObj;
  setSeries: React.Dispatch<React.SetStateAction<EventSeriesObj>>;
  token: string;
}

function SeriesPoster(props: SeriesPosterProps) {
  const series = props.series;
  const imgUrl = cld.image(series.poster_id).toURL();
  const imgSrc = imgUrl ? imgUrl : undefined;
  const [modalShow, setModalShow] = useState(false);

  const EditablePoster = (
    <Container className="">
      <EditButton
        setModalShow={setModalShow}
        faIcon={faUpload}
        actionName=" Poster"
      />
      <EditModal
        show={modalShow}
        onHide={() => setModalShow(false)}
        title="Edit Poster"
        entity={props.series}
        form={
          <PosterUploadForm
            series={series}
            currentPoster={imgSrc}
            setModalShow={setModalShow}
            setSeries={props.setSeries}
            token={props.token}
          />
        }
      />
    </Container>
  );

  return (
    <Container>
      {series.poster_id ? (
        <Image src={imgSrc} alt={series.name} className="img-fluid" />
      ) : null}
      {props.token && EditablePoster}
    </Container>
  );
}

export default SeriesPoster;
