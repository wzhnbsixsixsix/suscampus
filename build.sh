#!/usr/bin/env bash

# Exit on error
set -o errexit


# Install the Node.js environment
echo "Installing Node.js...."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

echo "Node.js version: $(node -v)"
echo "npm version: $(npm -v)"

cd sustainableCampus/static/js || { echo "Directory switching failure！"; exit 1; }

npm install --legacy-peer-deps



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