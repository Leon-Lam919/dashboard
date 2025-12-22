import { useState } from "react"

function TaskList() {
  const [tasks, setTasks] = useState([
    { name: 'Coding', completed: false },
    { name: 'Workout', completed: false },
    { name: 'Keyboard Practice', completed: false },
  ])

  const toggleTask = (index) => {
    const list = [...tasks];
    list[index].completed = !list[index].completed;
    setTasks(list);
  }

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
          Completion: {completedCount}/3
        </p>
      </div>
    </div>
  )
}

export default TaskList
