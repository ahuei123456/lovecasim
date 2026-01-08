# Love Live! Solo Card Game Deployment Guide

## 1. Prepare GitHub Repository

1.  **Initialize Git** (if not already done):
    ```bash
    git init
    git add .
    git commit -m "Initial commit for deployment"
    ```

2.  **Create a Repository on GitHub**:
    *   Go to [GitHub.com](https://github.com/new).
    *   Create a new public/private repository named `loveca-solo` (or similar).
    *   Do **NOT** add README, gitignore, or license (we already have them).

3.  **Push to GitHub**:
    *   Copy the commands provided by GitHub under "...or push an existing repository from the command line".
    *   Example:
        ```bash
        git remote add origin https://github.com/YOUR_USERNAME/loveca-solo.git
        git branch -M main
        git push -u origin main
        ```

## 2. Deploy to Render (Free Tier)

Render is the easiest way to host this Python/Flask app for free.

1.  **Sign Up/Login**: Go to [render.com](https://render.com/) and log in (use GitHub login for easier linking).
2.  **New Web Service**:
    *   Click **New +** button -> **Web Service**.
    *   Select "Build and deploy from a Git repository".
    *   Connect your `loveca-solo` repository.
3.  **Configure Service**:
    *   **Name**: `loveca-solo` (this will determine your URL, e.g., `loveca-solo.onrender.com`).
    *   **Region**: Closest to you (e.g., Singapore, Frankfurt, Oregon).
    *   **Branch**: `main`.
    *   **Runtime**: **Python 3**.
    *   **Build Command**: `pip install -r requirements.txt`.
    *   **Start Command**: `gunicorn server:app` (This is already in your `Procfile`, but Render might ask).
    *   **Instance Type**: **Free**.
4.  **Deploy**:
    *   Click **Create Web Service**.
    *   Render will clone your repo, install dependencies (numpy, flask, numba), and start the server.
    *   Wait for the green "Live" status.

## 3. Access Your Game

*   Your game will be available at `https://<your-service-name>.onrender.com`.
*   Share this URL with anyone!
*   The "Free" tier spins down after 15 minutes of inactivity. The first request after spin-down might take ~30-60 seconds to load.

## Notes regarding AI Mode

*   The AI runs on the server (CPU).
*   The current free tier on Render provides limited CPU (0.1 CPU usually). The Numba optimizations we added will help, but AI turns might take a few seconds.
*   "Player vs AI" mode works perfectly.
