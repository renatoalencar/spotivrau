import {useState, useEffect} from 'react'
import axios from 'axios'

function Song({ song }) {
  return (
    <div>
      <p><b>{song.name}</b></p>
      <p><img src={`/media/${song.waveform}`} /></p>
      <p><audio controls src={`/media/${song.song}`} /></p>
    </div>
  )
}


function App() {
  const [progress, setProgress] = useState(0)
  const [songId, setSongId] = useState(null)
  const [song, setSong] = useState(null)

  useEffect(() => {
    if (!songId) {
      return
    }

    const interval = setTimeout(() => {
      axios.get('http://localhost:5000/songs/' + songId)
        .then(response => {
          setSong(response.data)
        })
    }, 5000)
  }, [songId])

  function handleSubmit(e) {
    e.preventDefault()

    axios.post('http://localhost:5000/transcode', new FormData(e.target), {
      onUploadProgress(uploadEvent) {
        setProgress(Math.floor(uploadEvent.loaded * 100 / uploadEvent.total))
      }
    }).then(response => {
      setSongId(response.data.id)
    })

    return false
  }

  return (
    <form encType="multipart/form-data" onSubmit={handleSubmit}>
      <i>{songId}</i> {' '}
      <i>{progress}</i>

      {song && <Song song={song} />}

      <p>
        <input type="text" name="name" />
      </p>
      <p>
        <input type="file" name="file" />
      </p>

      <button type="submit">Send</button>
    </form>
  );
}

export default App;
