import { Button } from "react-bootstrap";
import "./EmailSignupButton.css";

function EmailSignupButton() {
  const signupUrl = "http://eepurl.com/iNpJz-/";
  return (
    <Button
      id="email-signup-button"
      variant="primary"
      href={signupUrl}
      target="_self"
      rel="noopener noreferrer"
    >
      Sign up for our newsletter
    </Button>
  );
}

export default EmailSignupButton;
