import { Button } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { IconDefinition } from "@fortawesome/free-solid-svg-icons";
import "./EditButton.css";

interface EditButtonProps {
  setModalShow: React.Dispatch<React.SetStateAction<boolean>>;
  faIcon: IconDefinition;
  actionName?: string;
}

function EditButton(props: EditButtonProps) {
  return (
    <Button
      className="edit-icon btn-edit"
      onClick={() => {
        props.setModalShow(true);
      }}
    >
      <FontAwesomeIcon icon={props.faIcon} />
      {props.actionName}
    </Button>
  );
}

export default EditButton;
