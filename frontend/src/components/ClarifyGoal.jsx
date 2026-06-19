import { useState } from 'react'
import axios from 'axios'

function ClarifyGoal({ onComplete, onBack }) {
  const [step, setStep] = useState('goal') // 'goal', 'loading', 'questions'
  const [goal, setGoal] = useState('')
  const [questions, setQuestions] = useState([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState([])
  const [currentAnswer, setCurrentAnswer] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleGoalSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await axios.post('http://localhost:8000/ai/clarify', {
        goal: goal
      })
      
      setQuestions(response.data.questions)
      setStep('questions')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate questions')
      console.error('Error generating questions:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleAnswerSubmit = (e) => {
    e.preventDefault()
    
    if (!currentAnswer.trim()) {
      return
    }

    const newAnswers = [...answers, currentAnswer]
    setAnswers(newAnswers)
    setCurrentAnswer('')

    // Move to next question or complete
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    } else {
      // All questions answered
      onComplete({
        goal,
        questions,
        answers: newAnswers
      })
    }
  }

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
      setCurrentAnswer(answers[currentQuestionIndex - 1])
      setAnswers(answers.slice(0, -1))
    }
  }

  const handleBackToGoal = () => {
    setStep('goal')
    setQuestions([])
    setAnswers([])
    setCurrentQuestionIndex(0)
    setCurrentAnswer('')
    setError(null)
  }

  if (step === 'goal') {
    return (
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6">
          What do you want to learn?
        </h2>
        
        <form onSubmit={handleGoalSubmit} className="space-y-6">
          <div>
            <label htmlFor="goal" className="block text-sm font-medium text-gray-700 mb-2">
              Learning Goal
            </label>
            <textarea
              id="goal"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="e.g., I want to learn Data Structures & Algorithms for technical interviews"
              rows="4"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              required
            />
            <p className="mt-2 text-sm text-gray-500">
              Be specific about what you want to learn. We'll ask follow-up questions to personalize your roadmap.
            </p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <div className="flex gap-3">
            {onBack && (
              <button
                type="button"
                onClick={onBack}
                className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
              >
                Back
              </button>
            )}
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {loading ? 'Analyzing...' : 'Next'}
            </button>
          </div>
        </form>
      </div>
    )
  }

  if (step === 'questions') {
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100

    return (
      <div className="bg-white rounded-lg shadow-lg p-8">
        {/* Progress bar */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">
              Question {currentQuestionIndex + 1} of {questions.length}
            </span>
            <button
              onClick={handleBackToGoal}
              className="text-sm text-gray-500 hover:text-gray-700"
            >
              Start Over
            </button>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Goal reminder */}
        <div className="mb-6 p-4 bg-blue-50 rounded-lg">
          <p className="text-sm text-gray-600">
            <span className="font-semibold">Your goal:</span> {goal}
          </p>
        </div>

        {/* Chat-style questions */}
        <div className="space-y-4 mb-6">
          {/* Previous Q&A */}
          {answers.map((answer, idx) => (
            <div key={idx} className="space-y-3">
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-lg px-4 py-3 max-w-[80%]">
                  <p className="text-gray-800">{questions[idx]}</p>
                </div>
              </div>
              <div className="flex justify-end">
                <div className="bg-blue-600 text-white rounded-lg px-4 py-3 max-w-[80%]">
                  <p>{answer}</p>
                </div>
              </div>
            </div>
          ))}

          {/* Current question */}
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg px-4 py-3 max-w-[80%]">
              <p className="text-gray-800 font-medium">{questions[currentQuestionIndex]}</p>
            </div>
          </div>
        </div>

        {/* Answer input */}
        <form onSubmit={handleAnswerSubmit} className="space-y-4">
          <div>
            <textarea
              value={currentAnswer}
              onChange={(e) => setCurrentAnswer(e.target.value)}
              placeholder="Type your answer here..."
              rows="3"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              required
              autoFocus
            />
          </div>

          <div className="flex gap-3">
            {currentQuestionIndex > 0 && (
              <button
                type="button"
                onClick={handlePrevious}
                className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
              >
                Previous
              </button>
            )}
            <button
              type="submit"
              className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              {currentQuestionIndex === questions.length - 1 ? 'Complete' : 'Next'}
            </button>
          </div>
        </form>
      </div>
    )
  }

  return null
}

export default ClarifyGoal
