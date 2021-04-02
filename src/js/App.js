import {useState} from 'react'
import axios from 'axios'

function App() {
  const [progress, setProgress] = useState(0)

  async function handleSubmit(e) {
    const eventSource = new EventSource('http://localhost:8080/status')
    eventSource.onmessage = (e) => {
      const data = JSON.parse(e.data)

      console.log(data)

      if(data.type === 'progress') {
        setProgress(data.progress)
      }
    }

    const data = new FormData(e.target)

    await axios.post(
      'http://localhost:8080/transcode',
      data,
      {
        onUploadProgress(event) {
          setProgress(event.loaded / event.total)
        }
      }
    )
  }

  return (
    <form encType="multipart/form-data" onSubmit={(e) => {
      e.preventDefault()
      handleSubmit(e)
      return false
    }}>
      <i>{progress}</i>

      <input type="file" name="file" />

      <button type="submit">Send</button>
    </form>
  );
}

export default App;
