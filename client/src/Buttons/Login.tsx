import {
  CredentialResponse,
  GoogleLogin,
  googleLogout,
} from "@react-oauth/google";
import { postUser } from "../api";
import Cookies from "js-cookie";

interface LoginProps {
  setToken: React.Dispatch<React.SetStateAction<string>>;
}

function Login(props: LoginProps) {
  const handleSuccess = async (credentialResponse: CredentialResponse) => {
    if (credentialResponse.credential) {
      const token = credentialResponse.credential;
      props.setToken(token);
      Cookies.set("token", token, { expires: 1 });
      postUser(token)
        .then((user) => {
          console.log(`Welcome, ${user.name}!`);
        })
        .catch(() => {
          console.error("Nice try, but you can't do that. Logging you out.");
          googleLogout();
          props.setToken("");
        });
    } else {
      console.error("Login Failed");
    }
  };
  return (
    <GoogleLogin
      onSuccess={handleSuccess}
      onError={() => {
        console.error("Login Failed");
      }}
    />
  );
}

export default Login;
