import ArticleCard from "./ArticleCard"

function ArticleList({ articles }) {
  const arr = articles.map(article =>
    <div key={article.link}>
      <ArticleCard {...article} /></div>)

  return <div className="justify-items-start">{arr}</div>
}

export default ArticleList
