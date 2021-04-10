import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlay, faPause } from "@fortawesome/free-solid-svg-icons";

import './Song.css'

import {
  usePlayer,
  togglePlayOrReplace,
} from "./Player";
import {formatTime} from './time'

export function Song({ index, song }) {
  const player = usePlayer();

  const isCurrentSong = player.song && player.song.id === song.id
  const playing = player.state.state === "playing" && isCurrentSong

  const classes = ['player']

  if (playing) {
    classes.push('player--playing')
  }

  if (isCurrentSong) {
    classes.push('player--current-song')
  }

  return (
    <div className={classes.join(' ')}>
      <span className="player__index-number">
        {index}
      </span>
      <button
        className="player__button player__button--outline"
        onClick={() => togglePlayOrReplace(player, song)}
      >
        <FontAwesomeIcon
          icon={
            playing
              ? faPause
              : faPlay
          }
        />
      </button>

      <img className="player__song-cover" src={'/media/' + song.cover} />

      <div className="player__info">
        <div className="player__info__title-and-artist">
          <h3 className="player__song-title">{song.name}</h3>
          <p className="player__song-artist">{song.artist}</p>
        </div>

        <span className="player__duration">
          {formatTime(song.duration)}
        </span>
      </div>
    </div>
  );
}
