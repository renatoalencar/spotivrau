import {useMemo, useState} from 'react'
import Fuse from 'fuse.js'
import {useArtists} from './api'

function useSearch() {
  const artists = useArtists()
  const fuse = useMemo(
    () => new Fuse(artists, {
      includeScore: true,
      keys: ['name'],
    }),
    [artists]
  )

  const [filtered, setFiltered] = useState([])

  return {
    artists: filtered,
    search(query) {
      const result = fuse.search(query)

      setFiltered(result)
    }
  }
}

export function NewArtist() {
  const {artists, search} = useSearch()

  function handleChange(e) {
    search(e.target.value)
  }

  return (
    <>
      <input className="input" placeholder="Search..." onChange={handleChange} />
      {artists.map(a => <b key={a.item.id}>{a.item.name}</b>)}
    </>
  )
}