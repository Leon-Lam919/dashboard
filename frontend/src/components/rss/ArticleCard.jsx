import
  function ArticleCard({ title, description, source, link }) {

    return (
      < a >
        <span>{source}</span>
        <h3>{title}</h3>
        <p>{description}</p>

      </a >
    )
  }

export default ArticleCard
