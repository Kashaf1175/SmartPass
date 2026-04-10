import { useState, useEffect } from 'react'
import { markAttendance, fetchClasses } from '../services/attendanceService'

function AttendanceButton({ onAttendanceMarked }) {
  const [loading, setLoading] = useState(false)
  const [classes, setClasses] = useState([])
  const [selectedClassId, setSelectedClassId] = useState('')
  const [location, setLocation] = useState({ latitude: 19.1116656, longitude: 77.2929891 })
  const [deviceId, setDeviceId] = useState('device-001')
  const [loadError, setLoadError] = useState('')

  useEffect(() => {
    const loadClasses = async () => {
      try {
        console.log('Loading classes...')
        const token = localStorage.getItem('token')
        console.log('Token exists:', !!token)
        
        const classesData = await fetchClasses()
        console.log('Classes data received:', classesData)
        
        setClasses(classesData)
        if (classesData.length > 0) {
          setSelectedClassId(classesData[0]._id)
        }
      } catch (error) {
        console.error('Error loading classes:', error)
        console.error('Error response:', error?.response)
        setLoadError(error?.response?.data?.detail || error.message || 'Unable to load classes')
      }
    }
    loadClasses()
  }, [])

  const handleMarkAttendance = async () => {
    if (!selectedClassId) {
      alert('Please select a class first.')
      return
    }

    setLoading(true)
    try {
      let finalLocation = location

      // Try to get real location (with proper async handling)
      if (navigator.geolocation) {
        await new Promise((resolve) => {
          navigator.geolocation.getCurrentPosition(
            (position) => {
              finalLocation = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
              }
              setLocation(finalLocation)
              resolve()
            },
            () => {
              // Use default location if geolocation fails
              console.log('Using default location')
              resolve()
            },
            { timeout: 5000 }
          )
        })
      }

      const result = await markAttendance({
        class_id: selectedClassId,
        latitude: finalLocation.latitude,
        longitude: finalLocation.longitude,
        device_id: deviceId,
      })

      onAttendanceMarked(result)
    } catch (error) {
      console.error('Error marking attendance:', error)
      console.error('Error details:', error?.response?.data)
      alert(error?.response?.data?.detail || 'Failed to mark attendance. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm text-slate-300 mb-2">Select Class</label>
        <select
          value={selectedClassId}
          onChange={(e) => setSelectedClassId(e.target.value)}
          className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100"
        >
          <option value="">Choose a class...</option>
          {classes.map((classItem) => (
            <option key={classItem._id} value={classItem._id}>
              {classItem.name} - {classItem.subject?.name || 'Unknown Subject'}
              {classItem.day_of_week !== undefined ? ` | ${['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][classItem.day_of_week]}` : ''}
              {classItem.week_number ? ` | Week ${classItem.week_number}` : ''}
              {classItem.schedule_time ? ` | ${classItem.schedule_time}` : ''}
            </option>
          ))}
        </select>
        {loadError && <p className="mt-2 text-sm text-rose-400">{loadError}</p>}
        {!loadError && classes.length === 0 && (
          <p className="mt-2 text-sm text-rose-400">No classes available yet. Ask admin to add classes first.</p>
        )}
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label className="block text-sm text-slate-300 mb-2">Latitude</label>
          <input
            type="number"
            step="any"
            value={location.latitude}
            onChange={(e) => setLocation(prev => ({ ...prev, latitude: parseFloat(e.target.value) }))}
            className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100"
          />
        </div>
        <div>
          <label className="block text-sm text-slate-300 mb-2">Longitude</label>
          <input
            type="number"
            step="any"
            value={location.longitude}
            onChange={(e) => setLocation(prev => ({ ...prev, longitude: parseFloat(e.target.value) }))}
            className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100"
          />
        </div>
      </div>
      <div>
        <label className="block text-sm text-slate-300 mb-2">Device ID</label>
        <input
          type="text"
          value={deviceId}
          onChange={(e) => setDeviceId(e.target.value)}
          className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100"
        />
      </div>
      <button
        onClick={handleMarkAttendance}
        disabled={loading || !selectedClassId}
        className="w-full rounded-2xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? 'Marking Attendance...' : 'Mark Attendance'}
      </button>
    </div>
  )
}

export default AttendanceButton