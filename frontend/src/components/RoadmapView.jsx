function RoadmapView({ roadmap, onBack }) {
  if (!roadmap) return null

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-3xl font-bold text-gray-800 mb-2">
              {roadmap.goal}
            </h2>
            <p className="text-gray-600">
              {roadmap.duration_weeks} week learning roadmap
            </p>
            <p className="text-sm text-gray-500 mt-1">
              Created: {new Date(roadmap.created_at).toLocaleDateString()}
            </p>
          </div>
          <button
            onClick={onBack}
            className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors"
          >
            ← Back
          </button>
        </div>

        {/* Success message */}
        <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-green-800">
            ✨ Your personalized roadmap has been generated successfully!
          </p>
        </div>

        <div className="space-y-4">
          {roadmap.week_plans.map((week) => (
            <div
              key={week.id}
              className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow bg-gradient-to-r from-white to-blue-50"
            >
              <div className="flex items-center mb-3">
                <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-semibold mr-3">
                  Week {week.week_number}
                </span>
                <h3 className="text-xl font-semibold text-gray-800">
                  {week.focus_title}
                </h3>
              </div>

              <div className="mb-4">
                <h4 className="text-sm font-semibold text-gray-700 mb-2">📚 Topics:</h4>
                <ul className="list-disc list-inside space-y-1">
                  {week.topics_json.map((topic, idx) => (
                    <li key={idx} className="text-gray-600">{topic}</li>
                  ))}
                </ul>
              </div>

              <div className="mb-4">
                <h4 className="text-sm font-semibold text-gray-700 mb-2">✅ Practice Tasks:</h4>
                <ul className="list-disc list-inside space-y-1">
                  {week.tasks_json.map((task, idx) => (
                    <li key={idx} className="text-gray-600">{task}</li>
                  ))}
                </ul>
              </div>

              <div className="flex items-center text-sm">
                <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full font-medium">
                  🎯 Target: {week.target_problems} problems
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default RoadmapView
