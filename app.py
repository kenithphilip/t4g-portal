from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/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'

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    data = request.json
    
    # Check if the event is related to branch protection rule changes
    if 'commits' in data:
        repo_name = data['repository']['full_name']
        branch = data['ref'].split('/')[-1]
        pusher_name = data['pusher']['name']
        commit_messages = [commit['message'] for commit in data['commits']]
        commit_urls = [commit['url'] for commit in data['commits']]
        
        message_text = f"Branch protection rules for repository `{repo_name}` on branch `{branch}` have been modified by `{pusher_name}`.\n"
        for i, msg in enumerate(commit_messages):
            message_text += f"\nCommit {i+1}:\n* Message: {msg}\n* URL: {commit_urls[i]}\n"
        
        message = {
            "text": message_text
        }

        response = requests.post(SLACK_WEBHOOK_URL, json=message)

        if response.status_code != 200:
            return jsonify({'status': 'error', 'message': 'Failed to send message to Slack'}), response.status_code
        
        return jsonify({'status': 'ok'}), 200

    return jsonify({'status': 'ignored'}), 200

if __name__ == '__main__':
    app.run(port=5000)
