import { useState, useEffect } from 'react'
import axios from 'axios'
import LoadingOverlay from './LoadingOverlay'

function RoadmapForm({ clarificationData, onRoadmapCreated, onBack }) {
  const [durationWeeks, setDurationWeeks] = useState(8)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Extract duration from answers if available
  useEffect(() => {
    if (clarificationData?.answers) {
      const durationAnswer = clarificationData.answers.find(answer => 
        /\d+\s*(week|wk)/i.test(answer)
      )
      if (durationAnswer) {
        const match = durationAnswer.match(/(\d+)\s*(week|wk)/i)
        if (match) {
          setDurationWeeks(parseInt(match[1]))
        }
      }
    }
  }, [clarificationData])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      // Format answers as key-value pairs
      const answersDict = {}
      clarificationData.questions.forEach((question, idx) => {
        // Create a simple key from the question
        const key = question.toLowerCase()
          .replace(/[^a-z0-9\s]/g, '')
          .split(' ')
          .slice(0, 3)
          .join('_')
        answersDict[key] = clarificationData.answers[idx]
      })

      // Call AI generation endpoint
      const response = await axios.post('http://localhost:8000/ai/generate-roadmap', {
        goal: clarificationData.goal,
        answers: answersDict,
        duration_weeks: durationWeeks
      })

      // Transform response to match expected format
      const roadmapData = {
        id: response.data.roadmap_id,
        goal: response.data.goal,
        duration_weeks: response.data.duration_weeks,
        created_at: new Date().toISOString(),
        week_plans: response.data.weeks.map(week => ({
          id: week.week,
          roadmap_id: response.data.roadmap_id,
          week_number: week.week,
          focus_title: week.focus,
          topics_json: week.topics,
          tasks_json: week.practice_tasks,
          target_problems: week.target_problems
        }))
      }

      onRoadmapCreated(roadmapData)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate roadmap')
      console.error('Error generating roadmap:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {loading && <LoadingOverlay message="🤖 AI is crafting your personalized roadmap..." />}
      
      <div className="bg-white rounded-lg shadow-lg p-8">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">
        Review & Generate Roadmap
      </h2>

      {/* Display clarification summary */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg space-y-3">
        <div>
          <p className="text-sm font-semibold text-gray-700">Your Goal:</p>
          <p className="text-gray-800">{clarificationData.goal}</p>
        </div>
        
        <div className="border-t pt-3">
          <p className="text-sm font-semibold text-gray-700 mb-2">Your Answers:</p>
          <div className="space-y-2">
            {clarificationData.questions.map((question, idx) => (
              <div key={idx} className="text-sm">
                <p className="text-gray-600">{question}</p>
                <p className="text-gray-800 font-medium ml-4">→ {clarificationData.answers[idx]}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="duration" className="block text-sm font-medium text-gray-700 mb-2">
            Duration (weeks)
          </label>
          <input
            type="number"
            id="duration"
            value={durationWeeks}
            onChange={(e) => setDurationWeeks(parseInt(e.target.value))}
            min="1"
            max="52"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        <div className="flex gap-3">
          <button
            type="button"
            onClick={onBack}
            className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
          >
            Back
          </button>
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating AI Roadmap...
              </>
            ) : (
              '✨ Generate AI Roadmap'
            )}
          </button>
        </div>
      </form>

      <div className="mt-6 p-4 bg-green-50 rounded-lg">
        <p className="text-sm text-gray-600">
          <span className="font-semibold">✨ AI-Powered:</span> Your roadmap will be personalized 
          based on your goal and answers using GPT-4o-mini.
        </p>
      </div>
      </div>
    </>
  )
}

export default RoadmapForm
