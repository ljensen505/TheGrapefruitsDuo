import Modal from "react-bootstrap/Modal";
import "./ErrorModal.css";

interface ErrorModalProps {
  error: string;
  entity: string;
  show: boolean;
}

function ErrorModal(props: ErrorModalProps) {
  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
      className="error-modal"
    >
      <Modal.Header className="error-content">
        <Modal.Title id="contained-modal-title-vcenter">API Error</Modal.Title>
      </Modal.Header>
      <Modal.Body className="error-content">
        <p>{props.error}</p>
        <p>error occurred while fetching {props.entity}</p>
        <p>Try again later or contact the site administrator</p>
      </Modal.Body>
    </Modal>
  );
}

export default ErrorModal;
