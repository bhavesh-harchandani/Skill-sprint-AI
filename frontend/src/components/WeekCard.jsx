import { useState } from 'react'
import axios from 'axios'

function WeekCard({ week, completed, onToggleComplete }) {
  const [recommendations, setRecommendations] = useState(null)
  const [loadingRecs, setLoadingRecs] = useState(false)
  const [showRecs, setShowRecs] = useState(false)
  const [error, setError] = useState(null)

  const fetchRecommendations = async () => {
    if (recommendations) {
      setShowRecs(!showRecs)
      return
    }

    setLoadingRecs(true)
    setError(null)
    
    try {
      const response = await axios.get(`http://localhost:8000/recommendations/${week.id}`)
      setRecommendations(response.data.recommendations)
      setShowRecs(true)
      
      // Show success message for topic-specific expansion
      if (response.data.recommendations.length > 0) {
        console.log(`Loaded ${response.data.recommendations.length} recommendations for: ${week.focus_title}`)
      }
    } catch (err) {
      if (err.response?.status === 500) {
        const detail = err.response?.data?.detail || ''
        if (detail.includes('expanding') || detail.includes('Generating')) {
          setError(`Generating practice items for "${week.focus_title}"... Please try again in a moment.`)
        } else {
          setError('Failed to load recommendations. Please try again.')
        }
      } else if (err.response?.status === 403) {
        setError('Not authorized to access this week')
      } else {
        setError(err.response?.data?.detail || 'Failed to load recommendations')
      }
      console.error('Error fetching recommendations:', err)
    } finally {
      setLoadingRecs(false)
    }
  }

  const getDifficultyColor = (difficulty) => {
    switch (difficulty.toLowerCase()) {
      case 'easy':
        return 'bg-green-100 text-green-800'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'hard':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div
      className={`border rounded-lg p-6 transition-all ${
        completed
          ? 'bg-green-50 border-green-300 opacity-75'
          : 'bg-white border-gray-200 hover:shadow-md'
      }`}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center flex-1">
          <span
            className={`px-3 py-1 rounded-full text-sm font-semibold mr-3 ${
              completed
                ? 'bg-green-600 text-white'
                : 'bg-blue-600 text-white'
            }`}
          >
            Week {week.week_number}
          </span>
          <h3 className={`text-xl font-semibold ${
            completed ? 'text-gray-600 line-through' : 'text-gray-800'
          }`}>
            {week.focus_title}
          </h3>
          {completed && (
            <span className="ml-3 text-green-600">
              ✓
            </span>
          )}
        </div>
        
        <button
          onClick={onToggleComplete}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            completed
              ? 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }`}
        >
          {completed ? 'Mark Incomplete' : 'Mark Complete'}
        </button>
      </div>

      <div className="mb-4">
        <h4 className="text-sm font-semibold text-gray-700 mb-2">📚 Topics:</h4>
        <ul className="list-disc list-inside space-y-1">
          {week.topics_json.map((topic, idx) => (
            <li key={idx} className={completed ? 'text-gray-500' : 'text-gray-600'}>
              {topic}
            </li>
          ))}
        </ul>
      </div>

      <div className="mb-4">
        <h4 className="text-sm font-semibold text-gray-700 mb-2">✅ Practice Tasks:</h4>
        <ul className="list-disc list-inside space-y-1">
          {week.tasks_json.map((task, idx) => (
            <li key={idx} className={completed ? 'text-gray-500' : 'text-gray-600'}>
              {task}
            </li>
          ))}
        </ul>
      </div>

      <div className="flex items-center justify-between mb-4">
        <span
          className={`px-3 py-1 rounded-full font-medium text-sm ${
            completed
              ? 'bg-gray-200 text-gray-600'
              : 'bg-purple-100 text-purple-800'
          }`}
        >
          🎯 Target: {week.target_problems} problems
        </span>

        <button
          onClick={fetchRecommendations}
          disabled={loadingRecs}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors disabled:bg-indigo-400 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {loadingRecs ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Loading recommendations...</span>
            </>
          ) : (
            <>
              🎓 {showRecs ? 'Hide' : 'Get'} Practice Recommendations
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      {showRecs && recommendations && (
        <div className="mt-4 p-4 bg-indigo-50 border border-indigo-200 rounded-lg">
          <h4 className="text-sm font-semibold text-indigo-900 mb-3 flex items-center gap-2">
            <span>🎯</span>
            <span>Recommended Practice for: {week.focus_title}</span>
            <span className="text-xs font-normal text-indigo-600">
              (Topic-specific AI recommendations)
            </span>
          </h4>
          
          {recommendations.length === 0 ? (
            <p className="text-sm text-indigo-600">No recommendations available yet.</p>
          ) : (
            <div className="space-y-3">
              {recommendations.map((rec, idx) => (
                <div
                  key={rec.id}
                  className="bg-white p-3 rounded-lg border border-indigo-100 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-indigo-600 font-semibold">#{idx + 1}</span>
                        <a
                          href={rec.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:text-blue-800 font-medium hover:underline"
                        >
                          {rec.title}
                        </a>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{rec.description}</p>
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded">
                          {rec.topic}
                        </span>
                        <span className={`text-xs px-2 py-1 rounded font-medium ${getDifficultyColor(rec.difficulty)}`}>
                          {rec.difficulty}
                        </span>
                        {rec.tags && rec.tags.length > 0 && rec.tags.slice(0, 3).map((tag, tagIdx) => (
                          <span key={tagIdx} className="text-xs px-2 py-1 bg-blue-50 text-blue-700 rounded">
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default WeekCard
