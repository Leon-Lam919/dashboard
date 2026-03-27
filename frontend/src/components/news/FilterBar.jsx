function FilterBar({ sources, activeSource, sortOrder, onSourceChange, onSortChange }) {
  const src = sources.map(source =>
    <button
      key={source}
      onClick={() => onSourceChange(source)}
      className={` ml-2 ${source === activeSource ? 'bg-sky-300' : 'bg-sky-950'}`}
    >
      {source}
    </button>
  )

  return (
    <div>
      {src}
      <button onClick={() => onSortChange()}
        className="ml-2">
        {sortOrder === 'newest' ? 'newest' : 'oldest'}
      </button>
    </div >
  )
}


export default FilterBar
