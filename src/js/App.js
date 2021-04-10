import { useState } from "react";

import {
  Player,
  PlayerProvider,
} from "./Player";
import {NewSong} from './NewSong'
import {Song} from './Song'
import {useFetchSongs} from './api';
import "./App.css";

function App() {
  const songs = useFetchSongs();
  const [newSong, setNewSong] = useState(false);

  function handleNewSong() {
    setNewSong(true);
  }

  return (
    <PlayerProvider>
      <div className="app">
        {songs.map((song, index) => (
          <Song key={song.id} index={index + 1} song={song} />
        ))}

        <br />

        {newSong ? (
          <NewSong />
        ) : (
          <button className="primary-button" onClick={handleNewSong}>
            New song
          </button>
        )}

        <Player playlistSongs={songs} />
      </div>
    </PlayerProvider>
  );
}
export default App;
