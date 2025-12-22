import './index.css'
import TaskList from './components/Tasklist'

function App() {
  return (
    <div className='min-h-screen bg-gray-900 text-white p-8'>
      <h1 className='text-3xl font-bold mb-8'>Daily Dashboard</h1>
      <TaskList />
    </div>
  )
}

export default App
