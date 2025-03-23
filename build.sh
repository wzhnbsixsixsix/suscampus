#!/usr/bin/env bash

# Exit on error
set -o errexit


# ----------------------------
# 1. Install Node.js (no sudo)
# ----------------------------
echo "Installing Node.js..."
export NODE_VERSION=18.20.2  # Specify Node.js version

# Create local installation directory
mkdir -p $HOME/.nodejs
curl -o node.tar.gz https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.gz
tar -xzf node.tar.gz -C $HOME/.nodejs --strip-components=1
rm node.tar.gz

# Set environment variables
export PATH="$HOME/.nodejs/bin:$PATH"
echo "Node.js version: $(node -v)"
echo "npm version: $(npm -v)"

# ----------------------------
# 2. Install frontend dependencies
# ----------------------------
echo "Entering frontend directory..."
cd sustainableCampus/static/js || { echo "Directory change failed! Check if the path is correct"; exit 1; }

echo "Installing npm dependencies..."
npm install --no-audit --legacy-peer-deps  # Disable audit logs

# Optional build step
if [ -f "package.json" ] && [ -f "package-lock.json" ]; then
  echo "Executing production build..."
  npm run build --if-present
fi

# Return to project root
cd ../../../..
# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate


if [ "$RENDER" = "true" ]; then
  echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'abc')" | python manage.py shell
fi