# Step 5: Production Deployment (Render + Docker)

This guide walks you through connecting your existing GitHub repository to Render to host your AI forensics application.

## 1. Verify Your Repository Structure
Before deploying, ensure your GitHub repository contains these files at the root:
- `app.py`
- `tools.py`
- `requirements.txt`
- `Dockerfile`
- `.gitignore` (ensure it contains `.env` so your API key is NOT uploaded)

## 2. Connect GitHub to Render
1. Go to [Render.com](https://render.com) and log in.
2. Click the **New +** button in the top right and select **Web Service**.
3. Under the "Connect a repository" section, find your repository in the list and click **Connect**.
   - *Note: If you don't see it, click "Configure account" to ensure Render has permission to access your specific repository.*

## 3. Configure Deployment Settings
On the "Create a new Web Service" page, fill in the following:
- **Name:** Choose a unique name (this will form your URL, e.g., `my-forensics-app.onrender.com`).
- **Region:** Select the one closest to you.
- **Branch:** `main` (or whichever branch your code is on).
- **Runtime:** Ensure this is set to **Docker**.
- **Build Command:** (Leave default)
- **Start Command:** (Leave default—Render will read this from your Dockerfile)

## 4. Add Environment Variables (Crucial)
Scroll down to the **Environment** section and click **Add Environment Variable**:
- **Key:** `GEMINI_API_KEY`
- **Value:** *(Paste your actual Gemini API key here)*

## 5. Deploy
- Select the **Free** instance type at the bottom.
- Click **Create Web Service**. 

## 6. Monitor and Launch
Render will start building your container. You can watch the deployment logs on the screen. Once the log says `Your service is live 🎉`, your forensic app is publicly available at the URL provided at the top of the dashboard.