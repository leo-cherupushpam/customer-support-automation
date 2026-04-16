#!/bin/bash

# Customer Support Automation - Deployment Script
# Run this after creating your GitHub repository

echo "🚀 Deploying Customer Support Automation to Streamlit Cloud"
echo ""

# Check if remote already exists
if git remote get-url origin &> /dev/null; then
    echo "✓ Remote origin already configured"
else
    echo "⚠ Remote origin not configured"
    echo ""
    echo "Please create a GitHub repository first:"
    echo "  1. Go to https://github.com/new"
    echo "  2. Create repository: customer-support-automation"
    echo "  3. Run: git remote add origin https://github.com/YOUR_USERNAME/customer-support-automation.git"
    echo ""
    exit 1
fi

# Check if we have commits
if [ $(git rev-list --count HEAD) -eq 0 ]; then
    echo "⚠ No commits to push"
    exit 1
fi

# Push to GitHub
echo "📦 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✓ Successfully pushed to GitHub!"
    echo ""
    echo "🌐 Next steps:"
    echo "  1. Visit https://streamlit.io/cloud"
    echo "  2. Sign in with GitHub"
    echo "  3. Click 'New App'"
    echo "  4. Select 'customer-support-automation' repository"
    echo "  5. Branch: main"
    echo "  6. App path: app.py"
    echo "  7. Click 'Deploy'"
    echo ""
    echo "Your app will be live at: https://customer-support-automation.streamlit.app"
else
    echo "❌ Failed to push to GitHub"
    exit 1
fi
