import './index.css'
import TaskList from './components/Tasklist'
import NewsWidget from './components/news/NewsWidget'

function App() {
  return (
    <div className='min-h-screen bg-gray-900 text-white p-8'>
      <h1 className='text-3xl font-bold mb-8'>Daily Dashboard</h1>
      <TaskList />
      <NewsWidget />
    </div>
  )
}

export default App
