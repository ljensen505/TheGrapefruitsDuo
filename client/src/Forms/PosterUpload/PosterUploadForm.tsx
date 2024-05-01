import { Button, Container, Form, Image } from "react-bootstrap";
import { EventSeriesObj } from "../../Series/SeriesList";
import { useState } from "react";
import { sizeLimit } from "../HeadshotUpload/HeadshotUploadForm";
import { postSeriesPoster } from "../../api";

interface PosterUploadFormProps {
  series: EventSeriesObj;
  currentPoster: string | undefined;
  setModalShow: React.Dispatch<React.SetStateAction<boolean>>;
  setSeries: React.Dispatch<React.SetStateAction<EventSeriesObj>>;
  token: string;
}

function PosterUploadForm(props: PosterUploadFormProps) {
  const [preview, setPreview] = useState<string | undefined>(
    props.currentPoster,
  );
  const [fileError, setFileError] = useState<string>("");
  const [canSubmit, setCanSubmit] = useState<boolean>(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

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

    if (selectedFile) {
      postSeriesPoster(props.series.series_id, selectedFile, props.token)
        .then((updatedEventObj) => {
          props.setSeries(updatedEventObj);
          props.setModalShow(false);
        })
        .catch((error) => {
          console.error(error);
          setFileError(
            "Failed to upload poster: " + error.response.data.detail,
          );
        });
      return;
    }
    console.error("no file selected");
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
          {preview && (
            <Image
              src={preview}
              className="img-fluid rounded-circle poster-preview"
              alt={`${props.series.name} poster`}
            />
          )}
        </Container>
        <Form.Label id="poster-upload">Upload Poster</Form.Label>
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

export default PosterUploadForm;
