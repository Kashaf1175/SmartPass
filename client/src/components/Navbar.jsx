import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'

function Navbar() {
  const { user, logout } = useContext(AuthContext)

  return (
    <nav className="bg-slate-900 border-b border-slate-700 px-4 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-xl font-semibold text-cyan-300">SmartPass</h1>
          <span className="text-slate-400">Fraud Detection System</span>
        </div>
        <div className="flex items-center space-x-4">
          {user && (
            <>
              <span className="text-slate-300">Welcome, {user.email}</span>
              <span className="rounded-full border border-slate-700 px-3 py-1 text-sm">
                {user.role}
              </span>
              <button
                onClick={logout}
                className="rounded-lg bg-slate-800 px-4 py-2 text-slate-100 hover:bg-slate-700"
              >
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar