import { useState, useEffect, useContext } from 'react'
import { AuthContext } from '../context/AuthContext'
import { fetchFraudAnalysis, fetchSubjects, fetchClasses, createSubject, createClass, fetchAdminStudentAttendance } from '../services/attendanceService'
import { deleteSubject, updateSubject, deleteClass, updateClass } from '../services/api'
import Navbar from '../components/Navbar'
import Table from '../components/Table'
import Chart from '../components/Chart'
import MapView from '../components/MapView'

function AdminDashboard() {
  const { user } = useContext(AuthContext)
  const [fraudData, setFraudData] = useState({ flagged: [], total_records: 0 })
  const [subjects, setSubjects] = useState([])
  const [classes, setClasses] = useState([])
  const [studentAttendance, setStudentAttendance] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('dashboard')
  const [subjectError, setSubjectError] = useState('')
  const [classError, setClassError] = useState('')
  const [editingSubject, setEditingSubject] = useState(null)
  const [editingClass, setEditingClass] = useState(null)

  // Form states
  const [newSubject, setNewSubject] = useState({ name: '', code: '', description: '' })
  const [newClassData, setNewClassData] = useState({ name: '', subject_id: '', schedule_time: '', room_number: '', day_of_week: '', week_number: '' })

  useEffect(() => {
    const loadData = async () => {
      try {
        const [fraudResult, subjectsResult, classesResult, studentResult] = await Promise.all([
          fetchFraudAnalysis(),
          fetchSubjects(),
          fetchClasses(),
          fetchAdminStudentAttendance()
        ])
        setFraudData(fraudResult)
        setSubjects(subjectsResult)
        setClasses(classesResult)
        setStudentAttendance(studentResult)
      } catch (error) {
        console.error('Error loading data:', error)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  const handleCreateSubject = async (e) => {
    e.preventDefault()
    setSubjectError('')
    try {
      if (editingSubject) {
        const token = localStorage.getItem('token')
        await updateSubject(token, editingSubject._id, newSubject)
        setEditingSubject(null)
      } else {
        await createSubject(newSubject)
      }
      setNewSubject({ name: '', code: '', description: '' })
      setSubjects(await fetchSubjects())
    } catch (error) {
      console.error('Error saving subject:', error)
      setSubjectError(error?.response?.data?.detail || error.message || 'Failed to save subject')
    }
  }

  const handleCreateClass = async (e) => {
    e.preventDefault()
    setClassError('')
    try {
      if (editingClass) {
        const token = localStorage.getItem('token')
        await updateClass(token, editingClass._id, newClassData)
        setEditingClass(null)
      } else {
        await createClass(newClassData)
      }
      setNewClassData({ name: '', subject_id: '', schedule_time: '', room_number: '', day_of_week: '', week_number: '' })
      setClasses(await fetchClasses())
    } catch (error) {
      console.error('Error saving class:', error)
      setClassError(error?.response?.data?.detail || error.message || 'Failed to save class')
    }
  }

  const handleDeleteSubject = async (subjectId) => {
    if (window.confirm('Are you sure you want to delete this subject?')) {
      try {
        const token = localStorage.getItem('token')
        await deleteSubject(token, subjectId)
        setSubjects(await fetchSubjects())
      } catch (error) {
        alert('Failed to delete subject: ' + (error?.response?.data?.detail || error.message))
      }
    }
  }

  const handleDeleteClass = async (classId) => {
    if (window.confirm('Are you sure you want to delete this class?')) {
      try {
        const token = localStorage.getItem('token')
        await deleteClass(token, classId)
        setClasses(await fetchClasses())
      } catch (error) {
        alert('Failed to delete class: ' + (error?.response?.data?.detail || error.message))
      }
    }
  }

  const handleEditSubject = (subject) => {
    setEditingSubject(subject)
    setNewSubject({ name: subject.name, code: subject.code, description: subject.description })
  }

  const handleEditClass = (classItem) => {
    setEditingClass(classItem)
    setNewClassData({ 
      name: classItem.name, 
      subject_id: classItem.subject_id, 
      schedule_time: classItem.schedule_time, 
      room_number: classItem.room_number,
      day_of_week: classItem.day_of_week || '',
      week_number: classItem.week_number || ''
    })
  }

  const chartData = [
    { name: 'Flagged', value: fraudData.flagged.length },
    { name: 'Normal', value: Math.max(0, fraudData.total_records - fraudData.flagged.length) },
  ]

  const tableColumns = [
    { header: 'Timestamp', key: 'timestamp', render: (value) => new Date(value).toLocaleString() },
    { header: 'Student ID', key: 'user_id' },
    { header: 'Score', key: 'fraud_score' },
    { header: 'Location', key: 'latitude', render: (value, row) => `${value?.toFixed(5)}, ${row.longitude?.toFixed(5)}` },
    { header: 'Device', key: 'device_id', render: (value) => value || 'unknown' },
  ]

  const subjectColumns = [
    { header: 'Name', key: 'name' },
    { header: 'Code', key: 'code' },
    { header: 'Description', key: 'description' },
    { 
      header: 'Actions', 
      key: '_id',
      render: (value, row) => (
        <div className="flex gap-2">
          <button onClick={() => handleEditSubject(row)} className="text-blue-400 hover:text-blue-300 text-sm">Edit</button>
          <button onClick={() => handleDeleteSubject(value)} className="text-red-400 hover:text-red-300 text-sm">Delete</button>
        </div>
      )
    },
  ]

  const classColumns = [
    { header: 'Name', key: 'name' },
    { header: 'Subject', key: 'subject', render: (value) => value?.name || 'Unknown' },
    { header: 'Schedule', key: 'schedule_time' },
    { header: 'Room', key: 'room_number' },
    { header: 'Day', key: 'day_of_week', render: (value) => value !== undefined ? ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][value] : 'Not set' },
    { header: 'Week of Month', key: 'week_number', render: (value) => value || 'Not set' },
    { 
      header: 'Actions', 
      key: '_id',
      render: (value, row) => (
        <div className="flex gap-2">
          <button onClick={() => handleEditClass(row)} className="text-blue-400 hover:text-blue-300 text-sm">Edit</button>
          <button onClick={() => handleDeleteClass(value)} className="text-red-400 hover:text-red-300 text-sm">Delete</button>
        </div>
      )
    },
  ]

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
          <h1 className="text-3xl font-semibold">Admin Console</h1>
          <p className="text-slate-400 mt-1">Manage subjects, classes, and monitor fraud detection.</p>
        </header>

        {/* Tab Navigation */}
        <div className="flex space-x-1 mb-6 bg-slate-800 p-1 rounded-2xl">
          {['dashboard', 'students', 'subjects', 'classes'].map((tab) => (
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

        {activeTab === 'dashboard' && (
          <>
            <div className="grid gap-4 lg:grid-cols-3 mb-6">
              <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/30">
                <h3 className="text-sm uppercase text-slate-500">Total Records</h3>
                <p className="mt-3 text-3xl font-semibold text-cyan-300">{fraudData.total_records}</p>
              </div>
              <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/30">
                <h3 className="text-sm uppercase text-slate-500">Flagged Events</h3>
                <p className="mt-3 text-3xl font-semibold text-rose-400">{fraudData.flagged.length}</p>
              </div>
              <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/30">
                <h3 className="text-sm uppercase text-slate-500">Normal Events</h3>
                <p className="mt-3 text-3xl font-semibold text-emerald-400">{fraudData.total_records - fraudData.flagged.length}</p>
              </div>
            </div>

            <div className="grid gap-6 lg:grid-cols-2 mb-6">
              <Chart data={chartData} type="pie" title="Fraud Distribution" />
              <MapView locations={fraudData.flagged} />
            </div>

            <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/40">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold">Real-Time Fraud Alerts</h2>
                <span className="text-sm text-slate-400">Latest suspicious activities</span>
              </div>
              <div className="space-y-3">
                {fraudData.flagged.slice(0, 5).map((alert, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
                    <div>
                      <p className="text-sm font-semibold text-red-400">
                        Student: {alert.user_id}
                      </p>
                      <p className="text-xs text-slate-400">
                        {new Date(alert.timestamp).toLocaleString()}
                      </p>
                      <p className="text-xs text-slate-500">
                        Score: {alert.fraud_score} | Reasons: {alert.fraud_reasons?.join(', ') || 'N/A'}
                      </p>
                    </div>
                    <div className="text-red-400">
                      🚨
                    </div>
                  </div>
                ))}
                {fraudData.flagged.length === 0 && (
                  <p className="text-center text-slate-500 py-4">No recent alerts</p>
                )}
              </div>
            </div>
          </>
        )}

        {activeTab === 'students' && (
          <div className="space-y-6">
            <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/40">
              <h2 className="text-xl font-semibold mb-4">Student Attendance Overview</h2>
              <div className="space-y-4">
                {studentAttendance.map((student, index) => (
                  <div key={index} className={`rounded-2xl border p-4 ${
                    student.at_risk 
                      ? 'border-red-500/50 bg-red-500/5' 
                      : 'border-slate-700 bg-slate-800'
                  }`}>
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h3 className="font-semibold text-lg">{student.student_email}</h3>
                        <p className="text-sm text-slate-400">ID: {student.student_id}</p>
                      </div>
                      <div className="text-right">
                        <div className={`text-2xl font-bold ${
                          student.overall_percentage >= 75 ? 'text-emerald-400' :
                          student.overall_percentage >= 50 ? 'text-yellow-400' :
                          'text-red-400'
                        }`}>
                          {student.overall_percentage}%
                        </div>
                        <p className="text-xs text-slate-400">Overall</p>
                        {student.at_risk && (
                          <p className="text-xs text-red-400 font-semibold">⚠️ DETENTION RISK</p>
                        )}
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 mb-3">
                      <div className="text-center">
                        <p className="text-lg font-semibold text-cyan-400">{student.total_attended}</p>
                        <p className="text-xs text-slate-400">Classes Attended</p>
                      </div>
                      <div className="text-center">
                        <p className="text-lg font-semibold text-cyan-400">{student.total_possible}</p>
                        <p className="text-xs text-slate-400">Classes Scheduled</p>
                      </div>
                      <div className="text-center">
                        <p className="text-lg font-semibold text-emerald-400">{student.weekly_percentage ?? 0}%</p>
                        <p className="text-xs text-slate-400">This Week</p>
                      </div>
                      <div className="text-center">
                        <p className="text-lg font-semibold text-rose-400">{student.flagged_attendances ?? 0}</p>
                        <p className="text-xs text-slate-400">Flagged Logins</p>
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="text-sm font-semibold mb-2">Current Week of Month (Week {student.current_week_of_month}) - {student.month}</h4>
                      <div className="space-y-1">
                        {Object.entries(student.weekly_subjects).map(([subject, stats]) => (
                          <div key={subject} className="flex justify-between text-sm">
                            <span>{subject}</span>
                            <span className={
                              (stats.attended / Math.max(stats.total, 1)) >= 0.75 ? 'text-emerald-400' :
                              (stats.attended / Math.max(stats.total, 1)) >= 0.5 ? 'text-yellow-400' :
                              'text-red-400'
                            }>
                              {stats.attended}/{stats.total}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'subjects' && (
          <div className="space-y-6">
            <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/40">
              <h2 className="text-xl font-semibold mb-4">{editingSubject ? 'Edit Subject' : 'Create New Subject'}</h2>
              <form onSubmit={handleCreateSubject} className="space-y-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="block text-sm text-slate-300 mb-2">Subject Name</label>
                    <input
                      type="text"
                      value={newSubject.name}
                      onChange={(e) => setNewSubject(prev => ({ ...prev, name: e.target.value }))}
                      className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-slate-300 mb-2">Subject Code</label>
                    <input
                      type="text"
                      value={newSubject.code}
                      onChange={(e) => setNewSubject(prev => ({ ...prev, code: e.target.value }))}
                      className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100"
                      required
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm text-slate-300 mb-2">Description</label>
                  <textarea
                    value={newSubject.description}
                    onChange={(e) => setNewSubject(prev => ({ ...prev, description: e.target.value }))}
                    className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100"
                    rows="3"
                  />
                </div>
                {subjectError && <p className="text-rose-400 text-sm">{subjectError}</p>}
                <button
                  type="submit"
                  className="w-full rounded-2xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400"
                >
                  {editingSubject ? 'Update Subject' : 'Create Subject'}
                </button>
                {editingSubject && (
                  <button
                    type="button"
                    onClick={() => {
                      setEditingSubject(null)
                      setNewSubject({ name: '', code: '', description: '' })
                    }}
                    className="w-full rounded-2xl bg-slate-700 px-5 py-3 font-semibold text-slate-100 hover:bg-slate-600"
                  >
                    Cancel Edit
                  </button>
                )}
              </form>
            </div>

            <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/40">
              <h2 className="text-xl font-semibold mb-4">All Subjects</h2>
              <Table data={subjects} columns={subjectColumns} />
            </div>
          </div>
        )}

        {activeTab === 'classes' && (
          <div className="space-y-6">
            <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/40">
              <h2 className="text-xl font-semibold mb-4">{editingClass ? 'Edit Class' : 'Create New Class'}</h2>
              <form onSubmit={handleCreateClass} className="space-y-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="block text-sm text-slate-300 mb-2">Class Name</label>
                    <input
                      type="text"
                      value={newClassData.name}
                      onChange={(e) => setNewClassData(prev => ({ ...prev, name: e.target.value }))}
                      className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-slate-300 mb-2">Subject</label>
                    <select
                      value={newClassData.subject_id}
                      onChange={(e) => setNewClassData(prev => ({ ...prev, subject_id: e.target.value }))}
                      className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100"
                      required
                    >
                      <option value="">Select a subject...</option>
                      {subjects.map((subject) => (
                        <option key={subject._id} value={subject._id}>
                          {subject.name} ({subject.code})
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="block text-sm text-slate-300 mb-2">Schedule Time</label>
                    <input
                      type="time"
                      value={newClassData.schedule_time}
                      onChange={(e) => setNewClassData(prev => ({ ...prev, schedule_time: e.target.value }))}
                      className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-slate-300 mb-2">Room Number</label>
                    <input
                      type="text"
                      value={newClassData.room_number}
                      onChange={(e) => setNewClassData(prev => ({ ...prev, room_number: e.target.value }))}
                      className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100"
                    />
                  </div>
                </div>
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="block text-sm text-slate-300 mb-2">Day of Week</label>
                    <select
                      value={newClassData.day_of_week}
                      onChange={(e) => setNewClassData(prev => ({ ...prev, day_of_week: e.target.value }))}
                      className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100"
                    >
                      <option value="">Select day...</option>
                      <option value="0">Monday</option>
                      <option value="1">Tuesday</option>
                      <option value="2">Wednesday</option>
                      <option value="3">Thursday</option>
                      <option value="4">Friday</option>
                      <option value="5">Saturday</option>
                      <option value="6">Sunday</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm text-slate-300 mb-2">Week of Month</label>
                    <input
                      type="number"
                      min="1"
                      max="5"
                      value={newClassData.week_number}
                      onChange={(e) => setNewClassData(prev => ({ ...prev, week_number: e.target.value }))}
                      className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100"
                      placeholder="1-5"
                    />
                  </div>
                </div>
                {classError && <p className="text-rose-400 text-sm">{classError}</p>}
                <button
                  type="submit"
                  className="w-full rounded-2xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400"
                >
                  {editingClass ? 'Update Class' : 'Create Class'}
                </button>
                {editingClass && (
                  <button
                    type="button"
                    onClick={() => {
                      setEditingClass(null)
                      setNewClassData({ name: '', subject_id: '', schedule_time: '', room_number: '', day_of_week: '', week_number: '' })
                    }}
                    className="w-full rounded-2xl bg-slate-700 px-5 py-3 font-semibold text-slate-100 hover:bg-slate-600"
                  >
                    Cancel Edit
                  </button>
                )}
              </form>
            </div>

            <div className="rounded-3xl border border-slate-700 bg-slate-900 p-6 shadow-lg shadow-slate-950/40">
              <h2 className="text-xl font-semibold mb-4">All Classes</h2>
              <Table data={classes} columns={classColumns} />
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default AdminDashboard