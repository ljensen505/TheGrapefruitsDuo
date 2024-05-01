import { googleLogout } from "@react-oauth/google";
import { Button } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRightFromBracket } from "@fortawesome/free-solid-svg-icons";
import Cookies from "js-cookie";

interface LogoutProps {
  setToken: React.Dispatch<React.SetStateAction<string>>;
}

function Logout(props: LogoutProps) {
  const handleLogout = () => {
    googleLogout();
    props.setToken("");
    Cookies.remove("token");
  };

  return (
    <Button onClick={handleLogout}>
      <FontAwesomeIcon icon={faRightFromBracket} />
    </Button>
  );
}

export default Logout;
