import {Link, BrowserRouter as Router, Switch, Route} from 'react-router-dom';

import {
  Player,
  PlayerProvider,
} from "./Player";
import {NewSong} from './NewSong'
import {NewArtist} from './NewArtist'
import {Song} from './Song'
import {useFetchSongs} from './api';
import "./App.css";

function Header() {
  return (
    <nav className="header">
      <ul>
        <li className="header__link">
          <Link to="/">Home</Link>
        </li>
        <li className="header__link">
          <Link to="/new-song">
            New song
          </Link>
        </li>
      </ul>
    </nav>
  )
}

function Playlist() {
  const songs = useFetchSongs();

  return (
    <>
      {songs.map((song, index) => (
        <Song key={song.id} index={index + 1} song={song} />
      ))}

      <Player playlistSongs={songs} />
    </>
  )
}

function App() {
  return (
    <PlayerProvider>
      <Router>
        <div className="app">
          <Header />
          <br />

          <Switch>
            <Route path="/new-song">
              <NewArtist />
            </Route>
            <Route path="/">
              <Playlist />
            </Route>
          </Switch>
        </div>
      </Router>
    </PlayerProvider>
  );
}
export default App;
