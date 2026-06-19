import { useState, useEffect } from 'react'
import axios from 'axios'
import ProgressBar from './ProgressBar'
import WeekCard from './WeekCard'
import Timeline from './Timeline'

function Dashboard({ roadmap, onBack }) {
  const [progress, setProgress] = useState(null)
  const [weekStatuses, setWeekStatuses] = useState({})
  const [loading, setLoading] = useState(true)
  const [view, setView] = useState('cards') // 'cards' or 'timeline'
  const [shareUrl, setShareUrl] = useState(null)
  const [showShareModal, setShowShareModal] = useState(false)
  const [copySuccess, setCopySuccess] = useState(false)

  useEffect(() => {
    if (roadmap) {
      fetchProgress()
      fetchWeekStatuses()
    }
  }, [roadmap])

  const fetchProgress = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/roadmaps/${roadmap.id}/progress`)
      setProgress(response.data)
    } catch (error) {
      console.error('Error fetching progress:', error)
    }
  }

  const fetchWeekStatuses = async () => {
    try {
      const statuses = {}
      for (const week of roadmap.week_plans) {
        const response = await axios.get(`http://localhost:8000/weeks/${week.id}/status`)
        statuses[week.id] = response.data.completed
      }
      setWeekStatuses(statuses)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching week statuses:', error)
      setLoading(false)
    }
  }

  const handleToggleComplete = async (weekId) => {
    try {
      const response = await axios.patch(`http://localhost:8000/weeks/${weekId}/complete`)
      
      setWeekStatuses(prev => ({
        ...prev,
        [weekId]: response.data.completed
      }))
      
      await fetchProgress()
    } catch (error) {
      console.error('Error toggling completion:', error)
    }
  }

  const handleExportPDF = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/roadmaps/${roadmap.id}/export/pdf`,
        { responseType: 'blob' }
      )
      
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `roadmap_${roadmap.id}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (error) {
      console.error('Error exporting PDF:', error)
      alert('Failed to export PDF. Please try again.')
    }
  }

  const handleGenerateShareLink = async () => {
    try {
      const response = await axios.post(`http://localhost:8000/roadmaps/${roadmap.id}/share`)
      const fullUrl = `${window.location.origin}${response.data.share_url}`
      setShareUrl(fullUrl)
      setShowShareModal(true)
    } catch (error) {
      console.error('Error generating share link:', error)
      alert('Failed to generate share link. Please try again.')
    }
  }

  const handleCopyLink = () => {
    navigator.clipboard.writeText(shareUrl)
    setCopySuccess(true)
    setTimeout(() => setCopySuccess(false), 2000)
  }

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-8">
        <p className="text-center text-gray-600">Loading dashboard...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
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
            ← New Roadmap
          </button>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3 mb-6">
          <button
            onClick={handleExportPDF}
            className="flex-1 bg-green-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-green-700 transition-colors flex items-center justify-center gap-2"
          >
            📄 Download PDF
          </button>
          <button
            onClick={handleGenerateShareLink}
            className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
          >
            🔗 Share Roadmap
          </button>
        </div>

        {/* Progress Overview */}
        {progress && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-xl font-semibold text-gray-800">Your Progress</h3>
              <span className="text-2xl font-bold text-blue-600">
                {progress.progress_percent}%
              </span>
            </div>
            
            <ProgressBar 
              completed={progress.completed_weeks} 
              total={progress.total_weeks}
              percent={progress.progress_percent}
            />
            
            <div className="flex gap-6 text-center">
              <div className="flex-1 bg-blue-50 rounded-lg p-4">
                <p className="text-3xl font-bold text-blue-600">{progress.completed_weeks}</p>
                <p className="text-sm text-gray-600">Completed</p>
              </div>
              <div className="flex-1 bg-gray-50 rounded-lg p-4">
                <p className="text-3xl font-bold text-gray-600">
                  {progress.total_weeks - progress.completed_weeks}
                </p>
                <p className="text-sm text-gray-600">Remaining</p>
              </div>
              <div className="flex-1 bg-green-50 rounded-lg p-4">
                <p className="text-3xl font-bold text-green-600">{progress.total_weeks}</p>
                <p className="text-sm text-gray-600">Total Weeks</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* View Toggle */}
      <div className="flex justify-center gap-2 bg-white rounded-lg shadow p-2">
        <button
          onClick={() => setView('cards')}
          className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
            view === 'cards'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          📋 Detailed View
        </button>
        <button
          onClick={() => setView('timeline')}
          className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
            view === 'timeline'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          📈 Timeline View
        </button>
      </div>

      {/* Content based on view */}
      {view === 'timeline' ? (
        <Timeline weeks={roadmap.week_plans} weekStatuses={weekStatuses} />
      ) : (
        <div className="space-y-4">
          <h3 className="text-2xl font-semibold text-gray-800 bg-white rounded-lg shadow p-4">
            📅 Weekly Roadmap
          </h3>
          
          {roadmap.week_plans.map((week) => (
            <WeekCard
              key={week.id}
              week={week}
              completed={weekStatuses[week.id] || false}
              onToggleComplete={() => handleToggleComplete(week.id)}
            />
          ))}
        </div>
      )}

      {/* Share Modal */}
      {showShareModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg p-8 max-w-md w-full">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Share Your Roadmap</h3>
            <p className="text-gray-600 mb-4">
              Anyone with this link can view your roadmap (read-only)
            </p>
            
            <div className="bg-gray-50 p-3 rounded-lg mb-4 break-all text-sm">
              {shareUrl}
            </div>
            
            <div className="flex gap-3">
              <button
                onClick={handleCopyLink}
                className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                {copySuccess ? '✓ Copied!' : '📋 Copy Link'}
              </button>
              <button
                onClick={() => setShowShareModal(false)}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard
