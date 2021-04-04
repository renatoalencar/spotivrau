import {useCreateSong} from './api'
import {Song} from './Song'

import './NewSong.css'

function Progress(props) {
  return <progress className="progress-primary" {...props} />;
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

function UploadForm({ onSubmit }) {
  return (
    <form encType="multipart/form-data" onSubmit={onSubmit}>
      <h1>Upload a new song</h1>
      <Input type="text" name="name" label="Song name" />
      <Input type="file" name="cover" label="Song cover" />
      <Input type="file" name="file" label="Song media" />

      <button className="primary-button" type="submit">
        Send
      </button>
    </form>
  );
}

function SongStatusReport({ status, progress }) {
  const classes = ["song-report"];

  if (status === "done") {
    classes.push("song-report--done");
  }

  return (
    <div className={classes.join(" ")}>
      <p className="song_report__status">{status}</p>
      {progress !== null && (
        <Progress value={progress.loaded} max={progress.total} />
      )}
    </div>
  );
}

export function NewSong() {
  const { song, upload, status, progress } = useCreateSong();

  function handleSubmit(e) {
    e.preventDefault();
    upload(e.target);

    return false;
  }

  return (
    <div>
      {status === "done" && <Song song={song} />}
      {status !== "idle" && (
        <SongStatusReport status={status} progress={progress} />
      )}
      {status === "idle" && <UploadForm onSubmit={handleSubmit} />}
    </div>
  );
}
