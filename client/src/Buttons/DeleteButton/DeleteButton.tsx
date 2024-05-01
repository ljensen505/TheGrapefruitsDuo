import { Button } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash } from "@fortawesome/free-solid-svg-icons";
import { deleteSeries } from "../../api";
import "./DeleteButton.css";
import { EventSeriesObj } from "../../Series/SeriesList";

interface DeleteButtonProps {
  series: EventSeriesObj;
  setSeriesList: React.Dispatch<React.SetStateAction<EventSeriesObj[]>>;
  seriesList: EventSeriesObj[];
  actionName?: string;
  token: string;
}

function DeleteButton(props: DeleteButtonProps) {
  const handleDelete = () => {
    console.log(props.series.series_id);
    deleteSeries(props.series.series_id, props.token)
      .then(() => {
        props.setSeriesList(
          props.seriesList.filter(
            (series) => series.series_id !== props.series.series_id,
          ),
        );
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <Button className="delete-icon btn-delete" onClick={handleDelete}>
      <FontAwesomeIcon icon={faTrash} />
      {props.actionName}
    </Button>
  );
}

export default DeleteButton;
