import { Button, Container, Form } from "react-bootstrap";
import { MusicianObj } from "../../Musicians/Musician/Musician";
import { GroupObj } from "../../Group/Group";
import { patchMusician, patchGroup } from "../../api";
import { useState } from "react";

interface EditBioFormProps {
  entity: MusicianObj | GroupObj;
  hideModal: React.Dispatch<React.SetStateAction<boolean>>;
  onBioChange: () => void;
  setGroup?: React.Dispatch<React.SetStateAction<GroupObj | undefined>>;
  setMusician?: React.Dispatch<React.SetStateAction<MusicianObj>>;
  token: string;
}

function EditBioForm(props: EditBioFormProps) {
  const [formBio, setFormBio] = useState<string>(props.entity.bio);
  const [canSubmit, setCanSubmit] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const handleBioChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setFormBio(event.target.value);
    setCanSubmit(true);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (props.entity instanceof MusicianObj) {
      updateMusician(props.token, props.entity);
    } else if (props.entity instanceof GroupObj) {
      updateGroup(props.token, props.entity);
    } else {
      console.error("Invalid entity type");
    }
    props.onBioChange();
    props.hideModal(false);
  };

  const updateMusician = async (
    accessToken: string,
    musician: MusicianObj,
  ): Promise<void> => {
    patchMusician(
      musician.id,
      formBio,
      musician.name,
      musician.headshot_id,
      accessToken,
    )
      .then((patchedMusician) => {
        if (props.setMusician) {
          props.setMusician(patchedMusician);
        }
      })
      .catch((error) => {
        console.error(error);
        setError("Failed to update bio: " + error.response.data.detail);
      });
  };

  const updateGroup = async (
    accessToken: string,
    group: GroupObj,
  ): Promise<void> => {
    patchGroup(group.id, formBio, group.name, accessToken)
      .then((patchedGroup) => {
        if (props.setGroup) {
          props.setGroup(patchedGroup);
        }
      })
      .catch((error) => {
        console.error(error);
        setError("Failed to update bio: " + error.response.data.detail);
      });
  };

  const SubmitButton = canSubmit ? (
    <Button variant="primary" type="submit">
      Submit
    </Button>
  ) : (
    <Button variant="primary" type="submit" disabled>
      Submit
    </Button>
  );

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group controlId="formBio">
        <Form.Label>Bio</Form.Label>
        <Form.Control
          as="textarea"
          rows={10}
          required
          value={formBio}
          autoFocus
          onChange={handleBioChange}
        />
        {error && (
          <Form.Text className="text-danger error-text">{error}</Form.Text>
        )}
      </Form.Group>
      <Container className="d-flex justify-content-end mt-3">
        {SubmitButton}
      </Container>
    </Form>
  );
}

export default EditBioForm;
