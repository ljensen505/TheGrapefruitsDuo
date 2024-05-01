import { useState } from "react";
import Musician, { MusicianObj } from "./Musician/Musician";
import { Col, Container } from "react-bootstrap";
import "./Musicians.css";

interface MusiciansProps {
  musicians: MusicianObj[];
  setMusicians: React.Dispatch<React.SetStateAction<MusicianObj[]>>;
  token: string;
}

function Musicians(props: MusiciansProps) {
  const [update, setUpdate] = useState<boolean>(false);
  const musicians = props.musicians;

  const handleBioChange = () => {
    setUpdate(!update);
  };
  const handleHeadshotChange = () => {
    setUpdate(!update);
  };

  const musicianList = musicians.map((musician) => (
    <Musician
      key={musician.id}
      musician={musician}
      onBioChange={handleBioChange}
      onHeadshotChange={handleHeadshotChange}
      token={props.token}
    />
  ));

  return (
    <section id="musicians">
      <Col>
        <Container>
          <h3 className="display-3 text-end musicians-title">
            Meet the Musicians
          </h3>
        </Container>
        {musicianList}
      </Col>
    </section>
  );
}

export default Musicians;
