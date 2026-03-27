import FilterBar from "./FilterBar.jsx"
import ArticleList from "./ArticleList.jsx"
import { SOURCE_COLORS } from "../../constants/sourcesColors.js"

import { useState, useEffect, useMemo } from "react"

function NewsWidget() {
  const [articles, setArticles] = useState([])
  const [activeSource, setActiveSource] = useState('all')
  const [sortOrder, setSortOrder] = useState('newest')

  console.log('NewsWidget mounted')

  useEffect(() => {
    console.log('fetching data')
    const loadData = async () => {
      const data = await newsFeed()
      console.log('data received:', data)
      setArticles(data)
    }
    loadData()
  }, [])

  const newsFeed = async () => {
    const response = await fetch("/api/news_feed")

    if (!response.ok) {
      console.error(await response.text())
      return []
    }

    const data = await response.json()
    return data
  };

  const filter = useMemo(() => {
    const filtered = articles.filter((article) => activeSource === 'all' || article.source === activeSource)
    console.log('activeSource:', activeSource)
    console.log('article.source sample:', articles[0]?.source)
    const sorted = filtered.sort((oldDate, newDate) => {
      return sortOrder === 'newest' ? new Date(oldDate.date) - new Date(newDate.date) : new Date(newDate.date) - new Date(oldDate.date)
    })

    return sorted
  }, [articles, activeSource, sortOrder]);

  const srcs = Object.keys(SOURCE_COLORS)

  console.log('filtered articles:', filter)

  return (
    <div>
      <FilterBar
        sources={srcs}
        activeSource={activeSource}
        sortOrder={sortOrder}
        onSourceChange={(source) => setActiveSource(source)}
        onSortChange={() => setSortOrder(sortOrder === 'newest' ? 'oldest' : 'newest')}
      />
      <ArticleList articles={filter} />
    </div>
  )
}
export default NewsWidget
