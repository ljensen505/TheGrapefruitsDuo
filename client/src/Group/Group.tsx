import { Card, Container } from "react-bootstrap";
import "./Group.css";
import EditModal from "../EditModals/EditModal";
import { useState } from "react";
import EditBioForm from "../Forms/Bio/BioForm";
import { faPen } from "@fortawesome/free-solid-svg-icons";
import EditButton from "../Buttons/EditButton/EditButton";
import LivestreamPlayer from "../LivestreamPlayer/LivestreamPlayer";

export class GroupObj {
  id: number;
  name: string;
  bio: string;
  livestream_id: string;

  constructor(id: number, name: string, bio: string, livestream_id: string) {
    this.id = id;
    this.name = name;
    this.bio = bio;
    this.livestream_id = livestream_id;
  }
}

interface GroupProps {
  group?: GroupObj;
  onBioChange: () => void;
  setGroup: React.Dispatch<React.SetStateAction<GroupObj | undefined>>;
  token: string;
}

function Group(props: GroupProps) {
  const [modalShow, setModalShow] = useState(false);
  if (!props.group) {
    return null;
  }
  const group = props.group;

  const EditTitle = `Edit ${group.name}'s Bio`;

  const EditIcon = (
    <Container>
      <EditButton
        setModalShow={setModalShow}
        faIcon={faPen}
        actionName=" Group"
      />
      <EditModal
        show={modalShow}
        onHide={() => setModalShow(false)}
        title={EditTitle}
        entity={group}
        form={
          <EditBioForm
            entity={group}
            hideModal={setModalShow}
            onBioChange={props.onBioChange}
            setGroup={props.setGroup}
            token={props.token}
            livestream_id={group.livestream_id}
          />
        }
      />
    </Container>
  );

  return (
    <section id="about">
      <Container className="vh-100 d-flex align-items-center justify-content-center text-center">
        <Card className="group-info">
          <Card.Body>
            <Card.Title>
              <h1>{group.name}</h1>
            </Card.Title>
            {group.livestream_id && (
              <LivestreamPlayer livestreamId={group.livestream_id} />
            )}
            {props.token && EditIcon}
            <Card.Text className="lead group-bio">{group.bio}</Card.Text>
          </Card.Body>
        </Card>
      </Container>
    </section>
  );
}

export default Group;
