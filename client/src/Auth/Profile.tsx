import { Container } from "react-bootstrap";
import { JwtPayload, jwtDecode } from "jwt-decode";

interface GoogleJwtPayload extends JwtPayload {
  picture?: string;
  name?: string;
  email?: string;
}

interface ProfileProps {
  token: string;
}

const Profile = (props: ProfileProps) => {
  const decoded = jwtDecode<GoogleJwtPayload>(props.token);
  const name = decoded.name;
  const email = decoded.email;
  return (
    props.token && (
      <Container className="text-end">
        <p>
          Logged in as: <strong>{name}</strong>
        </p>
        <p>{email}</p>
      </Container>
    )
  );
};

export default Profile;
