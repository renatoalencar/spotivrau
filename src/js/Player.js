import {
  useState,
  useReducer,
  useEffect,
  useRef,
  useContext,
  createContext,
  useCallback,
} from "react";

import PlayerContainer from './PlayerContainer';

function playerState(state, action) {
  switch (action.type) {
    case "settime":
      return {
        ...state,
        ignoreSubsequentUpdates: action.ignoreSubsequentUpdates,
        currentTime: action.time,
      };
    case "timeupdate":
      const newCurrentTime = Math.floor(action.event.target.currentTime);

      /* We don't need the fractional part (less than one second)
         so we return the same state reference in order to React
         to bail out this update and avoid rerendering. If we build
         another object using the spread operator it wont happen
         since it would be another reference. */
      if (
        state.currentTime === newCurrentTime ||
        state.ignoreSubsequentUpdates
      ) {
        return state;
      }

      return {
        ...state,
        currentTime: newCurrentTime,
      };
    case "durationchange":
      return {
        ...state,
        duration: Math.floor(action.event.target.duration),
      };
    case "play":
      return {
        ...state,
        state: "playing",
      };
    case "pause":
      return {
        ...state,
        state: "paused",
      };
    case "volume":
      return {
        ...state,
        volume: action.event.target.volume,
      };
    case "togglemuted": {
      return {
        ...state,
        muted: !state.muted,
      };
    }
    default:
      return state;
  }
}

function throttle(fn, timeout) {
  let called = false;
  return function () {
    if (!called) {
      fn.apply(this, arguments);
      called = true;
      setTimeout(() => {
        called = false;
      }, timeout);
    }
  };
}

function debounce(fn, time) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      fn.apply(this, args);
    }, time);
  };
}

function usePlayerImpl() {
  const audio = useRef(new Audio());
  const [song, setSong] = useState(null);
  const [state, dispatch] = useReducer(playerState, { volume: 1.0 });

  const setCurrentTime = useCallback(
    debounce((time) => {
      dispatch({
        type: "settime",
        ignoreSubsequentUpdates: false,
        time,
      });
      audio.current.currentTime = time;
    }, 500),
    []
  );

  function seek(time) {
    dispatch({
      type: "settime",
      ignoreSubsequentUpdates: true,
      time,
    });
    setCurrentTime(time);
  }

  useEffect(() => {
    if (audio.current === null) {
      return;
    }

    if (song === null) {
      audio.current.src = null;
      return;
    }

    audio.current.src = "/media/" + song.song;
    audio.current.play();
  }, [song]);

  useEffect(() => {
    audio.current.addEventListener(
      "timeupdate",
      /* timeupdate is called on the millisecond space,
         so we need to avoid filling React's updated queue
         with useless updates and so avoid dropping frames. */
      throttle((event) => {
        dispatch({
          type: "timeupdate",
          event,
        });
      }, 16)
    );

    audio.current.addEventListener("durationchange", (event) => {
      dispatch({
        type: "durationchange",
        event,
      });
    });

    audio.current.addEventListener("play", (event) => {
      dispatch({
        type: "play",
        event,
      });
    });

    audio.current.addEventListener("pause", (event) => {
      dispatch({
        type: "pause",
        event,
      });
    });

    audio.current.addEventListener("volumechange", (event) => {
      dispatch({
        type: "volume",
        event,
      });
    });
  }, []);

  return {
    audio: audio.current,
    song,
    state,
    playSong(song) {
      setSong(song);
    },
    play() {
      audio.current.play();
    },
    pause() {
      audio.current.pause();
    },
    seek,
    setVolume(volume) {
      audio.current.volume = volume;
    },
    toggleMute() {
      dispatch({
        type: "togglemuted",
      });

      audio.current.muted = !state.muted
    },
  };
}

export function togglePlay(player) {
  player.audio.paused ? player.play() : player.pause();
}

export function togglePlayOrReplace(player, song) {
  if (player.song && player.song.id === song.id) {
    togglePlay(player);
    return;
  }

  player.playSong(song);
}

const PlayerContext = createContext(null);

export function usePlayer() {
  return useContext(PlayerContext);
}

export function PlayerProvider({ children }) {
  const player = usePlayerImpl();

  return (
    <PlayerContext.Provider value={player}>{children}</PlayerContext.Provider>
  );
}

function usePlaylist(songs) {
  const player = usePlayer();

  const currentPlayingSong = player.song

  return {
    next() {
      if (currentPlayingSong.index >= songs.length - 1) {
        return
      }

      togglePlayOrReplace(player, songs[currentPlayingSong.index + 1])
    },
    previous() {
      if (currentPlayingSong.index <= 0) {
        return
      }

      togglePlayOrReplace(player, songs[currentPlayingSong.index - 1])
    },
    hasNext: currentPlayingSong && currentPlayingSong.index >= songs.length,
    hasPrevious: currentPlayingSong && currentPlayingSong.index === 0,
  }
}

export function Player({ playlistSongs }) {
  const player = usePlayer();
  const playlist = usePlaylist(playlistSongs);

  return (
    <PlayerContainer
      player={player}
      onSeek={(e) => {
        player.seek(e.target.value);
      }}
      onVolume={(e) => {
        player.setVolume(e.target.value);
      }}
      onMute={() => {
        player.toggleMute();
      }}
      onPrevious={() => {
        playlist.previous();
      }}
      onNext={() => {
        playlist.next();
      }}
      onPlay={() => {
        togglePlay(player);
      }}
    />
  );
}
