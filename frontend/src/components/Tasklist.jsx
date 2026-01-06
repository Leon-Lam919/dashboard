import { useState } from "react"

const DISPLAY_NAME = {
  'keyboard': 'Keyboard Practice',
  'code': 'Coding',
  'workout': 'Workout',
  'cardio': 'Cardio'
}

function TaskList() {
  const [tasks, setTasks] = useState([
    { name: 'Coding', completed: false },
    { name: 'Workout', completed: false },
    { name: 'Keyboard Practice', completed: false },
    { name: 'Cardio', completed: false },
  ])

  const toggleTask = async (index) => {
    const list = [...tasks];
    list[index].completed = !list[index].completed;
    setTasks(list);
  }

  const getAll = async () => {
    const response = await fetch("http://localhost:8000/get_all")

    if (!response.ok) {
      console.error(await response.text())
      return []
    }

    const data = await response.json()

    return Object.entries(data).map(([name, status]) => ({
      id: name,
      name: formatDisplayName(name),
      completed: status?.toLowerCase() === 'yes'
    }))
  }

  getAll().then(tasks => console.log(tasks))


  const completedCount = tasks.filter(task => task.completed).length

  return (
    <div className="bg-gray-800 rounded-lg p-6 max-w-md">
      <h2 className="text-xl font-semibold mb-4">
        {new Date().toLocaleDateString('en-US', {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        })}
      </h2>

      <div className="space-y-3">
        {tasks.map((task, index) => (
          <div key={index} className="flex items-center gap-3 p-3 bg-gray-700 rounded">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => toggleTask(index)}
              className="w-5 h-5"
            />
            <span className="text-lg">{task.name}</span>
          </div>
        ))}
      </div>

      <div className="mt-6 pt-4 border-t border-gray-600">
        <p className="text-gray-400">
          Completion: {completedCount}/4
        </p>
      </div>
    </div>
  )
}

export default TaskList
