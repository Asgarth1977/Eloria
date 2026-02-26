# HOW_TO_USE.md (Portable Version)

# How to Use Grimlock Portable

Welcome to **Grimlock Portable**, a lightweight, distributable AI assistant version derived from the original Grimlock/Eloria project. This version is intended for easy deployment on other machines without requiring local development setup.

## Getting Started

1. **Download and Extract**  
   - Download the portable package and extract it to any directory on your computer.  

2. **Install Dependencies Automatically**  
   - Grimlock Portable includes a bootstrap script (`bootstrap_env.py`) which installs Python and JavaScript dependencies automatically.  

3. **Configure LM Studio Connection**  
   - Edit `config/app_config.json` to set the LM Studio host/port.  
   - Default is `127.0.0.1:7860`, change to your accessible IP if connecting remotely.  

4. **Launch the App**  
   - Run `run_grimlock.py` to start both backend and frontend.  
   - The interface will open in your default browser.  

5. **Memory & Logs**  
   - Memory and logs are stored relative to the portable folder, keeping the environment self-contained.  

6. **Safe Use Guidelines**  
   - This version is fully functional but limited compared to the developer edition.  
   - Some features (like advanced memory injection or custom scripting) are restricted for safe distribution.  
