import { useState, useEffect } from 'react'
import axios from 'axios'

function SharedRoadmap({ publicId }) {
  const [roadmap, setRoadmap] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchSharedRoadmap()
  }, [publicId])

  const fetchSharedRoadmap = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/share/${publicId}`)
      setRoadmap(response.data)
      setLoading(false)
    } catch (err) {
      setError('Roadmap not found or link is invalid')
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading shared roadmap...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md">
          <div className="text-red-600 text-5xl mb-4 text-center">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center">Roadmap Not Found</h2>
          <p className="text-gray-600 text-center mb-6">{error}</p>
          <a
            href="/"
            className="block w-full bg-blue-600 text-white py-3 rounded-lg text-center font-semibold hover:bg-blue-700 transition-colors"
          >
            Create Your Own Roadmap
          </a>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-6">
          <div className="text-center mb-6">
            <div className="inline-block bg-blue-100 text-blue-600 px-4 py-2 rounded-full text-sm font-semibold mb-4">
              📤 Shared Roadmap
            </div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">
              {roadmap.goal}
            </h1>
            <p className="text-gray-600">
              {roadmap.duration_weeks} week learning roadmap
            </p>
            <p className="text-sm text-gray-500 mt-2">
              Created: {new Date(roadmap.created_at).toLocaleDateString()}
            </p>
          </div>

          <div className="border-t pt-6">
            <a
              href="/"
              className="block w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 rounded-lg text-center font-semibold hover:from-blue-700 hover:to-indigo-700 transition-all"
            >
              ✨ Create Your Own Personalized Roadmap
            </a>
          </div>
        </div>

        {/* Week Plans */}
        <div className="space-y-4">
          {roadmap.week_plans.map((week) => (
            <div
              key={week.id}
              className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center mb-4">
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

              <div>
                <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full font-medium text-sm">
                  🎯 Target: {week.target_problems} problems
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Footer CTA */}
        <div className="mt-8 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg shadow-lg p-8 text-center text-white">
          <h3 className="text-2xl font-bold mb-3">Like this roadmap?</h3>
          <p className="mb-6 text-blue-100">
            Create your own personalized learning roadmap with SkillSprint AI
          </p>
          <a
            href="/"
            className="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
          >
            Get Started Free →
          </a>
        </div>
      </div>
    </div>
  )
}

export default SharedRoadmap
