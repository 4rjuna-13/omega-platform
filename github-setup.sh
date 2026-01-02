#!/bin/bash
echo "=== GITHUB SETUP HELPER ==="
echo ""
echo "Choose authentication method:"
echo "1. HTTPS with Personal Access Token (recommended)"
echo "2. SSH Key (more secure)"
echo "3. Check current setup"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "=== HTTPS TOKEN SETUP ==="
        echo "1. Create token at: https://github.com/settings/tokens"
        echo "2. Select 'repo' scope"
        echo "3. Copy the token (starts with ghp_)"
        echo ""
        read -p "Enter your GitHub username: " username
        read -sp "Enter your token: " token
        echo ""
        git remote set-url origin https://${username}:${token}@github.com/4rjuna-13/omega-platform.git
        echo "✅ Remote updated"
        git push origin main
        ;;
    2)
        echo ""
        echo "=== SSH KEY SETUP ==="
        echo "1. Generating SSH key..."
        ssh-keygen -t ed25519 -C "4rjuna13@chromebook" -f ~/.ssh/id_ed25519 -N ""
        echo ""
        echo "2. Add this key to GitHub:"
        echo "   Go to: https://github.com/settings/keys"
        echo "   Click 'New SSH key'"
        echo "   Paste the following:"
        echo ""
        cat ~/.ssh/id_ed25519.pub
        echo ""
        read -p "Press Enter after adding key to GitHub..."
        git remote set-url origin git@github.com:4rjuna-13/omega-platform.git
        echo "✅ Remote updated to SSH"
        ssh -T git@github.com
        ;;
    3)
        echo ""
        echo "=== CURRENT SETUP ==="
        echo "Remote URL:"
        git remote -v
        echo ""
        echo "SSH Test:"
        ssh -T git@github.com 2>&1 | head -2
        echo ""
        echo "Git Config:"
        git config --list | grep -E "(user\.|remote\.|credential)"
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
