#!/bin/bash
# Exit on any error
set -e

echo "🚀 Starting build process..."

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️ Running migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build completed successfully!"