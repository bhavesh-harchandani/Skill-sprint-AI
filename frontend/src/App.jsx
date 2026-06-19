import { useState } from 'react'
import { AuthProvider, useAuth } from './context/AuthContext'
import LandingPage from './components/LandingPage'
import Login from './components/Login'
import Signup from './components/Signup'
import ClarifyGoal from './components/ClarifyGoal'
import RoadmapForm from './components/RoadmapForm'
import Dashboard from './components/Dashboard'
import SharedRoadmap from './components/SharedRoadmap'
import MyRoadmaps from './components/MyRoadmaps'
import ProtectedRoute from './components/ProtectedRoute'
import Navbar from './components/Navbar'
import axios from 'axios'

function AppContent() {
  const [roadmap, setRoadmap] = useState(null)
  const [clarificationData, setClarificationData] = useState(null)
  const [view, setView] = useState('landing') // 'landing', 'login', 'signup', 'library', 'clarify', 'form', 'dashboard'
  const { isAuthenticated, loading } = useAuth()

  const handleGetStarted = () => {
    if (isAuthenticated) {
      setView('library')
    } else {
      setView('login')
    }
  }

  const handleLoginSuccess = () => {
    setView('library')
  }

  const handleSignupSuccess = () => {
    setView('library')
  }

  const handleCreateNew = () => {
    setRoadmap(null)
    setClarificationData(null)
    setView('clarify')
  }

  const handleClarificationComplete = (data) => {
    setClarificationData(data)
    setView('form')
  }

  const handleRoadmapCreated = (newRoadmap) => {
    setRoadmap(newRoadmap)
    localStorage.setItem('lastRoadmapId', newRoadmap.id)
    setView('dashboard')
  }

  const handleSelectRoadmap = (selectedRoadmap) => {
    setRoadmap(selectedRoadmap)
    setView('dashboard')
  }

  const handleBackToLibrary = () => {
    setView('library')
    setRoadmap(null)
  }

  const handleBackToLanding = () => {
    setView('landing')
    setClarificationData(null)
    setRoadmap(null)
  }

  const handleBackToClarify = () => {
    setView('clarify')
    setClarificationData(null)
    setRoadmap(null)
  }

  // Check if we're on a share URL
  const path = window.location.pathname
  if (path.startsWith('/share/')) {
    const publicId = path.split('/share/')[1]
    return <SharedRoadmap publicId={publicId} />
  }

  // Show loading while checking auth
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {view === 'landing' && (
        <LandingPage onGetStarted={handleGetStarted} />
      )}

      {view === 'login' && (
        <div className="min-h-screen flex items-center justify-center px-4">
          <Login 
            onSwitchToSignup={() => setView('signup')}
            onSuccess={handleLoginSuccess}
          />
        </div>
      )}

      {view === 'signup' && (
        <div className="min-h-screen flex items-center justify-center px-4">
          <Signup 
            onSwitchToLogin={() => setView('login')}
            onSuccess={handleSignupSuccess}
          />
        </div>
      )}
      
      {view !== 'landing' && view !== 'login' && view !== 'signup' && (
        <div>
          <Navbar onLogoClick={handleBackToLanding} />
          
          <div className="container mx-auto px-4 py-16">
            <div className="max-w-4xl mx-auto">
              <ProtectedRoute fallback={
                <div className="bg-white rounded-lg shadow-lg p-8 text-center">
                  <h2 className="text-2xl font-bold text-gray-800 mb-4">
                    Authentication Required
                  </h2>
                  <p className="text-gray-600 mb-6">
                    Please login to access this feature
                  </p>
                  <button
                    onClick={() => setView('login')}
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                  >
                    Go to Login
                  </button>
                </div>
              }>
                {view === 'library' && (
                  <MyRoadmaps 
                    onSelectRoadmap={handleSelectRoadmap}
                    onCreateNew={handleCreateNew}
                  />
                )}
                
                {view === 'clarify' && (
                  <ClarifyGoal onComplete={handleClarificationComplete} />
                )}
                
                {view === 'form' && (
                  <RoadmapForm 
                    clarificationData={clarificationData}
                    onRoadmapCreated={handleRoadmapCreated}
                    onBack={handleBackToClarify}
                  />
                )}
                
                {view === 'dashboard' && (
                  <Dashboard roadmap={roadmap} onBack={handleBackToLibrary} />
                )}
              </ProtectedRoute>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App
