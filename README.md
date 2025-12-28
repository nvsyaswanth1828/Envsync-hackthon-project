# Envsync-hackthon-project#  Envsync — dev_setup CLI (MVP)

*Envsync MVP* helps teams sync their development environment easily.  
The *Manager (Team Lead)* uploads project configuration (tool names + download links) using the *Web Dashboard, and the rest of the team pulls the same config using the *dev_setup CLI command**.

---

##  MVP Flow

1. Manager logs in through *login page (Landing.jsx)*
2. Manager opens the *Manager Dashboard (Dashboard.jsx)*
3. Manager uploads:
   - *Project Name*
   - *Tools list (comma-separated)*
   - *Source URLs (comma-separated string)*
4. Config gets stored in *Firebase Firestore*
5. Team members run the CLI:
   bash
   dev_setup <Project-Name>
   
6. CLI checks each tool:
   - If it *exists locally → skips*
   - If it *does NOT exist → downloads installer*
7. After checking all tools, CLI *terminates successfully* 

---

## Installation (For Teammates)

Clone the repo:

bash
git clone https://github.com/nachikethnks-2007/dev-setup-cli.git


Go into the folder:

bash
cd dev-setup-cli


Install dependencies:

bash
npm install


Run the manager login webpage:

bash
npm start


---

## Using the CLI

After Firestore config is uploaded, team members can pull it like this:

bash
dev_setup IoT-Weather-Hub


CLI will:
- Fetch project config from Firestore
- Validate installed tools
- Download missing tool installers

---

##  Current Supported Tools Example

vscode, postman, python, node


---

## Tech Stack Used in MVP
- React.js (Frontend)
- Tailwind CSS (UI Styling)
- Firebase Firestore (Config Storage)
- Python CLI (Tool validation + Downloading)

---
## Team Name
MVGR Tech Minds
