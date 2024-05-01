import EditButton from "../../../Buttons/EditButton/EditButton";
import { useEffect, useState } from "react";
import { Col, Card, Container } from "react-bootstrap";
import EditBioForm from "../../../Forms/Bio/BioForm";
import EditModal from "../../../EditModals/EditModal";
import { MusicianObj } from "../Musician";
import { faPen } from "@fortawesome/free-solid-svg-icons";

interface BioProps {
  musician: MusicianObj;
  textPosition: string;
  onBioChange: () => void;
  setMusician: React.Dispatch<React.SetStateAction<MusicianObj>>;
  token: string;
}

function MusicianBio(props: BioProps) {
  const [modalShow, setModalShow] = useState(false);
  const EditTitle = `Edit ${props.musician.name}'s Bio`;

  useEffect(() => {
    props.setMusician(props.musician);
  }, [props]);

  const Editable = (
    <Container>
      <EditButton
        setModalShow={setModalShow}
        faIcon={faPen}
        actionName=" Bio"
      />
      <EditModal
        show={modalShow}
        onHide={() => setModalShow(false)}
        title={EditTitle}
        entity={props.musician}
        form={
          <EditBioForm
            entity={props.musician}
            hideModal={setModalShow}
            onBioChange={props.onBioChange}
            setMusician={props.setMusician}
            token={props.token}
          />
        }
      />
    </Container>
  );

  return (
    <Col md={6} key="bioCard">
      <Card className={`${props.textPosition}`}>
        <Card.Header className="display-6">{props.musician.name}</Card.Header>
        <Card.Body>
          {props.token && Editable}
          <Card.Text>{props.musician.bio}</Card.Text>
        </Card.Body>
      </Card>
    </Col>
  );
}

export default MusicianBio;
