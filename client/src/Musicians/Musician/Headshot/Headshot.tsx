import { faUpload } from "@fortawesome/free-solid-svg-icons";
import EditButton from "../../../Buttons/EditButton/EditButton";
import { Col, Container, Image } from "react-bootstrap";
import HeadshotUpload from "../../../Forms/HeadshotUpload/HeadshotUploadForm";
import EditModal from "../../../EditModals/EditModal";
import { useState } from "react";
import { MusicianObj } from "../Musician";
import "./Headshot.css";

export interface HeadshotProps {
  src: string;
  musician: MusicianObj;
  onHeadshotChange?: () => void;
  setMusician?: React.Dispatch<React.SetStateAction<MusicianObj>>;
  token: string;
}

function Headshot(props: HeadshotProps) {
  const [modalShow, setModalShow] = useState(false);

  const EditableHeadshot = (
    <Container>
      <EditButton
        setModalShow={setModalShow}
        faIcon={faUpload}
        actionName=" Headshot"
      />
      <EditModal
        show={modalShow}
        onHide={() => setModalShow(false)}
        title="Edit Headshot"
        entity={props.musician}
        form={
          <HeadshotUpload
            currentHeadshot={props.src}
            musician={props.musician}
            onHeadshotChange={props?.onHeadshotChange}
            hideModal={setModalShow}
            setMusician={props?.setMusician}
            token={props.token}
          />
        }
      />
    </Container>
  );

  return (
    <Col
      key="headshot"
      className="d-flex align-items-center justify-content-center position-relative"
    >
      <Container className="d-flex align-items-center justify-content-center flex-column">
        <Image
          src={props.src}
          className="img-fluid rounded-circle"
          alt={props.musician.name}
        />
        {props.token && EditableHeadshot}
      </Container>
    </Col>
  );
}

export default Headshot;
