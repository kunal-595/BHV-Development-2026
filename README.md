# Behavioral Health Vault (BHV) 2026

The Behavioral Health Vault (BHV) is a minimalist, single-command functional prototype designed for UAA/UAF behavioral health research. It allows patients to record their recovery journeys through text narratives and visual media, ensuring data ownership through private "Cloud Vaults".

# Features implemented 

 Zero-Config Backend: Powered by FastAPI and SQLite for immediate deployment.
Dual-Layer Storage:
    Local Vault: Narratives and image metadata stored in `vault.db` (SQLModel).
    Cloud Sync: Automated creation of Private GitHub Repositories for each patient to ensure data sovereignty.
Dynamic Recovery Gallery: A real-time UI that displays stored narratives and images locally.
Automatic Deduplication: Logic to prevent duplicate entries during browser refreshes or resubmissions.

## Project Structure

* `main.py`: The core FastAPI application logic.
* `models.py`: Database blueprints using SQLModel.
* `github_service.py`: Integration with the GitHub API via PyGithub.
* `database/`: Contains the binary `vault.db` SQLite file.
* `uploads/`: Local directory for patient-provided media.

# Clone the repository
git clone  https://github.com/kunal-595/BHV-Development-2026.git
cd BHV-Development-2026
# Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
# Install the Toolkit
pip install -r requirements.txt
# Launch the Vault
python main.py

