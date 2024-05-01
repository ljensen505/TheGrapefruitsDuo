import { ButtonGroup, Container } from "react-bootstrap";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import Profile from "../../Auth/Profile";
import Login from "../../Buttons/Login";
import Logout from "../../Buttons/Logout";
import "./AdminDropdown.css";

interface AdminDropdownProps {
  appVersion: string;
  apiVersion: string;
  token: string;
  setToken: React.Dispatch<React.SetStateAction<string>>;
}

function AdminDropdown(props: AdminDropdownProps) {
  const AuthButton = () => {
    return props.token ? (
      <Logout setToken={props.setToken} />
    ) : (
      <Login setToken={props.setToken} />
    );
  };

  return (
    <>
      <DropdownButton
        as={ButtonGroup}
        align={{ lg: "end" }}
        title="Admin"
        id="admin-dropdown"
        variant="link"
        className="navbar-text-color"
      >
        {props.token && <Profile token={props.token} />}
        <Dropdown.Item eventKey="1" className="text-end" id="auth-row">
          <AuthButton />
        </Dropdown.Item>
        <Dropdown.Divider />
        <Container className="text-end text-muted" id="api-container">
          <p>APP Version: {props.appVersion}</p>
          <p>API Version: {props.apiVersion}</p>
        </Container>
      </DropdownButton>
    </>
  );
}

export default AdminDropdown;
