import { useState, useEffect } from 'react'
import axios from 'axios'

function MyRoadmaps({ onSelectRoadmap, onCreateNew }) {
  const [roadmaps, setRoadmaps] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchRoadmaps()
  }, [])

  const fetchRoadmaps = async () => {
    try {
      const response = await axios.get('http://localhost:8000/roadmaps/')
      setRoadmaps(response.data)
      setLoading(false)
    } catch (err) {
      setError('Failed to load roadmaps')
      setLoading(false)
      console.error('Error fetching roadmaps:', err)
    }
  }

  const handleContinue = async (roadmapId) => {
    try {
      // Fetch full roadmap data
      const response = await axios.get(`http://localhost:8000/roadmaps/${roadmapId}`)
      
      // Save to localStorage
      localStorage.setItem('lastRoadmapId', roadmapId)
      
      // Pass to parent
      onSelectRoadmap(response.data)
    } catch (err) {
      console.error('Error loading roadmap:', err)
      alert('Failed to load roadmap. Please try again.')
    }
  }

  const handleDelete = async (roadmapId, e) => {
    e.stopPropagation()
    
    if (!confirm('Are you sure you want to delete this roadmap?')) {
      return
    }

    try {
      await axios.delete(`http://localhost:8000/roadmaps/${roadmapId}`)
      setRoadmaps(roadmaps.filter(r => r.id !== roadmapId))
      
      // Clear from localStorage if it was the last opened
      if (localStorage.getItem('lastRoadmapId') === roadmapId.toString()) {
        localStorage.removeItem('lastRoadmapId')
      }
    } catch (err) {
      console.error('Error deleting roadmap:', err)
      alert('Failed to delete roadmap. Please try again.')
    }
  }

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your roadmaps...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="text-center">
          <div className="text-red-600 text-5xl mb-4">⚠️</div>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Error Loading Roadmaps</h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={fetchRoadmaps}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  if (roadmaps.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="text-center">
          <div className="text-6xl mb-4">📚</div>
          <h3 className="text-2xl font-semibold text-gray-800 mb-2">No Roadmaps Yet</h3>
          <p className="text-gray-600 mb-6">
            Create your first AI-powered learning roadmap to get started!
          </p>
          <button
            onClick={onCreateNew}
            className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-indigo-700 transition-all"
          >
            ✨ Create Your First Roadmap
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-3xl font-bold text-gray-800 mb-2">My Roadmaps</h2>
            <p className="text-gray-600">Continue your learning journey</p>
          </div>
          <button
            onClick={onCreateNew}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            + New Roadmap
          </button>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {roadmaps.map((roadmap) => (
            <div
              key={roadmap.id}
              className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer"
              onClick={() => handleContinue(roadmap.id)}
            >
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-gray-800 mb-2">
                    {roadmap.goal}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {roadmap.duration_weeks} weeks • Created {new Date(roadmap.created_at).toLocaleDateString()}
                  </p>
                </div>
                <button
                  onClick={(e) => handleDelete(roadmap.id, e)}
                  className="text-gray-400 hover:text-red-600 transition-colors p-2"
                  title="Delete roadmap"
                >
                  🗑️
                </button>
              </div>

              {/* Progress Bar */}
              <div className="mb-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-gray-700">Progress</span>
                  <span className="text-sm font-semibold text-blue-600">
                    {roadmap.progress_percent}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-blue-500 to-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${roadmap.progress_percent}%` }}
                  ></div>
                </div>
              </div>

              {/* Continue Button */}
              <button
                onClick={() => handleContinue(roadmap.id)}
                className="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                Continue Learning →
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default MyRoadmaps
