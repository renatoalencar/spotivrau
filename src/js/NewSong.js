import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCamera
} from "@fortawesome/free-solid-svg-icons";

import {useCreateSong} from './api'
import {Song} from './Song'

import './NewSong.css'

function Progress(props) {
  return <progress className="progress-primary" {...props} />;
}

function Input({ id, className, label, type, placeholder, name }) {
  const classes = ['input']

  if (className) {
    classes.push(className)
  }

  return (
    <div className={classes.join(' ')}>
      <label for={id} className="input__label">{label}</label>
      <input
        id={id}
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
    <form className="upload-form" encType="multipart/form-data" onSubmit={onSubmit}>
      <h2>Upload a new song</h2>

      <div className="upload-form__row">
        <Input
          id="upload-form-cover-input"
          className="upload-form__cover"
          type="file"
          name="cover"
          label={
            <>
              Song cover {' '}
              <FontAwesomeIcon icon={faCamera} />
            </>
          }
        />

        <div className="upload-form__column">
          <Input type="text" name="name" label="Song name" />
          <Input type="text" name="artist" label="Song artist" />
          <Input type="file" name="file" label="Song media" />
        </div>
      </div>

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
