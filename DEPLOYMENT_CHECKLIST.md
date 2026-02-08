# Deployment Checklist for Cross-Device Authentication

## Pre-Deployment Checklist

### 1. Backend Configuration
- [ ] Generate a strong `BETTER_AUTH_SECRET` using: `python -c "import secrets; print(secrets.token_hex(32))"`
- [ ] Set `BETTER_AUTH_SECRET` environment variable in your backend hosting platform
- [ ] Set `DATABASE_URL` environment variable in your backend hosting platform
- [ ] Set `GEMINI_API_KEY` environment variable in your backend hosting platform
- [ ] Update CORS origins in `backend/main.py` with your frontend domain
- [ ] Test your backend API endpoints directly after deployment

### 2. Frontend Configuration
- [ ] Set `NEXT_PUBLIC_API_URL` environment variable in Vercel to your deployed backend URL
- [ ] Verify the URL format (should be like `https://your-backend.onrender.com`, not `http://localhost:8000`)
- [ ] Test the frontend with the new backend URL

### 3. Post-Deployment Verification
- [ ] Test signup/login from your current device
- [ ] Test signup/login from a different device/network
- [ ] Verify that JWT tokens are being stored and sent correctly
- [ ] Check browser console and network tab for any errors
- [ ] Confirm that API requests are going to the correct backend URL

## Common Issues and Solutions

### Issue: Authentication works on one device but not others
**Cause:** Usually due to environment variables not being properly set in deployed environments
**Solution:** 
1. Verify `NEXT_PUBLIC_API_URL` points to your deployed backend, not localhost
2. Confirm `BETTER_AUTH_SECRET` is identical across all deployments
3. Check that CORS settings allow requests from your frontend domain

### Issue: CORS errors
**Symptoms:** Browser console shows "Cross-Origin Request Blocked" errors
**Solution:** 
1. Update the `allow_origins` list in `backend/main.py` with your frontend domain
2. Example: Add `"https://your-project-name.vercel.app"` to the list

### Issue: JWT token validation fails
**Symptoms:** Login succeeds but subsequent requests fail with authentication errors
**Solution:**
1. Ensure the same `BETTER_AUTH_SECRET` is used in all environments
2. Check that the secret is at least 32 characters long
3. Verify no extra spaces or characters in the environment variable

## Testing Steps

1. Deploy backend first
2. Note the backend URL (e.g., `https://your-backend.onrender.com`)
3. Deploy frontend with `NEXT_PUBLIC_API_URL` set to your backend URL
4. Test authentication flow on your current device
5. Test authentication flow on a different device or browser
6. Clear browser cache if experiencing issues

## Environment Variables Reference

### Backend (set in your hosting platform)
```
BETTER_AUTH_SECRET=your-32-character-secret-key
DATABASE_URL=your-database-connection-string
GEMINI_API_KEY=your-gemini-api-key
```

### Frontend (set in Vercel dashboard)
```
NEXT_PUBLIC_API_URL=https://your-deployed-backend-url.com
```