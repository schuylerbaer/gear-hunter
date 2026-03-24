import { useState, useEffect } from 'react'
import { supabase } from './services/supabaseClient'
import Auth from './pages/Auth'
import GearFeed from './pages/GearFeed'

function App() {
  const [session, setSession] = useState<any>(null)

  useEffect(() => {
    // Check if logged in
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
    })

    // Listen for login/logout events
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
    })

    return () => subscription.unsubscribe()
  }, [])

  // If no session exists, show Auth. Otherwise, show the GearFeed.
  return (
    <div className="min-h-screen bg-base-200">
      {!session ? <Auth /> : <GearFeed />}
    </div>
  )
}

export default App
