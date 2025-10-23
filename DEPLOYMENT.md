# Deployment Guide

This guide will help you deploy your Job Tracker Flask app to Railway (free hosting) with authentication.

## Prerequisites

1. **GitHub Account**: You'll need a GitHub account to store your code
2. **Railway Account**: Sign up at [railway.app](https://railway.app) (free)
3. **Environment Variables**: Set up your authentication credentials

## Step 1: Prepare Your Code

1. **Set up authentication credentials**:
   - Copy `env.example` to `.env`
   - Edit `.env` and set your username and password:
     ```
     FLASK_USERNAME=your_username_here
     FLASK_PASSWORD=your_secure_password_here
     SECRET_KEY=your_secret_key_here
     ```

2. **Install new dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Test locally**:
   ```bash
   python app.py
   ```
   - Visit `http://localhost:5000`
   - You should be redirected to the login page
   - Login with your credentials

## Step 2: Deploy to Railway

### Option A: Deploy from GitHub (Recommended)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit with authentication"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect it's a Python app

3. **Set Environment Variables**:
   - In Railway dashboard, go to your project
   - Click on "Variables" tab
   - Add these variables:
     - `FLASK_USERNAME`: Your username
     - `FLASK_PASSWORD`: Your password
     - `SECRET_KEY`: A random secret key (generate one)
     - `FLASK_ENV`: `production`

4. **Deploy**:
   - Railway will automatically build and deploy your app
   - You'll get a URL like `https://your-app-name.railway.app`

### Option B: Deploy with Railway CLI

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and deploy**:
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set environment variables**:
   ```bash
   railway variables set FLASK_USERNAME=your_username
   railway variables set FLASK_PASSWORD=your_password
   railway variables set SECRET_KEY=your_secret_key
   railway variables set FLASK_ENV=production
   ```

## Step 3: Access Your App

1. **Get your app URL** from Railway dashboard
2. **Visit the URL** - you should see the login page
3. **Login** with your credentials
4. **Test functionality** - add, edit, delete applications

## Security Features

- ✅ **Authentication Required**: Only you can access the app
- ✅ **Secure Password Storage**: Passwords are hashed
- ✅ **Session Management**: Secure login sessions
- ✅ **Environment Variables**: Credentials stored securely
- ✅ **HTTPS**: Railway provides SSL certificates

## Troubleshooting

### Common Issues:

1. **"Invalid username or password"**:
   - Check your environment variables in Railway
   - Make sure `FLASK_USERNAME` and `FLASK_PASSWORD` are set correctly

2. **Database errors**:
   - Railway provides persistent storage
   - Your data will be saved between deployments

3. **App not loading**:
   - Check Railway logs in the dashboard
   - Make sure all environment variables are set
   - Verify the build completed successfully

### Getting Help:

- **Railway Documentation**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: [discord.gg/railway](https://discord.gg/railway)
- **Check logs**: Railway dashboard → Your project → Deployments → View logs

## Alternative Hosting Options

If Railway doesn't work for you, here are other free options:

1. **Render**: [render.com](https://render.com)
2. **Fly.io**: [fly.io](https://fly.io) (free tier)
3. **PythonAnywhere**: [pythonanywhere.com](https://pythonanywhere.com)
4. **Heroku**: [heroku.com](https://heroku.com) (limited free tier)

Each platform has similar deployment processes but may require different configuration files.

## Cost

- **Railway**: Free tier includes 500 hours/month
- **Your usage**: Likely well within free limits for personal use
- **Upgrade**: Only if you need more resources or custom domains

## Next Steps

1. **Custom Domain**: Add your own domain name
2. **Backup**: Set up database backups
3. **Monitoring**: Add application monitoring
4. **Updates**: Deploy updates by pushing to GitHub

Your Job Tracker is now live and secure! 🎉
