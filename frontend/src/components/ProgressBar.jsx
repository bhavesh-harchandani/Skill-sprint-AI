function ProgressBar({ completed, total, percent }) {
  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-gray-700">
          {completed} of {total} weeks completed
        </span>
        <span className="text-sm font-semibold text-blue-600">
          {percent}%
        </span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
        <div
          className="bg-gradient-to-r from-blue-500 to-blue-600 h-4 rounded-full transition-all duration-500 ease-out flex items-center justify-end pr-2"
          style={{ width: `${percent}%` }}
        >
          {percent > 10 && (
            <span className="text-xs text-white font-semibold">
              {percent}%
            </span>
          )}
        </div>
      </div>
    </div>
  )
}

export default ProgressBar
