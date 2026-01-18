import { useState, useEffect } from "react"
import Checkbox from '@mui/joy/Checkbox';


const DISPLAY_NAME = {
  'keyboard': 'Keyboard Practice',
  'code': 'Coding',
  'workout': 'Workout',
  'cardio': 'Cardio'
}

function TaskList() {
  const [tasks, setTasks] = useState([])
  const [tempList, setTempList] = useState([])

  // use effect calls this function on mount (refesh, new tab opening, etc.)
  useEffect(() => {
    const loadData = async () => {
      const data = await getAll()
      setTasks(data)
    }
    loadData()
  }, [])

  //const temp = async()


  const getAll = async () => {
    const response = await fetch("http://localhost:8000/get_all")

    if (!response.ok) {
      console.error(await response.text())
      return []
    }

    const data = await response.json()

    // turns the JSON into an object that
    return Object.entries(data).map(([name, status]) => ({
      id: name,
      completed: status?.toLowerCase() === 'yes'
    }))
  }

  // Uses the current tasks in state and toggle one of them
  // newList is a new array, but its items reference the same task objects, so changing a task mutates previous state.
  // newList mutates the existing list
  // is called every time box is checked or unchecked
  // setTasks replaces the state with a new snapshot
  const toggleTask = async (index) => {
    const newList = [...tasks]
    newList[index].completed = !newList[index].completed;
    setTasks(newList);
    const id = newList[index].id;
    const completed = newList[index].completed;
    const response = await fetch(`http://localhost:8000/tasks/${id}`,
      {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          task_id: id,
          status: completed ? "yes" : "no"
        })
      });

    if (!response.ok) {
      console.error(await response.text())
      return []
    }

    const data = await response.json()
    console.log("This is what the PUT call returned: ", data)

  }

  const count = Object.keys(tasks).length;
  const completedCount = tasks.filter(task => task.completed).length

  return (
    <div className="bg-gray-800 rounded-lg p-6 max-w-xs">
      <h2 className="text-xl font-semibold mb-4">
        {new Date().toLocaleDateString('en-US', {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        })}
      </h2>

      <div className="space-y-0">
        {tasks.map((task, index) => (
          <div key={index} className="flex items-center gap-3 p-2">
            {/* Put this shit into a Box class instead of checkbox */}
            <Checkbox
              className="pb-2"
              label={task.id}
              checked={task.completed}
              onChange={() => toggleTask(index)}
              size="md"
              variant="outlined"
              sx={{
                // UNCHECKED state

                "--Checkbox-gap": "0.5rem",

                "--Checkbox-radius": "6px",

                "& .MuiCheckbox-label": {
                  color: "#6bf890",
                  fontSize: "2 rem",
                  fontWeight: 100,
                },

                "&.Mui-checked .MuiCheckbox-label": {
                  color: "#16a34a",
                  fontSize: "1 rem",
                  textDecoration: task.completed ? "line-through" : "none",
                  opacity: task.completed ? 0.6 : 1,
                },

                "& .MuiCheckbox-checkbox": {
                  borderColor: "#86efac",     // light green border
                  backgroundColor: "transparent",
                },

                // CHECKED state
                "&.Mui-checked .MuiCheckbox-checkbox": {
                  borderColor: "#22c55e",     // darker green
                  backgroundColor: "#22c55e", // filled green
                  color: "#ffffff",           // checkmark color
                },

                transition: "all 0.2s ease",
              }}
            >
            </Checkbox>
          </div>
        ))}
        <div className="mt-6 pt-6 border-t border-gray-600">
          <form>
            <label>Task: </label>
            <input className="bg-gray-600" type="text" />
          </form>

        </div>
      </div>

      <div className="mt-6 pt-4 border-t border-gray-600">
        <p className="text-gray-400">
          Completion: {completedCount}/{count}
        </p>
      </div>
    </div>



  )
}

export default TaskList
