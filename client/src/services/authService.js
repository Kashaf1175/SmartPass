import { loginUser, signupUser } from './api'

class AuthService {
  constructor() {
    this.token = localStorage.getItem('token')
    this.user = null
  }

  async login(email, password) {
    const response = await loginUser(email, password)
    this.token = response.access_token
    this.user = { email, role: response.role }
    localStorage.setItem('token', this.token)
    localStorage.setItem('role', response.role)
    return response
  }

  async signup(email, password, role) {
    const response = await signupUser(email, password, role)
    return response
  }

  logout() {
    this.token = null
    this.user = null
    localStorage.removeItem('token')
    localStorage.removeItem('role')
  }

  getToken() {
    return this.token
  }

  getUser() {
    return this.user
  }

  isAuthenticated() {
    return Boolean(this.token)
  }
}

export default new AuthService()