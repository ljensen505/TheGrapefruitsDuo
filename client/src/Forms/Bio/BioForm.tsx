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
  livestream_id?: string;
}

function EditBioForm(props: EditBioFormProps) {
  const [formBio, setFormBio] = useState<string>(props.entity.bio);
  const [formLivestreamId, setFormLivestreamId] = useState<string | undefined>(
    props.livestream_id,
  );
  const [canSubmit, setCanSubmit] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const handleBioChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setFormBio(event.target.value);
    setCanSubmit(true);
  };

  const handleLivestreamChange = (
    event: React.ChangeEvent<HTMLTextAreaElement>,
  ) => {
    setFormLivestreamId(event.target.value);
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
        setError("Failed to update bio: " + error.response.data.detail);
      });
  };

  const updateGroup = async (
    accessToken: string,
    group: GroupObj,
  ): Promise<void> => {
    const livestream_id = formLivestreamId ? formLivestreamId : "";
    patchGroup(group.id, formBio, livestream_id, group.name, accessToken)
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
      {/* need to account for empty string, which is falsy but the field should still show */}
      {props.livestream_id != undefined && (
        <Form.Group controlId="formLivestreamId">
          <p className="text-muted">
            A livestream id is part of a youtube url. Either
            ".../v=[livestream_id]" or ".../live/[livestream_id]". For example,
            "ncyl7cTU9k8" but without the quotations. Don't mess it up.{" "}
            <br></br>
            To remove an embedded livestream, just clear this field and submit
            the form.
          </p>
          <Form.Label>Livestream ID:</Form.Label>
          <Form.Control
            as="textarea"
            value={formLivestreamId}
            rows={1}
            onChange={handleLivestreamChange}
            placeholder=""
          />
        </Form.Group>
      )}
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
