# Deployment Guide 🚀

The best way to deploy your **Silent Guardian AI** app is using **Streamlit Community Cloud**. It is free, optimized for Streamlit apps, and connects directly to your GitHub repository.

**Note:** You **cannot** deploy this directly to Netlify because Netlify is for static websites, and this project requires a Python server.

## Steps to Deploy on Streamlit Cloud

1.  **Push to GitHub**
    *   Initialize a git repository if you haven't: `git init`
    *   Add files: `git add .`
    *   Commit: `git commit -m "Initial commit"`
    *   Create a repository on GitHub and push your code there.

2.  **Sign up for Streamlit Cloud**
    *   Go to [share.streamlit.io](https://share.streamlit.io/)
    *   Sign in with your GitHub account.

3.  **Deploy**
    *   Click **"New App"**.
    *   Select your GitHub repository (`Silent-Guardian-AI`).
    *   Select the branch (usually `main`).
    *   Set the "Main file path" to `app.py`.
    *   Click **"Deploy!"**.

## Requirements
Ensure you have the `requirements.txt` file in your repository (created in the previous step). Streamlit Cloud uses this to install the necessary libraries (`pydeck`, `pandas`, etc.).
