import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faPlay,
  faPause,
  faVolumeUp,
  faVolumeDown,
  faVolumeOff,
  faVolumeMute,
  faStepForward,
  faStepBackward,
} from "@fortawesome/free-solid-svg-icons";

import "./Player.css";
import { formatTime } from "./time";

function getVolumeIcon(volume, muted) {
  if (muted) {
    return faVolumeMute;
  }

  if (volume === 0) {
    return faVolumeOff;
  }

  if (volume < 0.5) {
    return faVolumeDown;
  }

  return faVolumeUp;
}

function IconButton({ icon, outline, onClick}) {
  const classes = ['global-player__round-button']

  if (outline) {
    classes.push('global-player__round-button--outline')
  }

  return (
    <button
      className={classes.join(' ')}
      onClick={onClick}
    >
      <FontAwesomeIcon icon={icon} />
    </button>
  )
}

function Time({ children }) {
  return (
    <span className="global-player__controls__time">
      {formatTime(children)}
    </span>
  )
}

export default function Player({ player, onSeek, onVolume, onMute, onPrevious, onNext, onPlay }) {
  if (player.song === null) {
    return null;
  }

  return (
    <div className="global-player">
      <div className="global-player__info">
        <img className="global-player__cover" src={"/media/" + player.song.cover} />

        <div className="global-player__info-column">
          <h2 className="global-player__song-title">
            {player.song.name}
          </h2>

          <p className="global-player__song-artist">{player.song.artist}</p>
        </div>
      </div>


      <div className="global-player__controls">
        <div className="global-player__controls__playback-control">
          <IconButton icon={faStepBackward} onClick={onPrevious} outline />

          <IconButton
            icon={player.state.state === "playing" ? faPause : faPlay}
            onClick={onPlay}
          />

          <IconButton icon={faStepForward} onClick={onNext} outline />
        </div>

        <div className="global-player__progress-container">
          <Time>{player.state.currentTime}</Time>

          <input
            type="range"
            className="global-player__progress-container__time-control"
            value={player.state.currentTime}
            max={player.state.duration}
            onChange={onSeek}
          />

          <Time>{player.state.duration}</Time>
        </div>
      </div>

      <div className="global-player__volume-container">
        <IconButton
          icon={getVolumeIcon(player.state.volume, player.state.muted)}
          onClick={onMute}
          outline
        />

        <input
          type="range"
          className="global-player__volume"
          value={player.state.volume}
          max={1}
          step={0.01}
          onChange={onVolume}
        />
      </div>
    </div>
  );
}
