import "./App.css";
import Musicians from "./Musicians/Musicians";
import NavBar from "./NavBar/NavBar";
import ContactForm from "./Forms/Contact/ContactForm";
import { Container } from "react-bootstrap";
import Group, { GroupObj } from "./Group/Group";
import SeriesList, { EventSeriesObj } from "./Series/SeriesList";
import { useState, useEffect } from "react";
import Footer from "./Footer/Footer";
import { getRoot } from "./api";
import { MusicianObj } from "./Musicians/Musician/Musician";
import ErrorModal from "./ErrorModal/ErrorModal";
import Cookies from "js-cookie";

function App() {
  const tokenCookie = Cookies.get("token");
  const [group, setGroup] = useState<GroupObj>();
  const [update, setUpdate] = useState<boolean>(false);
  const [musicians, setMusicians] = useState<MusicianObj[]>([]);
  const [seriesList, setSeriesList] = useState<EventSeriesObj[]>([]);
  const [apiVersion, setApiVersion] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [errorModalShow, setErrorModalShow] = useState<boolean>(false);
  const [errorEntity, setErrorEntity] = useState<string>("");
  const [token, setToken] = useState<string>(tokenCookie ? tokenCookie : "");
  const appVersion = import.meta.env.PACKAGE_VERSION;

  const handleGroupBioChange = () => {
    setUpdate(!update);
  };

  const handleError = (error: string, entity: string) => {
    console.error(error);
    setError(error);
    setErrorEntity(entity);
    setErrorModalShow(true);
  };

  useEffect(() => {
    getRoot()
      .then((tgd): void => {
        setGroup(tgd.group);
        setMusicians(tgd.musicians);
        setSeriesList(tgd.events);
        setApiVersion(tgd.version);
      })
      .catch((error) => {
        handleError(error.message, "root");
      });
  }, []);

  return (
    <div id="home">
      <NavBar
        musicians={musicians}
        apiVersion={apiVersion}
        appVersion={appVersion}
        token={token}
        setToken={setToken}
      />
      <Container id="content" style={{ maxWidth: "1200px", margin: "0 auto" }}>
        <Group
          group={group}
          onBioChange={handleGroupBioChange}
          setGroup={setGroup}
          token={token}
        />
        <Musicians
          musicians={musicians}
          setMusicians={setMusicians}
          token={token}
        />
        <SeriesList
          seriesList={seriesList}
          setSeriesList={setSeriesList}
          token={token}
        />
        <ContactForm />
      </Container>
      <Footer />
      <ErrorModal error={error} show={errorModalShow} entity={errorEntity} />
    </div>
  );
}

export default App;
