import { Container, Row } from "react-bootstrap";
import cld from "../../Cld/CloudinaryConfig";
import "./Musician.css";
import Headshot from "./Headshot/Headshot";
import MusicianBio from "./Bio/Bio";
import { useState } from "react";

export class MusicianObj {
  id: number;
  name: string;
  bio: string;
  headshot_id: string;

  constructor(id: number, name: string, bio: string, headshot_id: string) {
    this.id = id;
    this.name = name;
    this.bio = bio;
    this.headshot_id = headshot_id;
  }
}

export interface MusicianProps {
  musician: MusicianObj;
  onBioChange: () => void;
  onHeadshotChange?: () => void;
  token: string;
}

function Musician(props: MusicianProps) {
  const [musician, setMusician] = useState<MusicianObj>(props.musician);
  const textPosition = musician.id % 2 === 0 ? "text-end" : "text-start";
  const image = cld.image(musician.headshot_id);
  const imgUrl = image.toURL();
  const musicianID = musician.name.split(" ").join("-").toLowerCase();
  const key = `musician-${musician.id}`;

  const bioCard = (
    <MusicianBio
      key={key}
      musician={musician}
      textPosition={textPosition}
      onBioChange={props.onBioChange}
      setMusician={setMusician}
      token={props.token}
    />
  );

  const headshot = (
    <Headshot
      src={imgUrl}
      key="headshot"
      musician={musician}
      onHeadshotChange={props?.onHeadshotChange}
      setMusician={setMusician}
      token={props.token}
    />
  );

  return (
    <Container id={musicianID} className="musician-container">
      <Row className="row-spacing">
        {musician.id % 2 === 0 ? [bioCard, headshot] : [headshot, bioCard]}
      </Row>
    </Container>
  );
}

export default Musician;
