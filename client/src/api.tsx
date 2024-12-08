import axios from "axios";
import { GroupObj } from "./Group/Group";
import { MusicianObj } from "./Musicians/Musician/Musician";
import { EventSeriesObj } from "./Series/SeriesList";
import { EventObj } from "./Series/Events.tsx/Event/Event";
import { UserObj } from "./Auth/User";

const baseURL = import.meta.env.VITE_API_URL as string;

class TheGrapefruitsDuoAPI {
  version: string;
  group: GroupObj;
  musicians: MusicianObj[];
  events: EventSeriesObj[];

  constructor(
    version: string,
    group: GroupObj,
    musicians: MusicianObj[],
    events: EventSeriesObj[],
  ) {
    this.version = version;
    this.group = group;
    this.musicians = musicians;
    this.events = events;
  }
}

const api = axios.create({
  baseURL: baseURL,
});

export const getRoot = async (): Promise<TheGrapefruitsDuoAPI> => {
  const response = await api.get("/");
  const tgd = new TheGrapefruitsDuoAPI(
    response.data.version,
    new GroupObj(
      response.data.group.id,
      response.data.group.name,
      response.data.group.bio,
    ),
    response.data.musicians.map(
      (musician: MusicianObj) =>
        new MusicianObj(
          musician.id,
          musician.name,
          musician.bio,
          musician.headshot_id,
        ),
    ),
    response.data.events.map(
      (series: EventSeriesObj) =>
        new EventSeriesObj(
          series.series_id,
          series.name,
          series.description,
          series.events.map(
            (event: EventObj) =>
              new EventObj(
                event.event_id,
                event.location,
                event.time,
                event.ticket_url,
                event.map_url,
              ),
          ),
          series.poster_id,
        ),
    ),
  );
  return tgd;
};

export const getUsers = async (): Promise<EventObj[]> => {
  const response = await api.get("/users/");
  return response.data.map(
    (user: UserObj) => new UserObj(user.name, user.email, user.id, user.sub),
  );
};

export const getUser = async (id: number): Promise<UserObj> => {
  const response = await api.get(`/users/${id}/`);
  return new UserObj(
    response.data.name,
    response.data.email,
    response.data.id,
    response.data.sub,
  );
};

export const postUser = async (token: string): Promise<UserObj> => {
  const response = await api.post(
    "/users/",
    {},
    { headers: { Authorization: `Bearer ${token}` } },
  );
  return new UserObj(
    response.data.name,
    response.data.email,
    response.data.id,
    response.data.sub,
  );
};

export const getGroup = async (): Promise<GroupObj> => {
  const response = await api.get("/group/");
  return new GroupObj(response.data.id, response.data.name, response.data.bio);
};

export const getMusicians = async (): Promise<MusicianObj[]> => {
  const response = await api.get("/musicians/");
  return response.data.map(
    (musician: MusicianObj) =>
      new MusicianObj(
        musician.id,
        musician.name,
        musician.bio,
        musician.headshot_id,
      ),
  );
};

export const patchMusician = async (
  id: number,
  bio: string,
  name: string,
  headshot_id: string,
  user_token: string,
): Promise<MusicianObj> => {
  const response = await api.patch(
    `/musicians/${id}/`,
    { id, bio, name, headshot_id },
    { headers: { Authorization: `Bearer ${user_token}` } },
  );
  return new MusicianObj(
    response.data.id,
    response.data.name,
    response.data.bio,
    response.data.headshot_id,
  );
};

export const patchGroup = async (
  id: number,
  bio: string,
  name: string,
  user_token: string,
): Promise<GroupObj> => {
  const response = await api.patch(
    `/group/`,
    { id, bio, name },
    { headers: { Authorization: `Bearer ${user_token}` } },
  );
  return new GroupObj(response.data.id, response.data.name, response.data.bio);
};

export const postHeadshot = async (
  id: number,
  file: File,
  user_token: string,
): Promise<MusicianObj> => {
  const formData = new FormData();
  formData.append("file", file);
  const response = await api.post(`/musicians/${id}/headshot`, formData, {
    headers: { Authorization: `Bearer ${user_token}` },
  });
  return new MusicianObj(
    response.data.id,
    response.data.name,
    response.data.bio,
    response.data.headshot_id,
  );
};

export const postMessage = async (
  name: string,
  email: string,
  message: string,
): Promise<void> => {
  await api.post("/contact/", { name, email, message });
  return;
};

export const postSeriesPoster = async (
  series_id: number,
  poster: File,
  user_token: string,
): Promise<EventSeriesObj> => {
  const formData = new FormData();
  formData.append("poster", poster);
  const response = await api.post(`/events/${series_id}/poster`, formData, {
    headers: { Authorization: `Bearer ${user_token}` },
  });
  return new EventSeriesObj(
    response.data.series_id,
    response.data.name,
    response.data.description,
    response.data.events.map(
      (event: EventObj) =>
        new EventObj(
          event.event_id,
          event.location,
          event.time,
          event.ticket_url,
          event.map_url,
        ),
    ),
    response.data.poster_id,
  );
};

export const getSeriesList = async (): Promise<EventSeriesObj[]> => {
  const response = await api.get("/events/");
  return response.data.map(
    (series: EventSeriesObj) =>
      new EventSeriesObj(
        series.series_id,
        series.name,
        series.description,
        series.events.map(
          (event: EventObj) =>
            new EventObj(
              event.event_id,
              event.location,
              event.time,
              event.ticket_url,
              event.map_url,
            ),
        ),
        series.poster_id,
      ),
  );
};

export const postSeries = async (
  series: EventSeriesObj,
  user_token: string,
): Promise<EventSeriesObj> => {
  const response = await api.post("/events/", series, {
    headers: { Authorization: `Bearer ${user_token}` },
  });
  return new EventSeriesObj(
    response.data.series_id,
    response.data.name,
    response.data.description,
    response.data.events.map(
      (event: EventObj) =>
        new EventObj(
          event.event_id,
          event.location,
          event.time,
          event.ticket_url,
          event.map_url,
        ),
    ),
    response.data.poster_id,
  );
};
export const deleteSeries = async (
  series_id: number,
  user_token: string,
): Promise<void> => {
  await api.delete(`/events/${series_id}/`, {
    headers: { Authorization: `Bearer ${user_token}` },
  });
  return;
};

export const putSeries = async (
  series: EventSeriesObj,
  user_token: string,
): Promise<EventSeriesObj> => {
  const response = await api.put(`/events/${series.series_id}/`, series, {
    headers: { Authorization: `Bearer ${user_token}` },
  });
  return new EventSeriesObj(
    response.data.series_id,
    response.data.name,
    response.data.description,
    response.data.events.map(
      (event: EventObj) =>
        new EventObj(
          event.event_id,
          event.location,
          event.time,
          event.ticket_url,
          event.map_url,
        ),
    ),
    response.data.poster_id,
  );
};
