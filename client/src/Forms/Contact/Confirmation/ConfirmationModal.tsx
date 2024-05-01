import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";

interface ConfirmationModalProps {
  name: string;
  show: boolean;
  onHide: () => void;
}

function ConfirmationModal(props: ConfirmationModalProps) {
  return (
    <Modal
      {...props}
      size="sm"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Body className="d-flex flex-column align-items-center justify-content-center">
        <p>Thank you for your message, {props.name}!</p>
        <Button
          className="contact-button"
          variant="primary"
          onClick={props.onHide}
        >
          Close
        </Button>
      </Modal.Body>
    </Modal>
  );
}

export default ConfirmationModal;
