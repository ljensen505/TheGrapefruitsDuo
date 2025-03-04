import Modal from "react-bootstrap/Modal";
import { MusicianObj } from "../Musicians/Musician/Musician";
import { GroupObj } from "../Group/Group";
import { EventSeriesObj } from "../Series/SeriesList";

interface EditModalProps {
  title: string;
  show: boolean;
  onHide: () => void;
  form: JSX.Element;
  entity?: MusicianObj | GroupObj | EventSeriesObj;
  error?: string;
  livestream_id?: string;
}

function EditModal(props: EditModalProps) {
  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          {props.title}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>{props.form}</Modal.Body>
    </Modal>
  );
}

export default EditModal;
