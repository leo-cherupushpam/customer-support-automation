# Deployment Guide - Streamlit Cloud

## Prerequisites
- GitHub account
- Code committed to GitHub repository

## Step 1: Push Code to GitHub

```bash
# Navigate to project directory
cd /Users/leocherupushpam/Documents/Claude/Projects/Apps/portfolio/customer-support-automation

# Add all changes
git add .

# Commit changes
git commit -m "Week 4: Add beta tracking and deployment files"

# Add remote (if not already added)
git remote add origin https://github.com/YOUR_USERNAME/customer-support-automation.git

# Push to main branch
git push -u origin main
```

## Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://streamlit.io/cloud
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New App"
   - Select your repository: `customer-support-automation`
   - Choose branch: `main`
   - Enter app path: `app.py`
   - Click "Deploy"

3. **Wait for Deployment**
   - Streamlit will install dependencies from `requirements.txt`
   - Build will take 2-5 minutes
   - You'll receive email when complete

4. **Access Your App**
   - App will be live at: `https://customer-support-automation.streamlit.app`
   - Share this URL with beta testers

## Step 3: Verify Deployment

1. Open the app URL in a browser
2. Test the following:
   - Enter a sample ticket in the sidebar
   - Click "Process Ticket"
   - Verify all 4 agents work correctly
   - Check that classification, response, and escalation paths work

## Troubleshooting

### App fails to load
- Check `requirements.txt` has all dependencies
- Verify `app.py` is in the root directory
- Check Streamlit Cloud logs for errors

### Import errors
- Ensure `src/` directory is properly structured
- Check `__init__.py` files exist in `src/` and `src/agents/`
- Verify agent imports in `app.py` are correct

### Performance issues
- Add `Procfile` to optimize deployment
- Configure `.streamlit/config.toml` for production
- Consider adding caching for agent initialization

## Custom Domain (Optional)

1. Go to Settings > Domain
2. Enter your custom domain
3. Update DNS records as instructed
4. Wait for DNS propagation (up to 48 hours)

## Environment Variables (If Needed)

1. Go to Settings > Environment Variables
2. Add any required variables (e.g., API keys)
3. Click "Save"
4. App will redeploy with new variables

## Monitoring

- Check Streamlit Cloud dashboard for:
  - App uptime
  - Request count
  - Memory usage
  - Error logs

---

**Last Updated**: 2026-05-06
**Deployment Status**: Ready to deploy
