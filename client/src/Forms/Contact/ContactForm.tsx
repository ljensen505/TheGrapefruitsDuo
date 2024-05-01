import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { postMessage } from "../../api";
import { useState } from "react";
import { Col, Container, Row } from "react-bootstrap";
import "./ContactForm.css";
import ConfirmationModal from "./Confirmation/ConfirmationModal";
import EmailSignupButton from "../../EmailSignupButton/EmailSignupButton";

function ContactForm() {
  const [confirmationModalShow, setConfirmationModalShow] = useState(false);
  const [form, setForm] = useState<{ [key: string]: string }>({
    name: "",
    email: "",
    message: "",
  });

  const handleFormChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    postMessage(form.name, form.email, form.message)
      .then(() => {
        setConfirmationModalShow(true);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const handleFormReset = () => {
    setForm({ name: "", email: "", message: "" });
    setConfirmationModalShow(false);
  };

  return (
    <Container id="contact">
      <Row className="justify-content-center text-end">
        <Col xs={12} md={8} lg={6}>
          <Form
            className="contact-text"
            id="contact-form"
            onSubmit={handleSubmit}
          >
            <h3 className="display-3 contact-title">Contact Us</h3>
            <Form.Group className="mb-3" controlId="formBasicName">
              <Form.Control
                type="text"
                placeholder="Enter name"
                required
                name="name"
                value={form.name}
                onChange={handleFormChange}
                autoComplete="name"
              />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Control
                type="email"
                placeholder="Enter email"
                required
                name="email"
                value={form.email}
                onChange={handleFormChange}
                autoComplete="email"
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicMessage">
              <Form.Label>Message</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                required
                name="message"
                placeholder="Enter message"
                value={form.message}
                onChange={handleFormChange}
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
          <ConfirmationModal
            show={confirmationModalShow}
            onHide={handleFormReset}
            name={form.name}
          />
        </Col>
      </Row>
      <Row className="justify-content-center">
        <Container className="mt-5 text-center">
          <EmailSignupButton />
        </Container>
      </Row>
    </Container>
  );
}

export default ContactForm;
