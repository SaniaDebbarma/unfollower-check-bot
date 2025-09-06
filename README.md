# unfollower-check-bot

GitHub Unfollower Bot

A Python script that helps you manage your GitHub network by identifying users you follow who don’t follow you back — with the option to unfollow them directly.

⸻

✨ Features
	•	Fetches your followers and following lists from GitHub.
	•	Identifies users who don’t follow you back.
	•	Provides an interactive option to unfollow them safely.
	•	Uses GitHub API with Personal Access Token (PAT) for authentication.

⸻

⚙️ Requirements
	•	Python 3.7+
	•	GitHub Personal Access Token (PAT) with the user:follow scope.
📦 Installation
	1.	Clone this repository:

 git clone https://github.com/SaniaDebbarma/github-unfollower-bot.git
cd github-unfollower-bot

pip install requests

run the script--->
python github_unfollower_bot.py

You will be prompted for:
	•	Your GitHub username
	•	Your Personal Access Token (PAT) (input hidden for security)

Example workflow:
	•	The script lists all users you follow who don’t follow you back.
	•	You can choose to unfollow them one by one, all at once, or skip.

⸻

🔑 Getting a GitHub Personal Access Token (PAT)
	1.	Go to GitHub Settings → Developer settings → Personal access tokens.
	2.	Generate a new token with the scope:
	•	user:follow
	3.	Copy the token (keep it safe, it will only be shown once).

 ⚠️ Disclaimer

This script uses the official GitHub API.
	•	Be mindful of API rate limits.
	•	Unfollowing users is irreversible unless you manually follow them again.
	•	Use at your own discretion.

⸻

👩‍💻 Author

SaniaDebbarma
