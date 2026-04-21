import { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { supabase } from './services/supabaseClient'

import Navbar from './components/Navbar'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Browse from './pages/Browse'
import Settings from './pages/Settings'
import Login from './pages/Login'
import Signup from './pages/Signup'
import ResetPassword from './pages/ResetPassword'

export default function App() {
  const [session, setSession] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setLoading(false)
    })

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
    })

    return () => subscription.unsubscribe()
  }, [])

  if (loading) return null

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-white text-slate-900 font-sans selection:bg-blue-100">
        <Navbar session={session} />
        
        <Routes>
          <Route path="/" element={session ? <Navigate to="/dashboard" /> : <Home />} />

          <Route path="/login" element={session ? <Navigate to="/dashboard" /> : <Login />} />
          <Route path="/signup" element={session ? <Navigate to="/dashboard" /> : <Signup />} />
          <Route path="/reset-password" element={session ? <Navigate to="/dashboard" /> : <ResetPassword />} />

          <Route
            path="/dashboard"
            element={session ? <Dashboard /> : <Navigate to="/" />}
          />
          <Route
            path="/settings"
            element={session ? <Settings /> : <Navigate to="/" />}
          />
          <Route
            path="/browse"
            element={session ? <Browse /> : <Navigate to="/" />}
          />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
