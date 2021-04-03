import { useState, useEffect, useRef } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlay, faPause } from '@fortawesome/free-solid-svg-icons'
import axios from "axios";

import "./App.css";

const client = axios.create({
  baseURL: "http://localhost:5000"
});

function uploadSong(form, onProgress) {
  return client.post("transcode", new FormData(form), {
    onUploadProgress(uploadEvent) {
      onProgress(uploadEvent);
    },
  }).then(response => response.data);
}

function Progress(props) {
  return <progress className="progress-primary" {...props}/>
}

function Input({ label, type, placeholder, name }) {
  return (
    <div className="input">
      <label className="input__label">{label}</label>
      <input
        className="input__input"
        type={type}
        placeholder={placeholder}
        name={name}
      />
    </div>
  );
}

function Player({ song }) {
  const audio = useRef(null)
  const [duration, setDuration] = useState(0);
  const [progress, setProgress] = useState(0);

  function handleProgress(target) {
    setDuration(target.duration)
    setProgress(target.currentTime)
  }

  useEffect(() => {
    const interval = setInterval(() => {
      if (audio.current !== null) {
        handleProgress(audio.current)
      }
    }, 16)

    return () => clearInterval(interval)
  }, [audio.current])

  function togglePlay() {
    audio.current.paused ? audio.current.play() : audio.current.pause()
  }

  return (
    <div className="player">
        <img className="player__waveform" src={`/media/${song.waveform}`} />

        <div className="player__controls">
          <button class="player__button player__button--outline" onClick={togglePlay}>
            <FontAwesomeIcon icon={audio.current && !audio.current.paused ? faPause : faPlay} />
          </button>

          <div className="player__column">
            <h2 className="player__song-title">{song.name}</h2>

            <Progress value={progress} max={duration} />
          </div>
        </div>

        <audio ref={audio} src={`/media/${song.song}`} />
    </div>
  );
}

function UploadForm({ onSubmit }) {
  return (
    <form encType="multipart/form-data" onSubmit={onSubmit}>
      <h1>Upload a new song</h1>
      <Input type="text" name="name" label="Song name" />
      <Input type="file" name="file" label="Song media" />

      <button className="primary-button" type="submit">
        Send
      </button>
    </form>
  );
}

function SongStatusReport({ status, progress }) {
  const classes = ['song-report']

  if (status === 'done') {
    classes.push('song-report--done')
  }

  return (
    <div className={classes.join(' ')}>
      <p className="song_report__status">{status}</p>
      {progress !== null && <Progress value={progress.loaded} max={progress.total}/>}
    </div>
  )
}

function useWatchSong(songId, pollInterval = 500) {
  const [song, setSong] = useState(null);

  let interval = null;

  useEffect(() => {
    if (!songId) {
      return;
    }

    interval = setInterval(async () => {
      const response = await client.get("songs/" + songId);

      setSong(response.data);
    }, pollInterval);

    return cancel;
  }, [songId]);

  function cancel() {
    if (interval !== null) {
      clearInterval(interval);
      interval = null;
    }
  }

  return {
    song,
    cancel,
  };
}

function useCreateSong() {
  const [status, setStatus] = useState('idle')
  const [progress, setProgress] = useState(null);
  const [songId, setSongId] = useState(null);

  const { song, cancel } = useWatchSong(songId)

  async function upload(form) {
    setStatus('uploading')
    cancel()

    const { id } = await uploadSong(form, (uploadevent) => {
      setProgress(uploadevent)
    })

    setSongId(id)
  }

  useEffect(() => {
    setStatus(song !== null ? song.status : 'idle')
  }, [song])

  return {
    song,
    upload,
    status,
    progress,
  }
}

function App() {
  const {song, upload, status, progress} = useCreateSong()

  function handleSubmit(e) {
    e.preventDefault();
    upload(e.target);

    return false;
  }

  return (
    <div className="app">
      {status === 'done' && <Player song={song} />}
      {status !== 'idle' && <SongStatusReport status={status} progress={progress} />}
      {status === 'idle' && <UploadForm onSubmit={handleSubmit} />}
    </div>
  );
}

export default App;
