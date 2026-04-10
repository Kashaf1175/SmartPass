import { useState, useEffect, useContext } from 'react'
import { AuthContext } from '../context/AuthContext'
import { fetchAttendance, fetchWeeklyAttendance, fetchOverallAttendance } from '../services/attendanceService'
import Navbar from '../components/Navbar'
import Table from '../components/Table'
import Chart from '../components/Chart'

function History() {
  const { user } = useContext(AuthContext)
  const [attendanceHistory, setAttendanceHistory] = useState([])
  const [weeklyAttendance, setWeeklyAttendance] = useState(null)
  const [overallAttendance, setOverallAttendance] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const [data, weekly, overall] = await Promise.all([
          fetchAttendance(),
          fetchWeeklyAttendance(),
          fetchOverallAttendance(),
        ])
        setAttendanceHistory(data)
        setWeeklyAttendance(weekly)
        setOverallAttendance(overall)
      } catch (error) {
        console.error('Error loading attendance history:', error)
      } finally {
        setLoading(false)
      }
    }
    loadHistory()
  }, [])

  const chartData = attendanceHistory.reduce((acc, item) => {
    const label = item.is_flagged ? 'Flagged' : 'Normal'
    acc[label] = (acc[label] || 0) + 1
    return acc
  }, {})

  const chartDataArray = Object.entries(chartData).map(([name, value]) => ({ name, value }))

  const tableColumns = [
    { header: 'Timestamp', key: 'timestamp', render: (value) => new Date(value).toLocaleString() },
    { header: 'Device', key: 'device_id', render: (value) => value || 'unknown' },
    { header: 'Location', key: 'latitude', render: (value, row) => `${value?.toFixed(5)}, ${row.longitude?.toFixed(5)}` },
    { header: 'Fraud Score', key: 'fraud_score' },
    { header: 'Status', key: 'is_flagged', render: (value) => (
      <span className={`font-semibold ${value ? 'text-rose-400' : 'text-emerald-400'}`}>
        {value ? 'Flagged' : 'Normal'}
      </span>
    ) },
  ]

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyan-500 mx-auto mb-4"></div>
          <p>Loading history...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <Navbar />
      <div className="px-4 py-6">
        <header className="mb-6">
          <h1 className="text-3xl font-semibold">Attendance History</h1>
          <p className="text-slate-400 mt-1">View your complete attendance record, weekly timetable, and overall attendance metrics.</p>
        </header>

        {overallAttendance && (
          <div className="grid gap-6 lg:grid-cols-3 mb-6">
            <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/30">
              <h3 className="text-sm uppercase text-slate-500">Overall Attendance</h3>
              <p className="mt-3 text-3xl font-semibold text-cyan-300">{overallAttendance.overall_percentage}%</p>
              <p className="text-slate-400 mt-2">Attended {overallAttendance.total_attended} / {overallAttendance.total_possible} scheduled classes</p>
              {overallAttendance.at_risk && <p className="text-sm text-red-400 mt-2">⚠️ At risk of detention</p>}
            </div>
            <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/30">
              <h3 className="text-sm uppercase text-slate-500">Weekly Average</h3>
              <p className="mt-3 text-3xl font-semibold text-cyan-300">{weeklyAttendance?.weekly_percentage ?? 0}%</p>
              <p className="text-slate-400 mt-2">Current week: {weeklyAttendance?.week_start} to {weeklyAttendance?.week_end}</p>
            </div>
            <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/30">
              <h3 className="text-sm uppercase text-slate-500">Recent Activity</h3>
              <p className="mt-3 text-3xl font-semibold text-cyan-300">{attendanceHistory.length}</p>
              <p className="text-slate-400 mt-2">Total attendance records logged</p>
            </div>
          </div>
        )}

        {weeklyAttendance && (
          <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/40 mb-6">
            <div className="flex flex-col gap-3 mb-4 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <h2 className="text-xl font-semibold">Weekly Timetable</h2>
                <p className="text-slate-400">Week {weeklyAttendance.week_of_month} · {weeklyAttendance.month} · {weeklyAttendance.week_start} to {weeklyAttendance.week_end}</p>
              </div>
              <div className="space-x-3">
                <span className="inline-flex rounded-full bg-slate-800 px-3 py-1 text-sm text-slate-300">Classes: {weeklyAttendance.total_classes}</span>
                <span className="inline-flex rounded-full bg-slate-800 px-3 py-1 text-sm text-slate-300">Attended: {weeklyAttendance.total_attended}</span>
              </div>
            </div>
            <div className="grid gap-4 lg:grid-cols-2">
              {weeklyAttendance.days.map((day) => (
                <div key={day.date} className="rounded-3xl border border-slate-700 bg-slate-950 p-4">
                  <h3 className="font-semibold text-slate-100">{day.day_name} · {day.date}</h3>
                  {day.classes.length === 0 ? (
                    <p className="text-slate-500 mt-3">No classes scheduled.</p>
                  ) : (
                    <div className="mt-3 space-y-3">
                      {day.classes.map((classItem) => (
                        <div key={classItem.class_id} className="rounded-2xl border border-slate-800 bg-slate-900 p-3">
                          <div className="flex items-center justify-between gap-3">
                            <div>
                              <p className="font-semibold">{classItem.name}</p>
                              <p className="text-sm text-slate-500">{classItem.subject?.name || 'Unknown Subject'}</p>
                            </div>
                            <span className={`rounded-full px-2 py-1 text-xs font-semibold ${classItem.attended ? 'bg-emerald-500/10 text-emerald-300' : 'bg-rose-500/10 text-rose-300'}`}>
                              {classItem.attended ? 'Present' : 'Absent'}
                            </span>
                          </div>
                          <p className="text-sm text-slate-400 mt-2">{classItem.schedule_time || 'No time'} · Room {classItem.room_number || 'TBD'}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="grid gap-6 lg:grid-cols-2 mb-6">
          <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/30">
            <h2 className="text-xl font-semibold mb-4">Activity Summary</h2>
            <div className="space-y-3 text-slate-300">
              <p>Entries recorded: <strong>{attendanceHistory.length}</strong></p>
              <p>Latest score: <strong>{attendanceHistory[0]?.fraud_score ?? 'N/A'}</strong></p>
              <p>Flagged events: <strong>{attendanceHistory.filter((item) => item.is_flagged).length}</strong></p>
            </div>
          </div>
          <Chart data={chartDataArray} type="bar" title="Fraud Trend" />
        </div>

        <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/40">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Attendance Records</h2>
            <span className="text-sm text-slate-400">Most recent first</span>
          </div>
          <Table data={attendanceHistory} columns={tableColumns} />
        </div>
      </div>
    </div>
  )
}

export default History