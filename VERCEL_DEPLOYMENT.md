# 🚀 Deploy to Vercel - Complete Guide

## **Why Vercel?**

✅ **Generous Free Tier**: No time limits like Railway  
✅ **Excellent Performance**: Global CDN and edge functions  
✅ **Easy Deployment**: Simple Git integration  
✅ **Automatic HTTPS**: SSL certificates included  
✅ **Great Developer Experience**: Fast builds and deployments  

## **Step 1: Prepare Your Code**

### **Files Ready for Deployment:**
- ✅ `app.py` - Main Flask application
- ✅ `wsgi.py` - WSGI entry point for Vercel
- ✅ `vercel.json` - Vercel configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `templates/` - HTML templates
- ✅ `static/` - CSS and JavaScript files
- ✅ `.gitignore` - Protects sensitive files

### **Files Protected (NOT committed):**
- ❌ `.env` - Your actual credentials
- ❌ `job_tracker.db` - Your database file

## **Step 2: Install Vercel CLI**

```bash
# Install Vercel CLI globally
npm install -g vercel

# Verify installation
vercel --version
```

## **Step 3: Deploy to Vercel**

### **Option A: Deploy from GitHub (Recommended)**

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add Vercel deployment configuration"
   git push origin main
   ```

2. **Go to [vercel.com](https://vercel.com)**
3. **Sign up/Login** with GitHub
4. **Click "New Project"**
5. **Import your GitHub repository**
6. **Vercel will auto-detect Python and configure everything**

### **Option B: Deploy with Vercel CLI**

```bash
# Login to Vercel
vercel login

# Deploy from your project directory
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (your account)
# - Link to existing project? No
# - Project name: job-tracker (or your choice)
# - Directory: ./
```

## **Step 4: Set Environment Variables**

### **In Vercel Dashboard:**
1. **Go to your project**
2. **Click "Settings" tab**
3. **Click "Environment Variables"**
4. **Add these variables:**

```
FLASK_USERNAME=CarloCapuz
FLASK_PASSWORD=Valentine03
SECRET_KEY=your_random_secret_key_here
FLASK_ENV=production
```

### **Generate Secret Key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### **Using Vercel CLI:**
```bash
vercel env add FLASK_USERNAME
vercel env add FLASK_PASSWORD
vercel env add SECRET_KEY
vercel env add FLASK_ENV
```

## **Step 5: Access Your Deployed App**

1. **Vercel will give you a URL** like: `https://your-app-name.vercel.app`
2. **Visit the URL**
3. **Login with your credentials:**
   - Username: `CarloCapuz`
   - Password: `Valentine03`

## **Step 6: Test Everything**

✅ **Authentication works** - Only your credentials work  
✅ **Add applications** - Test CRUD operations  
✅ **Data persists** - Your data is saved  
✅ **Responsive design** - Works on mobile/desktop  
✅ **Fast loading** - Vercel's global CDN  

## **Vercel vs Railway Comparison**

| Feature | Vercel | Railway |
|---------|--------|---------|
| **Free Tier Duration** | Unlimited | 30 days only |
| **Free Tier Limits** | 100GB bandwidth/month | 500 hours/month |
| **Performance** | Global CDN | Good |
| **Deployment Speed** | Very Fast | Fast |
| **HTTPS** | Automatic | Automatic |
| **Custom Domains** | Free | Paid |
| **Database** | External needed | Built-in |

## **Database Considerations**

**Important**: Vercel is serverless, so the SQLite database won't persist between deployments. For production, consider:

1. **Vercel Postgres** (paid add-on)
2. **External database** (Supabase, PlanetScale, etc.)
3. **For now**: Your data will reset on each deployment

**Quick Fix for Testing**: The app will work, but data resets on each deployment.

## **Troubleshooting**

### **Common Issues:**

1. **"Module not found" errors**
   - Check `requirements.txt` includes all dependencies
   - Ensure all imports are correct

2. **"Environment variables not found"**
   - Check Vercel dashboard → Settings → Environment Variables
   - Make sure variables are set for "Production"

3. **"Database errors"**
   - SQLite files don't persist on Vercel
   - Consider external database for production

4. **"Build failed"**
   - Check Vercel build logs
   - Ensure all files are committed to Git

### **Getting Help:**
- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Vercel Discord**: [vercel.com/discord](https://vercel.com/discord)
- **Check logs**: Vercel dashboard → Functions → View logs

## **Cost & Limits**

- **Vercel Free Tier**: 
  - Unlimited deployments
  - 100GB bandwidth/month
  - 100GB-hours execution time/month
  - Perfect for personal projects

## **Next Steps After Deployment**

1. **Custom Domain**: Add your own domain (free on Vercel)
2. **External Database**: Set up persistent database
3. **Monitoring**: Add error tracking
4. **Updates**: Deploy updates by pushing to GitHub

## **Quick Commands Summary**

```bash
# Local development
python app.py

# Deploy to Vercel
vercel

# Add environment variables
vercel env add VARIABLE_NAME

# View logs
vercel logs

# Git workflow
git add .
git commit -m "Your commit message"
git push
```

## **Security Checklist**

- ✅ **Credentials in environment variables** (not in code)
- ✅ **HTTPS enabled** (automatic on Vercel)
- ✅ **Authentication required** for all routes
- ✅ **Passwords hashed** with SHA-256
- ✅ **Session management** with Flask-Login
- ✅ **No sensitive data in Git**

Your Job Tracker is now ready for Vercel deployment! 🎉

**Note**: For persistent data storage, consider upgrading to a paid Vercel plan with Postgres, or use an external database service.
