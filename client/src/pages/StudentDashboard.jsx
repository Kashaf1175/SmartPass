import { useState, useEffect, useContext } from 'react'
import { AuthContext } from '../context/AuthContext'
import { fetchAttendance, fetchWeeklyAttendance, fetchOverallAttendance } from '../services/attendanceService'
import Navbar from '../components/Navbar'
import AttendanceButton from '../components/AttendanceButton'
import Chart from '../components/Chart'

function StudentDashboard() {
  const { user } = useContext(AuthContext)
  const [attendanceHistory, setAttendanceHistory] = useState([])
  const [weeklyAttendance, setWeeklyAttendance] = useState(null)
  const [overallAttendance, setOverallAttendance] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('mark')

  useEffect(() => {
    const loadData = async () => {
      try {
        const [historyData, weeklyData, overallData] = await Promise.all([
          fetchAttendance(),
          fetchWeeklyAttendance(),
          fetchOverallAttendance()
        ])
        setAttendanceHistory(historyData)
        setWeeklyAttendance(weeklyData)
        setOverallAttendance(overallData)
      } catch (error) {
        console.error('Error loading attendance data:', error)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  const handleAttendanceMarked = async (newRecord) => {
    setAttendanceHistory([newRecord, ...attendanceHistory])
    // Refresh weekly and overall data
    try {
      const [weeklyData, overallData] = await Promise.all([
        fetchWeeklyAttendance(),
        fetchOverallAttendance()
      ])
      setWeeklyAttendance(weeklyData)
      setOverallAttendance(overallData)
    } catch (error) {
      console.error('Error refreshing attendance data:', error)
    }
  }

  const chartData = attendanceHistory.reduce((acc, item) => {
    const label = item.is_flagged ? 'Flagged' : 'Normal'
    acc[label] = (acc[label] || 0) + 1
    return acc
  }, {})

  const chartDataArray = Object.entries(chartData).map(([name, value]) => ({ name, value }))

  // Weekly attendance chart data
  const weeklyChartData = weeklyAttendance ? Object.entries(weeklyAttendance.subjects).map(([subject, data]) => ({
    name: data.subject_code,
    value: data.percentage
  })) : []

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-500 mx-auto mb-4"></div>
          <p>Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <Navbar />
      <div className="px-4 py-6">
        <header className="mb-6">
          <h1 className="text-3xl font-semibold">Student Panel</h1>
          <p className="text-slate-400 mt-1">Mark attendance and review your progress.</p>
        </header>

        {/* Tab Navigation */}
        <div className="flex space-x-1 mb-6 bg-slate-800 p-1 rounded-2xl">
          {['mark', 'weekly', 'overall', 'history'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`flex-1 py-2 px-4 rounded-xl font-medium transition-colors ${
                activeTab === tab
                  ? 'bg-cyan-500 text-slate-950'
                  : 'text-slate-300 hover:text-slate-100'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {activeTab === 'mark' && (
          <>
            <div className="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
              <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/40">
                <h2 className="text-xl font-semibold mb-4">Mark Attendance</h2>
                <AttendanceButton onAttendanceMarked={handleAttendanceMarked} />
              </div>
              <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/30">
                <h2 className="text-xl font-semibold mb-4">Activity Summary</h2>
                <div className="space-y-3 text-slate-300">
                  <p>Entries recorded: <strong>{attendanceHistory.length}</strong></p>
                  <p>Latest score: <strong>{attendanceHistory[0]?.fraud_score ?? 'N/A'}</strong></p>
                  <p>Flagged events: <strong>{attendanceHistory.filter((item) => item.is_flagged).length}</strong></p>
                </div>
              </div>
            </div>

            <div className="grid gap-6 lg:grid-cols-2 mt-6">
              <Chart data={chartDataArray} type="bar" title="Fraud Trend" />
              <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/30">
                <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
                <div className="space-y-3">
                  <button
                    onClick={() => setActiveTab('weekly')}
                    className="w-full rounded-2xl bg-slate-800 px-4 py-3 text-left hover:bg-slate-700"
                  >
                    📊 View Weekly Report
                  </button>
                  <button
                    onClick={() => setActiveTab('overall')}
                    className="w-full rounded-2xl bg-slate-800 px-4 py-3 text-left hover:bg-slate-700"
                  >
                    📈 Overall Progress
                  </button>
                  <button
                    onClick={() => setActiveTab('history')}
                    className="w-full rounded-2xl bg-slate-800 px-4 py-3 text-left hover:bg-slate-700"
                  >
                    📋 Full History
                  </button>
                  <button
                    onClick={() => window.location.reload()}
                    className="w-full rounded-2xl bg-slate-800 px-4 py-3 text-left hover:bg-slate-700"
                  >
                    🔄 Refresh Data
                  </button>
                </div>
              </div>
            </div>
          </>
        )}

        {activeTab === 'weekly' && weeklyAttendance && (
          <div className="space-y-6">
            <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/40">
              <h2 className="text-xl font-semibold mb-4">Weekly Attendance Report</h2>
              <div className="grid gap-4 md:grid-cols-3 mb-6">
                <div className="text-center">
                  <p className="text-2xl font-bold text-cyan-400">Week {weeklyAttendance.week_of_month}</p>
                  <p className="text-sm text-slate-400">Week of Month</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-emerald-400">{weeklyAttendance.month}</p>
                  <p className="text-sm text-slate-400">Month</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-emerald-400">{weeklyAttendance.week_start} - {weeklyAttendance.week_end}</p>
                  <p className="text-sm text-slate-400">Week Range</p>
                </div>
              </div>
              
              <div className="space-y-4">
                {Object.entries(weeklyAttendance.subjects).map(([subjectName, subjectData]) => (
                  <div key={subjectName} className="rounded-2xl border border-slate-700 bg-slate-800 p-4">
                    <div className="flex justify-between items-center mb-3">
                      <h3 className="font-semibold">{subjectName} ({subjectData.subject_code})</h3>
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                        subjectData.percentage >= 75 ? 'bg-emerald-500/20 text-emerald-400' :
                        subjectData.percentage >= 50 ? 'bg-yellow-500/20 text-yellow-400' :
                        'bg-red-500/20 text-red-400'
                      }`}>
                        {subjectData.percentage}%
                      </span>
                    </div>
                    
                    <div className="space-y-2">
                      {subjectData.classes.map((classItem, index) => (
                        <div key={index} className="flex justify-between items-center text-sm">
                          <span>{classItem.class_name} - {classItem.day}</span>
                          <span className={classItem.attended ? 'text-emerald-400' : 'text-red-400'}>
                            {classItem.attended ? '✓ Present' : '✗ Absent'}
                          </span>
                        </div>
                      ))}
                    </div>
                    
                    <div className="mt-3 text-sm text-slate-400">
                      Attended: {subjectData.attended_classes}/{subjectData.total_classes} classes
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            {weeklyChartData.length > 0 && (
              <Chart data={weeklyChartData} type="bar" title="Weekly Subject Performance (%)" />
            )}
          </div>
        )}

        {activeTab === 'overall' && overallAttendance && (
          <div className="space-y-6">
            <div className="grid gap-6 lg:grid-cols-2">
              <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/40">
                <h2 className="text-xl font-semibold mb-4">Overall Attendance</h2>
                <div className="text-center mb-6">
                  <div className={`text-6xl font-bold mb-2 ${
                    overallAttendance.overall_percentage >= 75 ? 'text-emerald-400' :
                    overallAttendance.overall_percentage >= 50 ? 'text-yellow-400' :
                    'text-red-400'
                  }`}>
                    {overallAttendance.overall_percentage}%
                  </div>
                  <p className="text-slate-400">Overall Attendance Rate</p>
                  {overallAttendance.at_risk && (
                    <p className="text-red-400 text-sm mt-2">⚠️ At risk of detention (below 50%)</p>
                  )}
                </div>
                
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between">
                    <span>Total Classes Attended:</span>
                    <span className="font-semibold">{overallAttendance.total_attended}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Total Classes Scheduled:</span>
                    <span className="font-semibold">{overallAttendance.total_possible}</span>
                  </div>
                </div>
              </div>
              
              <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/40">
                <h2 className="text-xl font-semibold mb-4">Subject-wise Performance</h2>
                <div className="space-y-3">
                  {Object.entries(overallAttendance.subjects).map(([subjectName, subjectData]) => (
                    <div key={subjectName} className="flex justify-between items-center">
                      <span className="text-sm">{subjectData.subject_code}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-20 bg-slate-700 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full ${
                              subjectData.percentage >= 75 ? 'bg-emerald-500' :
                              subjectData.percentage >= 50 ? 'bg-yellow-500' :
                              'bg-red-500'
                            }`}
                            style={{ width: `${Math.min(subjectData.percentage, 100)}%` }}
                          ></div>
                        </div>
                        <span className={`text-sm font-semibold ${
                          subjectData.percentage >= 75 ? 'text-emerald-400' :
                          subjectData.percentage >= 50 ? 'text-yellow-400' :
                          'text-red-400'
                        }`}>
                          {subjectData.percentage}%
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'history' && (
          <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/40">
            <h2 className="text-xl font-semibold mb-4">Attendance History</h2>
            <div className="space-y-3">
              {attendanceHistory.length === 0 ? (
                <p className="text-slate-400 text-center py-8">No attendance records found.</p>
              ) : (
                attendanceHistory.map((record, index) => (
                  <div key={index} className="flex justify-between items-center p-3 rounded-2xl bg-slate-800">
                    <div>
                      <p className="font-medium">{new Date(record.timestamp).toLocaleString()}</p>
                      <p className="text-sm text-slate-400">Class ID: {record.class_id}</p>
                    </div>
                    <div className="text-right">
                      <p className={`font-semibold ${record.is_flagged ? 'text-red-400' : 'text-emerald-400'}`}>
                        {record.is_flagged ? 'Flagged' : 'Normal'}
                      </p>
                      <p className="text-sm text-slate-400">Score: {record.fraud_score}</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default StudentDashboard
