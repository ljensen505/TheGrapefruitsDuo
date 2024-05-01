import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faInstagram,
  faFacebook,
  faYoutube,
} from "@fortawesome/free-brands-svg-icons";
import "./Footer.css";
import { Container, Row, Col } from "react-bootstrap";
import { Nav } from "react-bootstrap";

const currentYear = new Date().getFullYear();

const copyright = (
  <p className="text-center">&copy; {currentYear} The Grapefruits Duo</p>
);

function Footer() {
  return (
    <footer className="footer py-3">
      <Container>
        <Row>
          <Col className="text-center">
            <Nav className="justify-content-center">
              <Nav.Link
                href="https://www.instagram.com/thegrapefruitsduo/"
                className="m-2"
                target="_blank"
              >
                <FontAwesomeIcon icon={faInstagram} />
              </Nav.Link>
              <Nav.Link
                href="https://www.facebook.com/thegrapefruitsduo"
                className="m-2"
                target="_blank"
              >
                <FontAwesomeIcon icon={faFacebook} />
              </Nav.Link>
              <Nav.Link
                href="https://www.youtube.com/channel/UCzc-ds_awbx3RpGmLWEetKw"
                className="m-2"
                target="_blank"
              >
                <FontAwesomeIcon icon={faYoutube} />
              </Nav.Link>
            </Nav>
          </Col>
        </Row>
        <Row>
          <Col className="text-center">{copyright}</Col>
        </Row>
      </Container>
    </footer>
  );
}

export default Footer;
