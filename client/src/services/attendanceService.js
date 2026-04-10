import { markAttendance as apiMarkAttendance, fetchAttendance as apiFetchAttendance, fetchWeeklyAttendance as apiFetchWeeklyAttendance, fetchOverallAttendance as apiFetchOverallAttendance, fetchAdminStudentAttendance as apiFetchAdminStudentAttendance, fetchFraudAnalysis as apiFetchFraudAnalysis, fetchSubjects as apiFetchSubjects, fetchClasses as apiFetchClasses, createSubject as apiCreateSubject, createClass as apiCreateClass } from './api'

class AttendanceService {
  getToken() {
    return localStorage.getItem('token')
  }

  async markAttendance(attendanceData) {
    const token = this.getToken()
    return await apiMarkAttendance(token, attendanceData)
  }

  async getAttendance() {
    const token = this.getToken()
    return await apiFetchAttendance(token)
  }

  async getWeeklyAttendance() {
    const token = this.getToken()
    return await apiFetchWeeklyAttendance(token)
  }

  async getOverallAttendance() {
    const token = this.getToken()
    return await apiFetchOverallAttendance(token)
  }

  async getAdminStudentAttendance() {
    const token = this.getToken()
    return await apiFetchAdminStudentAttendance(token)
  }

  async getFraudAnalysis() {
    const token = this.getToken()
    return await apiFetchFraudAnalysis(token)
  }

  async getSubjects() {
    const token = this.getToken()
    return await apiFetchSubjects(token)
  }

  async getClasses() {
    const token = this.getToken()
    return await apiFetchClasses(token)
  }

  async createSubject(subjectData) {
    const token = this.getToken()
    return await apiCreateSubject(token, subjectData)
  }

  async createClass(classData) {
    const token = this.getToken()
    return await apiCreateClass(token, classData)
  }
}

// Named exports that automatically handle token retrieval
export const markAttendance = async (attendanceData) => {
  const token = localStorage.getItem('token')
  return await apiMarkAttendance(token, attendanceData)
}

export const fetchAttendance = async () => {
  const token = localStorage.getItem('token')
  return await apiFetchAttendance(token)
}

export const fetchWeeklyAttendance = async () => {
  const token = localStorage.getItem('token')
  return await apiFetchWeeklyAttendance(token)
}

export const fetchOverallAttendance = async () => {
  const token = localStorage.getItem('token')
  return await apiFetchOverallAttendance(token)
}

export const fetchAdminStudentAttendance = async () => {
  const token = localStorage.getItem('token')
  return await apiFetchAdminStudentAttendance(token)
}

export const fetchFraudAnalysis = async () => {
  const token = localStorage.getItem('token')
  return await apiFetchFraudAnalysis(token)
}

export const fetchSubjects = async () => {
  const token = localStorage.getItem('token')
  return await apiFetchSubjects(token)
}

export const fetchClasses = async () => {
  const token = localStorage.getItem('token')
  return await apiFetchClasses(token)
}

export const createSubject = async (subjectData) => {
  const token = localStorage.getItem('token')
  return await apiCreateSubject(token, subjectData)
}

export const createClass = async (classData) => {
  const token = localStorage.getItem('token')
  return await apiCreateClass(token, classData)
}

export default new AttendanceService()