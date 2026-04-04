# 🚀 Frontend Deployment Guide (Vercel)

## Quick Deployment (5 minutes)

### Step 1: Push Frontend to GitHub

```bash
cd frontend
git init
git add .
git commit -m "Add frontend for Call Center Compliance Analyzer"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/call-center-compliance-frontend.git
git push -u origin main
```

### Step 2: Deploy to Vercel

#### Option A: Using Vercel Dashboard (Easiest)

1. Go to [vercel.com](https://vercel.com)
2. Sign up / Login with GitHub
3. Click **"Add New Project"**
4. **Import** your GitHub repository
5. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `./` (or `frontend` if in monorepo)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Click **"Deploy"**

Your app will be live in ~2 minutes at `https://your-app.vercel.app`

#### Option B: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N
# - Project name? call-center-compliance
# - In which directory? ./
# - Override settings? N

# Production deployment
vercel --prod
```

### Step 3: Update API URL

After deploying backend to Render:

1. Edit `src/App.jsx`
2. Update line ~12:
```javascript
const API_URL = 'https://your-actual-api-name.onrender.com/api/call-analytics';
```
3. Redeploy:
```bash
git add .
git commit -m "Update API URL"
git push
```

Vercel auto-deploys on push!

### Step 4: Test Live App

1. Go to your Vercel URL
2. Upload a sample MP3 file
3. Wait for analysis (15-30 seconds)
4. Verify results display correctly

---

## Important Notes

### CORS Configuration

Your backend must allow requests from your Vercel domain.

In `app.py`, add:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://your-app.vercel.app'])
```

Add to `requirements.txt`:
```
flask-cors==4.0.0
```

### Environment Variables (If Needed)

If you want to use environment variables in frontend:

1. In Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add variables (they must start with `VITE_`):
   - `VITE_API_URL`: `https://your-api.onrender.com/api/call-analytics`
   - `VITE_API_KEY`: `sk_track3_987654321`

3. Access in code:
```javascript
const API_URL = import.meta.env.VITE_API_URL;
const API_KEY = import.meta.env.VITE_API_KEY;
```

### Custom Domain (Optional)

1. In Vercel Dashboard → Domains
2. Add your domain
3. Update DNS records as instructed
4. Your app will be available at your domain!

---

## Troubleshooting

### Build Fails

**Error**: `Module not found`
**Solution**: Make sure all dependencies are in `package.json`

```bash
npm install
npm run build  # Test locally first
```

### API Calls Fail (CORS Error)

**Error**: `Access to fetch at '...' has been blocked by CORS policy`
**Solution**: Add CORS to backend (see above)

### Slow First Load

**Explanation**: Vite optimizes on first visit, subsequent loads are fast.
**Solution**: This is normal, no action needed.

### 404 on Refresh

**Solution**: Vercel handles this automatically for Vite apps. If issue persists, add `vercel.json`:

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ]
}
```

---

## Vercel URL Examples

After deployment, you'll get a URL like:
- `https://call-center-compliance.vercel.app`
- `https://call-center-compliance-vishwa.vercel.app`
- `https://your-project-name-random.vercel.app`

**This is your live URL to submit to GUVI!**

---

## Local Development

While developing:

```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Frontend at `http://localhost:5173` → Talks to backend at `http://localhost:5000`

---

## Production Checklist

Before submitting:

- [ ] Backend deployed to Render and working
- [ ] Frontend deployed to Vercel
- [ ] API_URL updated in frontend code
- [ ] CORS configured in backend
- [ ] Test upload works end-to-end
- [ ] Responsive design works (test on mobile)
- [ ] No console errors
- [ ] Loading states work correctly
- [ ] Error handling works

---

## Submission URLs

For GUVI submission, you'll provide:

1. **Live URL**: `https://your-app.vercel.app`
2. **GitHub**: `https://github.com/YOUR_USERNAME/call-center-compliance-frontend`
3. **API Endpoint**: `https://your-api.onrender.com/api/call-analytics`

**All three must be working for full points!**

---

**Deployment complete! Your app is now live! 🎉**
