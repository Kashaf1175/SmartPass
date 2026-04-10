import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const API = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 5000,
})

// Add error interceptor to catch network errors
API.interceptors.response.use(
  response => response,
  error => {
    if (!error.response) {
      error.message = `Network Error: Cannot reach backend at ${API_BASE_URL}. Make sure the server is running.`
    }
    return Promise.reject(error)
  }
)

export const loginUser = async (email, password) => {
  const params = new URLSearchParams()
  params.append('username', email)
  params.append('password', password)
  const response = await API.post('/auth/login', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return response.data
}

export const signupUser = async (email, password, role) => {
  const response = await API.post('/auth/signup', { email, password, role })
  return response.data
}

export const markAttendance = async (token, attendance) => {
  const response = await API.post('/attendance/mark-attendance', attendance, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const fetchAttendance = async (token) => {
  const response = await API.get('/attendance/get-attendance', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const fetchWeeklyAttendance = async (token) => {
  const response = await API.get('/attendance/student-weekly-attendance', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const fetchOverallAttendance = async (token) => {
  const response = await API.get('/attendance/student-overall-attendance', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const fetchAdminStudentAttendance = async (token) => {
  const response = await API.get('/attendance/admin-student-attendance', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const fetchFraudAnalysis = async (token) => {
  const response = await API.get('/fraud/fraud-stats', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

// Subject and Class API calls
export const fetchSubjects = async (token) => {
  const response = await API.get('/classes/subjects', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const fetchClasses = async (token) => {
  const response = await API.get('/classes/classes', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const createSubject = async (token, subjectData) => {
  const response = await API.post('/classes/subjects', subjectData, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const createClass = async (token, classData) => {
  const response = await API.post('/classes/classes', classData, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const deleteSubject = async (token, subjectId) => {
  const response = await API.delete(`/classes/subjects/${subjectId}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const updateSubject = async (token, subjectId, subjectData) => {
  const response = await API.put(`/classes/subjects/${subjectId}`, subjectData, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const deleteClass = async (token, classId) => {
  const response = await API.delete(`/classes/classes/${classId}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

export const updateClass = async (token, classId, classData) => {
  const response = await API.put(`/classes/classes/${classId}`, classData, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return response.data
}

