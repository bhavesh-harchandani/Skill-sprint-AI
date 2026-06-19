function LandingPage({ onGetStarted }) {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-6xl font-extrabold text-gray-900 mb-6 animate-fade-in">
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                SkillSprint AI
              </span>
            </h1>
            <p className="text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Your AI-powered learning companion that creates personalized, week-by-week roadmaps for any skill
            </p>
            <button
              onClick={onGetStarted}
              className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:from-blue-700 hover:to-indigo-700 transform hover:scale-105 transition-all duration-200 shadow-lg"
            >
              🚀 Get Started Free
            </button>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-16">
            Why Choose SkillSprint AI?
          </h2>
          
          <div className="grid md:grid-cols-3 gap-12">
            {/* Feature 1 */}
            <div className="text-center p-6 rounded-xl hover:shadow-xl transition-shadow">
              <div className="text-5xl mb-4">🤖</div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">
                AI-Powered Mentor
              </h3>
              <p className="text-gray-600">
                GPT-4o-mini asks clarifying questions and generates personalized roadmaps tailored to your level, time, and goals
              </p>
            </div>

            {/* Feature 2 */}
            <div className="text-center p-6 rounded-xl hover:shadow-xl transition-shadow">
              <div className="text-5xl mb-4">📊</div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">
                Progress Tracking
              </h3>
              <p className="text-gray-600">
                Mark weeks as complete, visualize your progress, and stay motivated with timeline and detailed views
              </p>
            </div>

            {/* Feature 3 */}
            <div className="text-center p-6 rounded-xl hover:shadow-xl transition-shadow">
              <div className="text-5xl mb-4">📤</div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">
                Export & Share
              </h3>
              <p className="text-gray-600">
                Download your roadmap as PDF or share it with friends, mentors, or on social media
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="bg-gradient-to-br from-blue-50 to-indigo-100 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-16">
            How It Works
          </h2>
          
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-blue-600 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="font-bold text-lg mb-2">Enter Your Goal</h3>
              <p className="text-gray-600">Tell us what you want to learn</p>
            </div>

            <div className="text-center">
              <div className="bg-blue-600 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="font-bold text-lg mb-2">Answer Questions</h3>
              <p className="text-gray-600">AI asks about your level and time</p>
            </div>

            <div className="text-center">
              <div className="bg-blue-600 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="font-bold text-lg mb-2">Get Your Roadmap</h3>
              <p className="text-gray-600">Receive personalized week-by-week plan</p>
            </div>

            <div className="text-center">
              <div className="bg-blue-600 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                4
              </div>
              <h3 className="font-bold text-lg mb-2">Track Progress</h3>
              <p className="text-gray-600">Mark weeks complete as you learn</p>
            </div>
          </div>
        </div>
      </div>

      {/* Use Cases */}
      <div className="bg-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-16">
            Perfect For Any Learning Goal
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { icon: '💻', title: 'DSA & Coding', desc: 'Master algorithms for interviews' },
              { icon: '🤖', title: 'Machine Learning', desc: 'Build AI models from scratch' },
              { icon: '☁️', title: 'DevOps & Cloud', desc: 'Deploy scalable applications' },
              { icon: '🎨', title: 'Web Development', desc: 'Create modern websites' },
              { icon: '📱', title: 'Mobile Apps', desc: 'Build iOS & Android apps' },
              { icon: '🔒', title: 'Cybersecurity', desc: 'Learn ethical hacking' },
              { icon: '📊', title: 'Data Science', desc: 'Analyze and visualize data' },
              { icon: '🎮', title: 'Game Dev', desc: 'Create your own games' }
            ].map((item, idx) => (
              <div key={idx} className="bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-xl text-center hover:shadow-lg transition-shadow">
                <div className="text-4xl mb-3">{item.icon}</div>
                <h3 className="font-bold text-gray-900 mb-2">{item.title}</h3>
                <p className="text-sm text-gray-600">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 py-20">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Start Your Learning Journey?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join thousands of learners who are achieving their goals with AI-powered roadmaps
          </p>
          <button
            onClick={onGetStarted}
            className="bg-white text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transform hover:scale-105 transition-all duration-200 shadow-lg"
          >
            Create Your Roadmap Now →
          </button>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-gray-400 mb-4">
            Built with ❤️ using FastAPI, React, and OpenAI
          </p>
          <p className="text-gray-500 text-sm">
            © 2026 SkillSprint AI. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  )
}

export default LandingPage
