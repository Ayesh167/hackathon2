'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Button from '@/components/Button';
import { apiClient } from '@/lib/api';

// Simple function to decode JWT token to get user ID
const getUserIdFromToken = (): string | null => {
  const token = localStorage.getItem('jwt_token');
  if (!token) return null;

  try {
    // Split the token to get the payload part
    const parts = token.split('.');
    if (parts.length !== 3) return null;

    // Decode the payload (second part)
    const payload = parts[1];
    // Add padding if needed
    const paddedPayload = payload + '='.repeat((4 - payload.length % 4) % 4);
    const decodedPayload = atob(paddedPayload);
    const parsedPayload = JSON.parse(decodedPayload);

    // Return the subject (user ID) from the token
    return parsedPayload.sub || null;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

const ProfilePage = () => {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Profile editing state
  const [isEditing, setIsEditing] = useState(false);
  const [editName, setEditName] = useState('');
  const [editEmail, setEditEmail] = useState('');
  const [updating, setUpdating] = useState(false);
  const [updateError, setUpdateError] = useState('');
  
  // Password change modal state
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  const [passwordChangeError, setPasswordChangeError] = useState('');
  const [passwordChanging, setPasswordChanging] = useState(false);
  
  // Active sessions modal state
  const [showSessionsModal, setShowSessionsModal] = useState(false);
  const [sessions, setSessions] = useState<any[]>([]);
  const [loadingSessions, setLoadingSessions] = useState(false);
  
  // 2FA modal state
  const [showTwoFactorModal, setShowTwoFactorModal] = useState(false);
  const [twoFactorStep, setTwoFactorStep] = useState<'setup' | 'verify' | 'success'>('setup');
  const [verificationToken, setVerificationToken] = useState('');
  const [twoFactorError, setTwoFactorError] = useState('');
  const [twoFactorLoading, setTwoFactorLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('jwt_token');
    if (!token) {
      router.push('/login');
      return;
    }

    const fetchUserDetails = async () => {
      try {
        setLoading(true);
        const response = await apiClient.getUserDetails();
        
        if (response.error) {
          setError(response.error);
        } else if (response.data) {
          setUser(response.data);
          // Initialize edit fields with current user data
          setEditName(response.data.name || '');
          setEditEmail(response.data.email || '');
        } else {
          setError('Failed to fetch user details');
        }
      } catch (err) {
        console.error('Error fetching user details:', err);
        setError('An unexpected error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchUserDetails();
  }, [router]);

  const handleLogout = () => {
    // Clear the token from localStorage
    apiClient.logout();

    // Redirect to login page
    router.push('/login');
    router.refresh(); // Refresh to update navbar
  };

  const handleEditToggle = () => {
    if (isEditing) {
      // Cancel editing
      setEditName(user?.name || '');
      setEditEmail(user?.email || '');
      setIsEditing(false);
      setUpdateError('');
    } else {
      // Start editing
      setIsEditing(true);
    }
  };

  const handleSaveProfile = async () => {
    if (!editName.trim() || !editEmail.trim()) {
      setUpdateError('Name and email are required');
      return;
    }

    setUpdating(true);
    setUpdateError('');

    try {
      const response = await apiClient.updateUser({
        name: editName,
        email: editEmail
      });

      if (response.error) {
        setUpdateError(response.error);
      } else if (response.data) {
        // Update the user state with new data
        setUser(response.data);
        // Also update the edit fields to reflect the changes
        setEditName(response.data.name);
        setEditEmail(response.data.email);
        setIsEditing(false);
      }
    } catch (err) {
      console.error('Error updating profile:', err);
      setUpdateError('An unexpected error occurred');
    } finally {
      setUpdating(false);
    }
  };

  const handleChangePassword = async () => {
    // Reset previous errors
    setPasswordChangeError('');
    
    // Validate inputs
    if (!currentPassword.trim() || !newPassword.trim() || !confirmNewPassword.trim()) {
      setPasswordChangeError('All fields are required');
      return;
    }
    
    if (newPassword !== confirmNewPassword) {
      setPasswordChangeError('New passwords do not match');
      return;
    }
    
    if (newPassword.length < 6) {
      setPasswordChangeError('New password must be at least 6 characters long');
      return;
    }
    
    setPasswordChanging(true);
    
    try {
      const response = await apiClient.changePassword({
        current_password: currentPassword,
        new_password: newPassword
      });
      
      if (response.error) {
        setPasswordChangeError(response.error);
      } else if (response.data) {
        // Success - close modal and reset fields
        setShowPasswordModal(false);
        setCurrentPassword('');
        setNewPassword('');
        setConfirmNewPassword('');
        setPasswordChangeError('');
        alert('Password changed successfully!');
      }
    } catch (err) {
      console.error('Error changing password:', err);
      setPasswordChangeError('An unexpected error occurred');
    } finally {
      setPasswordChanging(false);
    }
  };

  // Function to load active sessions
  const loadActiveSessions = async () => {
    setLoadingSessions(true);
    try {
      const response = await apiClient.getActiveSessions();
      if (response.error) {
        console.error('Error loading sessions:', response.error);
      } else if (response.data) {
        setSessions(response.data.sessions || []);
      }
    } catch (err) {
      console.error('Error loading sessions:', err);
    } finally {
      setLoadingSessions(false);
    }
  };

  // Function to handle showing the sessions modal
  const handleShowSessions = async () => {
    await loadActiveSessions();
    setShowSessionsModal(true);
  };

  // Function to revoke a session
  const handleRevokeSession = async (sessionId: string) => {
    if (!window.confirm(`Are you sure you want to revoke session ${sessionId}?`)) {
      return;
    }

    try {
      const response = await apiClient.revokeSession(sessionId);
      if (response.error) {
        alert(`Error revoking session: ${response.error}`);
      } else {
        alert(response.data?.message || 'Session revoked successfully');
        // Reload sessions
        await loadActiveSessions();
      }
    } catch (err) {
      console.error('Error revoking session:', err);
      alert('An error occurred while revoking the session');
    }
  };

  // Function to start 2FA setup
  const handleStartTwoFactor = async () => {
    setTwoFactorLoading(true);
    setTwoFactorError('');
    try {
      const response = await apiClient.setupTwoFactor();
      if (response.error) {
        setTwoFactorError(response.error);
      } else {
        setTwoFactorStep('verify');
      }
    } catch (err) {
      console.error('Error starting 2FA setup:', err);
      setTwoFactorError('An error occurred while setting up 2FA');
    } finally {
      setTwoFactorLoading(false);
    }
  };

  // Function to verify 2FA setup
  const handleVerifyTwoFactor = async () => {
    if (!verificationToken.trim()) {
      setTwoFactorError('Please enter the verification token');
      return;
    }

    setTwoFactorLoading(true);
    setTwoFactorError('');
    try {
      const response = await apiClient.verifyTwoFactor(verificationToken);
      if (response.error) {
        setTwoFactorError(response.error);
      } else if (response.data?.success) {
        setTwoFactorStep('success');
      }
    } catch (err) {
      console.error('Error verifying 2FA:', err);
      setTwoFactorError('An error occurred while verifying 2FA');
    } finally {
      setTwoFactorLoading(false);
    }
  };

  // Function to disable 2FA
  const handleDisableTwoFactor = async () => {
    if (!window.confirm('Are you sure you want to disable two-factor authentication?')) {
      return;
    }

    setTwoFactorLoading(true);
    setTwoFactorError('');
    try {
      const response = await apiClient.disableTwoFactor();
      if (response.error) {
        setTwoFactorError(response.error);
      } else {
        alert(response.data?.message || '2FA disabled successfully');
        setShowTwoFactorModal(false);
      }
    } catch (err) {
      console.error('Error disabling 2FA:', err);
      setTwoFactorError('An error occurred while disabling 2FA');
    } finally {
      setTwoFactorLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading profile...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-md p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <div className="mx-auto h-16 w-16 bg-red-100 rounded-full flex items-center justify-center mb-4">
              <span className="text-red-600 text-2xl">⚠️</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-1">Error Loading Profile</h3>
            <p className="text-gray-500 mb-4">{error}</p>
            <Button
              variant="primary"
              size="md"
              onClick={() => router.push('/tasks')}
            >
              Go to Tasks
            </Button>
          </div>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-md p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <div className="mx-auto h-16 w-16 bg-yellow-100 rounded-full flex items-center justify-center mb-4">
              <span className="text-yellow-600 text-2xl">?</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-1">Profile Not Found</h3>
            <p className="text-gray-500 mb-4">Unable to load your profile information.</p>
            <Button
              variant="primary"
              size="md"
              onClick={() => router.push('/tasks')}
            >
              Go to Tasks
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Profile</h1>
          <Button
            variant="secondary"
            size="md"
            onClick={() => router.back()}
          >
            Back
          </Button>
        </div>

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="bg-blue-600 p-6">
            <div className="flex items-center">
              <div className="bg-blue-200 border-2 border-dashed rounded-xl w-16 h-16 flex items-center justify-center text-blue-800 font-bold text-xl">
                {user.name.charAt(0)}
              </div>
              <div className="ml-4 text-white">
                <h2 className="text-2xl font-bold">{isEditing ? editName : user.name}</h2>
                <p className="text-blue-100">{isEditing ? editEmail : user.email}</p>
              </div>
            </div>
          </div>

          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-1">Full Name</h3>
                {isEditing ? (
                  <input
                    type="text"
                    value={editName}
                    onChange={(e) => setEditName(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter your name"
                  />
                ) : (
                  <p className="text-gray-900">{user.name}</p>
                )}
              </div>

              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-1">Email Address</h3>
                {isEditing ? (
                  <input
                    type="email"
                    value={editEmail}
                    onChange={(e) => setEditEmail(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter your email"
                  />
                ) : (
                  <p className="text-gray-900">{user.email}</p>
                )}
              </div>

              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-1">Account Created</h3>
                <p className="text-gray-900">{new Date(user.created_at).toLocaleDateString()}</p>
              </div>

              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-1">User ID</h3>
                <p className="text-gray-900 font-mono text-sm">{user.id.substring(0, 8)}...</p>
              </div>
            </div>

            {updateError && (
              <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-md text-sm">
                {updateError}
              </div>
            )}

            <div className="flex flex-col sm:flex-row gap-3">
              {isEditing ? (
                <>
                  <Button
                    variant="primary"
                    size="md"
                    className="flex-1"
                    onClick={handleSaveProfile}
                    disabled={updating}
                  >
                    {updating ? 'Saving...' : 'Save Changes'}
                  </Button>
                  <Button
                    variant="secondary"
                    size="md"
                    className="flex-1"
                    onClick={handleEditToggle}
                    disabled={updating}
                  >
                    Cancel
                  </Button>
                </>
              ) : (
                <>
                  <Button
                    variant="primary"
                    size="md"
                    className="flex-1"
                    onClick={handleEditToggle}
                  >
                    Edit Profile
                  </Button>
                  <Button
                    variant="secondary"
                    size="md"
                    className="flex-1"
                    onClick={handleLogout}
                  >
                    Logout
                  </Button>
                </>
              )}
            </div>
          </div>
        </div>

        <div className="mt-8 bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-medium text-gray-800 mb-4">Account Security</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center py-2 border-b border-gray-100">
              <span className="text-gray-600">Change Password</span>
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => setShowPasswordModal(true)}
              >
                Update
              </Button>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-gray-100">
              <span className="text-gray-600">Two-Factor Authentication</span>
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => setShowTwoFactorModal(true)}
              >
                Setup
              </Button>
            </div>
            <div className="flex justify-between items-center py-2">
              <span className="text-gray-600">Active Sessions</span>
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => setShowSessionsModal(true)}
              >
                View
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Password Change Modal */}
      {showPasswordModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-800">Change Password</h3>
                <button 
                  onClick={() => {
                    setShowPasswordModal(false);
                    setPasswordChangeError('');
                    setCurrentPassword('');
                    setNewPassword('');
                    setConfirmNewPassword('');
                  }}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>

              {passwordChangeError && (
                <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-md text-sm">
                  {passwordChangeError}
                </div>
              )}

              <div className="space-y-4">
                <div>
                  <label htmlFor="currentPassword" className="block text-sm font-medium text-gray-700 mb-1">
                    Current Password
                  </label>
                  <input
                    id="currentPassword"
                    type="password"
                    value={currentPassword}
                    onChange={(e) => setCurrentPassword(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter current password"
                  />
                </div>

                <div>
                  <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700 mb-1">
                    New Password
                  </label>
                  <input
                    id="newPassword"
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter new password"
                  />
                </div>

                <div>
                  <label htmlFor="confirmNewPassword" className="block text-sm font-medium text-gray-700 mb-1">
                    Confirm New Password
                  </label>
                  <input
                    id="confirmNewPassword"
                    type="password"
                    value={confirmNewPassword}
                    onChange={(e) => setConfirmNewPassword(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Confirm new password"
                  />
                </div>
              </div>

              <div className="flex gap-3 mt-6">
                <Button
                  variant="secondary"
                  size="md"
                  className="flex-1"
                  onClick={() => {
                    setShowPasswordModal(false);
                    setPasswordChangeError('');
                    setCurrentPassword('');
                    setNewPassword('');
                    setConfirmNewPassword('');
                  }}
                >
                  Cancel
                </Button>
                <Button
                  variant="primary"
                  size="md"
                  className="flex-1"
                  onClick={handleChangePassword}
                  disabled={passwordChanging}
                >
                  {passwordChanging ? 'Updating...' : 'Update Password'}
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Active Sessions Modal */}
      {showSessionsModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[80vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-800">Active Sessions</h3>
                <button 
                  onClick={() => setShowSessionsModal(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>

              {loadingSessions ? (
                <div className="flex justify-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>
              ) : (
                <div className="space-y-4">
                  {sessions.length > 0 ? (
                    sessions.map((session) => (
                      <div 
                        key={session.id} 
                        className={`flex justify-between items-center p-4 border rounded-lg ${
                          session.is_current ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
                        }`}
                      >
                        <div>
                          <div className="font-medium">{session.device}</div>
                          <div className="text-sm text-gray-600">
                            {session.ip_address} • {session.location} • Last activity: {session.last_activity}
                          </div>
                          {session.is_current && (
                            <div className="text-xs text-blue-600 font-semibold mt-1">Current session</div>
                          )}
                        </div>
                        {!session.is_current && (
                          <Button
                            variant="secondary"
                            size="sm"
                            onClick={() => handleRevokeSession(session.id)}
                          >
                            Revoke
                          </Button>
                        )}
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-8 text-gray-500">
                      No active sessions found
                    </div>
                  )}
                </div>
              )}

              <div className="mt-6">
                <Button
                  variant="secondary"
                  size="md"
                  className="w-full"
                  onClick={() => setShowSessionsModal(false)}
                >
                  Close
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Two-Factor Authentication Modal */}
      {showTwoFactorModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-800">
                  {twoFactorStep === 'setup' && 'Setup Two-Factor Authentication'}
                  {twoFactorStep === 'verify' && 'Verify Two-Factor Authentication'}
                  {twoFactorStep === 'success' && 'Two-Factor Authentication Enabled'}
                </h3>
                <button 
                  onClick={() => {
                    setShowTwoFactorModal(false);
                    setTwoFactorStep('setup');
                    setTwoFactorError('');
                    setVerificationToken('');
                  }}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>

              {twoFactorError && (
                <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-md text-sm">
                  {twoFactorError}
                </div>
              )}

              {twoFactorStep === 'setup' && (
                <div className="space-y-4">
                  <div className="text-gray-600">
                    <p className="mb-3">To enable two-factor authentication:</p>
                    <ol className="list-decimal pl-5 space-y-2">
                      <li>Download an authenticator app (Google Authenticator, Authy, etc.)</li>
                      <li>Click the button below to generate a QR code</li>
                      <li>Scan the QR code with your authenticator app</li>
                      <li>Enter the code from your app to verify</li>
                    </ol>
                  </div>
                  
                  <div className="pt-4">
                    <Button
                      variant="primary"
                      size="md"
                      className="w-full"
                      onClick={handleStartTwoFactor}
                      disabled={twoFactorLoading}
                    >
                      {twoFactorLoading ? 'Generating...' : 'Generate QR Code'}
                    </Button>
                  </div>
                </div>
              )}

              {twoFactorStep === 'verify' && (
                <div className="space-y-4">
                  <div className="text-gray-600">
                    <p className="mb-3">Enter the 6-digit code from your authenticator app:</p>
                  </div>
                  
                  <div>
                    <input
                      type="text"
                      value={verificationToken}
                      onChange={(e) => setVerificationToken(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Enter 6-digit code"
                      maxLength={6}
                    />
                  </div>
                  
                  <div className="flex gap-3 pt-2">
                    <Button
                      variant="secondary"
                      size="md"
                      className="flex-1"
                      onClick={() => {
                        setTwoFactorStep('setup');
                        setTwoFactorError('');
                      }}
                    >
                      Back
                    </Button>
                    <Button
                      variant="primary"
                      size="md"
                      className="flex-1"
                      onClick={handleVerifyTwoFactor}
                      disabled={twoFactorLoading}
                    >
                      {twoFactorLoading ? 'Verifying...' : 'Verify'}
                    </Button>
                  </div>
                </div>
              )}

              {twoFactorStep === 'success' && (
                <div className="space-y-4">
                  <div className="text-center py-4">
                    <div className="mx-auto h-16 w-16 bg-green-100 rounded-full flex items-center justify-center mb-4">
                      <span className="text-green-600 text-2xl">✓</span>
                    </div>
                    <h4 className="text-lg font-medium text-gray-800 mb-2">2FA Setup Complete!</h4>
                    <p className="text-gray-600">
                      Two-factor authentication has been successfully enabled on your account.
                    </p>
                  </div>
                  
                  <div className="pt-2">
                    <Button
                      variant="primary"
                      size="md"
                      className="w-full"
                      onClick={() => {
                        setShowTwoFactorModal(false);
                        setTwoFactorStep('setup');
                      }}
                    >
                      Done
                    </Button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProfilePage;