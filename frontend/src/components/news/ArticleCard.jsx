import { SOURCE_COLORS, DEFAULT_COLOR } from '../../constants/sourcesColors'
function ArticleCard({ title, description, source, link }) {

  return (
    <div className="pb-4">
      <div className="border-4 border-gray-600 rounded-lg p-4 mb-0 max-w-xs">
        < a href={link} target='_blank' rel='noopener noreferrer'>
          <span className={`${SOURCE_COLORS[source] || DEFAULT_COLOR} rounded-md px-1 py-0.5 border border-gray-600`}>{source}</span>
          <h3 className=''>{title}</h3>
          <p>{description}</p>
        </a >
      </div>
    </div>
  )
}

export default ArticleCard
