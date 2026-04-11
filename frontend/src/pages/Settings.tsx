import { useState, useEffect } from 'react'
import { supabase } from '../services/supabaseClient'
import { usePageTitle } from '../hooks/usePageTitle'

export default function Settings() {
  usePageTitle('Settings')
  const [currentEmail, setCurrentEmail] = useState('')
  const [newEmail, setNewEmail] = useState('')
  const [emailLoading, setEmailLoading] = useState(false)
  const [emailMessage, setEmailMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)

  const [newPassword, setNewPassword] = useState('')
  const [confirmNewPassword, setConfirmNewPassword] = useState('')
  const [passwordLoading, setPasswordLoading] = useState(false)
  const [passwordMessage, setPasswordMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)

  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)

  useEffect(() => {
    supabase.auth.getUser().then(({ data: { user } }) => {
      if (user?.email) setCurrentEmail(user.email)
    })
  }, [])

  const handleUpdateEmail = async (e: React.FormEvent) => {
    e.preventDefault()
    setEmailLoading(true)
    setEmailMessage(null)

    const { error } = await supabase.auth.updateUser({ email: newEmail })

    if (error) {
      setEmailMessage({ type: 'error', text: error.message })
    } else {
      setEmailMessage({ type: 'success', text: 'Confirmation link sent to both old and new email addresses.' })
      setNewEmail('')
    }
    setEmailLoading(false)
  }

  const handleUpdatePassword = async (e: React.FormEvent) => {
    e.preventDefault()
    setPasswordLoading(true)
    setPasswordMessage(null)

    if (newPassword !== confirmNewPassword) {
      setPasswordMessage({ type: 'error', text: 'Passwords do not match!' })
      setPasswordLoading(false)
      return
    }

    const { error } = await supabase.auth.updateUser({ password: newPassword })

    if (error) {
      setPasswordMessage({ type: 'error', text: error.message })
    } else {
      setPasswordMessage({ type: 'success', text: 'Password successfully updated.' })
      setNewPassword('')
      setConfirmNewPassword('')
    }
    setPasswordLoading(false)
  }

  const executeDelete = async () => {
    const { error } = await supabase.rpc('delete_user')

    if (error) {
      alert(`Failed to delete account: ${error.message}`)
      return
    }

    await supabase.auth.signOut()
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-12">
      
      <div className="mb-10">
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Settings</h1>
        <p className="text-slate-500 mt-1">Manage your account preferences and security.</p>
      </div>

      <div className="space-y-8">
        
        {/* --- Update Email Card --- */}
        <div className="bg-white p-8 rounded-3xl shadow-[0_4px_20px_rgb(0,0,0,0.03)] border border-slate-100">
          <h2 className="text-xl font-bold text-slate-900 mb-1">Email Address</h2>
          <p className="text-sm text-slate-500 mb-6">Your current email is <span className="font-semibold text-slate-900">{currentEmail}</span></p>
          
          {emailMessage && (
            <div className={`mb-6 p-4 rounded-2xl text-sm border font-medium ${emailMessage.type === 'error' ? 'bg-red-50 text-red-600 border-red-100' : 'bg-green-50 text-green-700 border-green-100'}`}>
              {emailMessage.text}
            </div>
          )}

          <form onSubmit={handleUpdateEmail} className="flex flex-col sm:flex-row gap-4">
            <input
              type="email"
              required
              value={newEmail}
              onChange={(e) => setNewEmail(e.target.value)}
              className="flex-1 px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all"
              placeholder="Enter new email address"
            />
            <button
              type="submit"
              disabled={emailLoading || !newEmail}
              className="bg-slate-900 text-white font-semibold px-8 py-3 rounded-full hover:bg-slate-800 transition-all disabled:opacity-50 whitespace-nowrap"
            >
              {emailLoading ? 'Updating...' : 'Update Email'}
            </button>
          </form>
        </div>

        {/* --- Update Password Card --- */}
        <div className="bg-white p-8 rounded-3xl shadow-[0_4px_20px_rgb(0,0,0,0.03)] border border-slate-100">
          <h2 className="text-xl font-bold text-slate-900 mb-1">Change Password</h2>
          <p className="text-sm text-slate-500 mb-6">Ensure your account is using a long, random password to stay secure.</p>
          
          {passwordMessage && (
            <div className={`mb-6 p-4 rounded-2xl text-sm border font-medium ${passwordMessage.type === 'error' ? 'bg-red-50 text-red-600 border-red-100' : 'bg-green-50 text-green-700 border-green-100'}`}>
              {passwordMessage.text}
            </div>
          )}

          {/* --- UPDATED FORM LAYOUT --- */}
          <form onSubmit={handleUpdatePassword} className="flex flex-col gap-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <input
                type="password"
                required
                minLength={6}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all"
                placeholder="New password (min. 6 chars)"
              />
              <input
                type="password"
                required
                minLength={6}
                value={confirmNewPassword}
                onChange={(e) => setConfirmNewPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all"
                placeholder="Confirm new password"
              />
            </div>
            <button
              type="submit"
              disabled={passwordLoading || !newPassword || !confirmNewPassword}
              className="w-full sm:w-auto self-start bg-slate-900 text-white font-semibold px-8 py-3 rounded-full hover:bg-slate-800 transition-all disabled:opacity-50 whitespace-nowrap"
            >
              {passwordLoading ? 'Updating...' : 'Update Password'}
            </button>
          </form>
        </div>

        {/* --- Danger Zone Card --- */}
        <div className="bg-red-50/50 p-8 rounded-3xl border border-red-100 mt-12">
          <h2 className="text-xl font-bold text-red-700 mb-1">Danger Zone</h2>
          <p className="text-sm text-red-600/80 mb-6">Permanently delete your account and all of your active gear alerts. This action cannot be undone.</p>
          
          <button
            onClick={() => setIsDeleteModalOpen(true)}
            className="bg-red-600 text-white font-semibold px-8 py-3 rounded-full hover:bg-red-700 transition-all shadow-md hover:shadow-red-500/30 whitespace-nowrap"
          >
            Delete Account
          </button>
        </div>

      </div>

      {/* --- Delete Modal --- */}
      {isDeleteModalOpen && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl p-8 w-full max-w-md shadow-2xl border border-slate-100 text-center">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            </div>
            <h2 className="text-2xl font-bold text-slate-900 mb-2 tracking-tight">Are you absolutely sure?</h2>
            <p className="text-slate-500 mb-8">
              This will permanently delete your account and remove all of your active gear tracking alerts. This cannot be undone.
            </p>
            
            <div className="flex gap-3">
              <button 
                onClick={() => setIsDeleteModalOpen(false)}
                className="flex-1 bg-slate-100 text-slate-700 font-semibold py-3.5 rounded-full hover:bg-slate-200 transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={executeDelete}
                className="flex-1 bg-red-600 text-white font-semibold py-3.5 rounded-full hover:bg-red-700 transition-all shadow-md hover:shadow-red-500/30"
              >
                Yes, delete it
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
