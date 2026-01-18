from github import Github
import os

# Use an environment variable to keep your token secret
# To set this on Windows terminal: $env:GITHUB_TOKEN="your_token_here"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Initialize GitHub only if token exists
g = Github(GITHUB_TOKEN) if GITHUB_TOKEN else None

def create_private_vault(patient_name: str):
    """Creates a private repo for the patient to ensure data sovereignty."""
    if not g:
        print("GitHub Error: GITHUB_TOKEN not found in environment variables.")
        return None
        
    user = g.get_user()
    repo_name = f"BHV-Vault-{patient_name.replace(' ', '-').lower()}"
    
    try:
        # Check if repo already exists, otherwise create it
        try:
            repo = user.get_repo(repo_name)
        except:
            repo = user.create_repo(repo_name, private=True)
            repo.create_file("README.md", "Initial setup", f"# {patient_name}'s Vault")
        
        return repo.full_name
    except Exception as e:
        print(f"GitHub Error: {e}")
        return None

def upload_file_to_vault(repo_full_name: str, file_path: str):
    """Pushes the recovery image to the GitHub vault."""
    if not g:
        return False
        
    repo = g.get_repo(repo_full_name)
    file_name = os.path.basename(file_path)
    
    with open(file_path, "rb") as f:
        content = f.read()
    
    # Upload to the cloud
    repo.create_file(file_name, f"New recovery entry: {file_name}", content)
    return True