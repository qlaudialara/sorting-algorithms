#!/bin/bash
# Push to GitHub with Personal Access Token
# Run this script and enter your GitHub credentials when prompted

cd /Users/qlaudia/sorting-experiment

echo "=========================================="
echo "Pushing to GitHub..."
echo "=========================================="
echo ""
echo "Repository: https://github.com/qlaudialara/sorting-algorithms-experiment"
echo ""
echo "When prompted:"
echo "  Username: qlaudialara"
echo "  Password: [Paste your Personal Access Token]"
echo ""
echo "To get a PAT:"
echo "  1. Go to: https://github.com/settings/tokens"
echo "  2. Click 'Generate new token (classic)'"
echo "  3. Select 'repo' scope"
echo "  4. Copy and paste the token below"
echo ""
echo "=========================================="
echo ""

git push -u origin main

echo ""
echo "=========================================="
echo "Done! Check your repository:"
echo "https://github.com/qlaudialara/sorting-algorithms-experiment"
echo "=========================================="
