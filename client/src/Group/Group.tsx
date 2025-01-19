import { Card, Container, Image } from "react-bootstrap";
import "./Group.css";
import EditModal from "../EditModals/EditModal";
import { useEffect, useState } from "react";
import EditBioForm from "../Forms/Bio/BioForm";
import { faPen } from "@fortawesome/free-solid-svg-icons";
import EditButton from "../Buttons/EditButton/EditButton";
import LivestreamPlayer from "../LivestreamPlayer/LivestreamPlayer";
import cld from "../Cld/CloudinaryConfig";

export class GroupObj {
  id: number;
  name: string;
  bio: string;
  livestream_id: string;
  livestream_program_cld_id?: string;

  constructor(
    id: number,
    name: string,
    bio: string,
    livestream_id: string,
    livestream_program_cld_id?: string,
  ) {
    this.id = id;
    this.name = name;
    this.bio = bio;
    this.livestream_id = livestream_id;
    this.livestream_program_cld_id = livestream_program_cld_id;
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
  const [programId, setProgramId] = useState<string | undefined>(undefined);
  const [programUrl, setProgramUrl] = useState<string | undefined>(undefined);

  const group = props.group;

  useEffect(() => {
    if (group) {
      setProgramId(group.livestream_program_cld_id);
    }
    if (programId) {
      setProgramUrl(cld.image(programId).toURL());
    }
  }, [group, programId]);

  if (!group) {
    return null;
  }

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
      <Container className="d-flex align-items-center justify-content-center text-center">
        <Card className="group-info">
          <Card.Body>
            <Card.Title>
              <h1>{group.name}</h1>
            </Card.Title>
            {group.livestream_id && (
              <LivestreamPlayer livestreamId={group.livestream_id} />
            )}
            {group.livestream_id && group.livestream_program_cld_id && (
              <Container className="d-flex align-items-center justify-content-center flex-column">
                <a href={programUrl} target="_blank">
                  <Image
                    src={programUrl}
                    className="img-fluid"
                    alt="A of the current livestream"
                  />
                </a>
              </Container>
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
