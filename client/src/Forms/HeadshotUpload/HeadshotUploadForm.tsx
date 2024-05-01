import { Form, Image, Button, Container } from "react-bootstrap";
import { MusicianObj } from "../../Musicians/Musician/Musician";
import { useState } from "react";
import { postHeadshot } from "../../api";
import "./HeadshotUpload.css";

export const sizeLimit = 1000000; // one megabyte

interface HeadshotUploadProps {
  currentHeadshot: string;
  musician: MusicianObj;
  onHeadshotChange?: () => void;
  hideModal?: React.Dispatch<React.SetStateAction<boolean>>;
  setMusician?: React.Dispatch<React.SetStateAction<MusicianObj>>;
  token: string;
}

function HeadshotUpload(props: HeadshotUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState<string>("");
  const [preview, setPreview] = useState<string>(props.currentHeadshot);
  const [canSubmit, setCanSubmit] = useState<boolean>(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const allowedTypes = ["image/jpeg", "image/png"];
    const file = event.target.files?.[0];
    const fileSize = file?.size; // bytes
    const fileType = file?.type; // MIME type

    if (fileSize && fileSize > sizeLimit) {
      console.error("file too large");
      setFileError("file too large");
      setCanSubmit(false);
      return;
    }
    if (fileType && !allowedTypes.includes(fileType)) {
      console.error("invalid file type");
      setFileError("invalid file type");
      setCanSubmit(false);
      return;
    }

    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
      setCanSubmit(true);
      setFileError("");
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!props.token) {
      console.error("no access token");
      return;
    }

    if (props.musician && selectedFile) {
      uploadHeadshot(props.token, props.musician, selectedFile);
      props.hideModal?.(false);

      return;
    }
    console.error("no file selected");
  };

  const uploadHeadshot = async (
    accessToken: string,
    musician: MusicianObj,
    file: File,
  ) => {
    postHeadshot(musician.id, file, accessToken)
      .then((updatedMusician) => {
        props.onHeadshotChange?.();
        props.setMusician?.(updatedMusician);
      })
      .catch((error) => {
        console.error(error);
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
      <Form.Group controlId="formFile" className="mb-3">
        <Container className="d-flex justify-content-center">
          <Image
            src={preview}
            className="img-fluid rounded-circle headshot-preview"
            alt={`${props.musician.name} headshot`}
          />
        </Container>
        <Form.Label id="headshot-upload">Upload Headshot</Form.Label>
        <Form.Control type="file" onChange={handleFileChange} />
        <Form.Text className="text-muted">
          size limit: {sizeLimit / 1000000} MB
        </Form.Text>
        {fileError && (
          <Form.Text className="text-danger error-text">{fileError}</Form.Text>
        )}
      </Form.Group>
      <Container className="d-flex justify-content-end">
        {SubmitButton}
      </Container>
    </Form>
  );
}

export default HeadshotUpload;
