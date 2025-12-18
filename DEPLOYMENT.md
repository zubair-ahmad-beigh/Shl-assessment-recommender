# Deploying SHL Assessment Recommender to Render

This guide walks you through deploying both the FastAPI backend and Streamlit frontend to Render.

## 📋 Prerequisites

- A [Render account](https://render.com) (free tier works)
- A GitHub account
- Your code pushed to a GitHub repository
- Gemini API key (if using LLM features)

## 🏗️ Architecture Overview

You'll deploy **two separate services**:

1. **Backend Service** (FastAPI) - Handles recommendations using FAISS
2. **Frontend Service** (Streamlit) - User interface

## 📦 Step 1: Push Your Code to GitHub

If you haven't already, push your project to GitHub:

```bash
cd c:\Users\beigh\Downloads\shl-assessment-recommender-main
git init
git add .
git commit -m "Prepare for Render deployment"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## 🚀 Step 2: Deploy the Backend Service

### 2.1 Create New Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your `shl-assessment-recommender` repository

### 2.2 Configure Backend Service

Fill in the following settings:

| Setting | Value |
|---------|-------|
| **Name** | `shl-recommender-backend` (or your choice) |
| **Region** | Choose closest to you (e.g., Oregon) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn api:app --host 0.0.0.0 --port $PORT` |
| **Plan** | `Free` |

### 2.3 Add Environment Variables

Click **"Advanced"** and add environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.8` | Matches your runtime.txt |
| `GEMINI_API_KEY` | `your-api-key-here` | Optional, if using Gemini |

### 2.4 Deploy Backend

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment (downloads ML models)
3. Once deployed, you'll see a URL like: `https://shl-recommender-backend.onrender.com`
4. **Save this URL** - you'll need it for the frontend!

### 2.5 Test Backend

Visit these URLs to verify:
- Health check: `https://your-backend-url.onrender.com/health`
- Root: `https://your-backend-url.onrender.com/`

You should see JSON responses.

## 🎨 Step 3: Deploy the Frontend Service

### 3.1 Create New Web Service

1. In Render Dashboard, click **"New +"** → **"Web Service"**
2. Select the **same repository**
3. This time we'll configure it for the frontend

### 3.2 Configure Frontend Service

Fill in the following settings:

| Setting | Value |
|---------|-------|
| **Name** | `shl-recommender-frontend` (or your choice) |
| **Region** | Same as backend |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements-frontend.txt` |
| **Start Command** | `streamlit run frontend.py --server.port $PORT --server.address 0.0.0.0` |
| **Plan** | `Free` |

### 3.3 Add Environment Variables

Click **"Advanced"** and add:

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.8` | Matches your runtime.txt |
| `API_URL` | `https://your-backend-url.onrender.com` | **Use YOUR backend URL from Step 2.4** |

⚠️ **IMPORTANT**: Make sure `API_URL` does NOT have a trailing slash and does NOT include `/recommend` - just the base URL!

### 3.4 Deploy Frontend

1. Click **"Create Web Service"**
2. Wait 2-3 minutes for deployment
3. Once deployed, you'll get a URL like: `https://shl-recommender-frontend.onrender.com`

## ✅ Step 4: Test Your Deployment

1. Open your frontend URL in a browser
2. Enter a test query like: `"Software engineer with Java and communication skills"`
3. Click **"Get Recommendations"**
4. You should see assessment recommendations!

## 🔧 Troubleshooting

### Backend Issues

**Problem**: Backend fails to start
- **Solution**: Check logs in Render dashboard. Common issues:
  - Missing files (`shl_faiss.index`, `metadata.pkl`, `shl_assessments.json`)
  - Make sure these files are committed to your Git repository

**Problem**: Health check fails
- **Solution**: Verify the `/health` endpoint works locally first

### Frontend Issues

**Problem**: Frontend can't connect to backend
- **Solution**: 
  - Verify `API_URL` environment variable is set correctly
  - Check backend is running and accessible
  - Look at frontend logs for connection errors

**Problem**: CORS errors
- **Solution**: Backend already has CORS enabled for all origins. If issues persist, check browser console.

### Free Tier Limitations

**Problem**: Services spin down after 15 minutes of inactivity
- **Solution**: This is normal on free tier. Services will restart when accessed (takes ~30 seconds)
- **Upgrade Option**: Paid plans ($7/month per service) keep services always running

## 📊 Monitoring

### View Logs
- Go to your service in Render Dashboard
- Click **"Logs"** tab
- Monitor for errors or issues

### Check Metrics
- Click **"Metrics"** tab
- View CPU, memory usage, response times

## 🔄 Updating Your Deployment

When you make code changes:

1. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push
   ```

2. Render will **automatically redeploy** both services!

## 💰 Cost Breakdown

### Free Tier (Current Setup)
- 750 hours/month per service
- Services spin down after 15 min inactivity
- **Cost**: $0/month

### Paid Tier (If Needed)
- Always-on services
- Better performance
- **Cost**: ~$7/month per service = $14/month total

## 🎯 Next Steps

- [ ] Test with various queries
- [ ] Monitor performance in Render dashboard
- [ ] Consider upgrading if you need always-on services
- [ ] Set up custom domain (optional, available on paid plans)

## 📞 Support

If you encounter issues:
1. Check Render's [documentation](https://render.com/docs)
2. Review service logs in Render dashboard
3. Verify all files are committed to Git

---

**Congratulations!** 🎉 Your SHL Assessment Recommender is now live on Render!
