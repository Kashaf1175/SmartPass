import { useState, useContext } from 'react'
import { AuthContext } from '../context/AuthContext'

function Signup() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('student')
  const [error, setError] = useState('')
  const { signup } = useContext(AuthContext)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await signup(email, password, role)
      alert('Signup successful! Please login.')
      window.location.hash = '#login'
    } catch (error) {
      console.error('Signup error:', error)
      let errorMsg = 'Signup failed. Please try again.'
      
      if (error.message?.includes('Network Error')) {
        errorMsg = error.message
      } else if (error.response?.data?.detail) {
        errorMsg = error.response.data.detail
      } else if (error.message) {
        errorMsg = error.message
      }
      
      setError(errorMsg)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-md bg-slate-950/80 border border-slate-700 rounded-3xl p-8 shadow-2xl shadow-slate-900">
        <h1 className="text-3xl font-semibold mb-6 text-cyan-300">Create Account</h1>
        
        {error && (
          <div className="mb-4 p-3 bg-red-900/30 border border-red-600 rounded-lg text-red-200 text-sm">
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-slate-300 mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-2xl border border-slate-700 bg-slate-900 px-4 py-3 text-slate-100"
              required
            />
          </div>
          <div>
            <label className="block text-slate-300 mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-2xl border border-slate-700 bg-slate-900 px-4 py-3 text-slate-100"
              required
            />
          </div>
          <div>
            <label className="block text-slate-300 mb-2">Role</label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="w-full rounded-2xl border border-slate-700 bg-slate-900 px-4 py-3 text-slate-100"
            >
              <option value="student">Student</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <button
            type="submit"
            className="w-full rounded-2xl bg-cyan-500 px-5 py-3 text-slate-950 font-semibold hover:bg-cyan-400"
          >
            Sign Up
          </button>
        </form>
        <div className="mt-4 text-center">
          <button
            onClick={() => window.location.hash = '#login'}
            className="text-sm text-slate-400 hover:text-slate-100"
          >
            Already have an account?
          </button>
        </div>
      </div>
    </div>
  )
}

export default Signup