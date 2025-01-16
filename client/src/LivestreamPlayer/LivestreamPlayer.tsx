import { Container } from "react-bootstrap";

interface LivestreamPlayerProps {
  livestreamId: string;
}

const LivestreamPlayer = (props: LivestreamPlayerProps) => {
  const iframeSrc = `https://www.youtube.com/embed/${props.livestreamId}?autoplay=1`;

  return (
    <Container className="d-flex justify-content-center my-3">
      <div className="ratio ratio-16x9">
        <iframe
          src={iframeSrc}
          title="YouTube Livestream"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen"
          allowFullScreen
          className="rounded border"
        ></iframe>
      </div>
    </Container>
  );
};

export default LivestreamPlayer;
