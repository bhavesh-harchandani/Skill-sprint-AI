function Timeline({ weeks, weekStatuses }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-xl font-semibold text-gray-800 mb-4">📈 Learning Timeline</h3>
      
      <div className="relative">
        {/* Timeline line */}
        <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gray-300"></div>
        
        {/* Timeline items */}
        <div className="space-y-4">
          {weeks.map((week, index) => {
            const isCompleted = weekStatuses[week.id] || false
            const isLast = index === weeks.length - 1
            
            return (
              <div key={week.id} className="relative flex items-start">
                {/* Timeline dot */}
                <div className={`relative z-10 flex items-center justify-center w-12 h-12 rounded-full border-4 ${
                  isCompleted 
                    ? 'bg-green-500 border-green-200' 
                    : 'bg-white border-gray-300'
                }`}>
                  {isCompleted ? (
                    <span className="text-white font-bold">✓</span>
                  ) : (
                    <span className="text-gray-600 font-semibold text-sm">{week.week_number}</span>
                  )}
                </div>
                
                {/* Content */}
                <div className={`ml-4 flex-1 pb-8 ${isLast ? 'pb-0' : ''}`}>
                  <div className={`p-3 rounded-lg ${
                    isCompleted ? 'bg-green-50' : 'bg-gray-50'
                  }`}>
                    <h4 className={`font-semibold ${
                      isCompleted ? 'text-green-800' : 'text-gray-800'
                    }`}>
                      Week {week.week_number}: {week.focus_title}
                    </h4>
                    <p className="text-sm text-gray-600 mt-1">
                      {week.topics_json.length} topics • {week.tasks_json.length} tasks
                    </p>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default Timeline
