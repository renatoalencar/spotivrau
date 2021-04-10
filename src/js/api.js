import {
  useState,
  useEffect,
  useRef,
} from "react";
import axios from "axios";

const client = axios.create({
  baseURL: "http://localhost:5000",
});

function addIndex(song, index) {
  return {
    ...song,
    index,
  }
}

export function useFetchSongs() {
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    client.get("/songs").then((response) => {
      setSongs(response.data.songs.map(addIndex));
    });
  }, []);

  return songs;
}

export function useWatchSong(songId, pollInterval = 500) {
  const [song, setSong] = useState(null);
  const interval = useRef(null);

  useEffect(() => {
    if (!songId) {
      return;
    }

    interval.current = setInterval(async () => {
      const response = await client.get("songs/" + songId);

      if (response.data.status === 'done') {
        cancel();
      }

      setSong(response.data);
    }, pollInterval);

    return cancel;
  }, [songId, pollInterval]);

  function cancel() {
    if (interval.current !== null) {
      clearInterval(interval.current);
      interval.current = null;
    }
  }

  return {
    song,
    cancel,
  };
}

function uploadSong(form, onProgress) {
  return client
    .post("transcode", new FormData(form), {
      onUploadProgress(uploadEvent) {
        onProgress(uploadEvent);
      },
    })
    .then((response) => response.data);
}

export function useCreateSong() {
  const [status, setStatus] = useState("idle");
  const [progress, setProgress] = useState(null);
  const [songId, setSongId] = useState(null);

  const { song, cancel } = useWatchSong(songId);

  async function upload(form) {
    setStatus("uploading");
    cancel();

    const { id } = await uploadSong(form, (uploadevent) => {
      setProgress(uploadevent);
    });

    setSongId(id);
  }

  useEffect(() => {
    setStatus(song !== null ? song.status : "idle");
  }, [song]);

  return {
    song,
    upload,
    status,
    progress,
  };
}
