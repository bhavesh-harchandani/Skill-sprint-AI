import { useAuth } from '../context/AuthContext'

function Navbar({ onLogoClick }) {
  const { user, logout, isAuthenticated } = useAuth()

  return (
    <div className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <h1 
            className="text-3xl font-bold text-gray-800 cursor-pointer hover:text-blue-600 transition-colors"
            onClick={onLogoClick}
          >
            SkillSprint AI
          </h1>
          
          {isAuthenticated && user && (
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-800">{user.name}</p>
                <p className="text-xs text-gray-500">{user.email}</p>
              </div>
              <button
                onClick={logout}
                className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors font-medium"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Navbar
