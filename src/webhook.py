from flask import Blueprint, request, jsonify, redirect, url_for
import hmac
import hashlib
import os

github_webhook_blueprint = Blueprint('github_webhook', __name__)

@github_webhook_blueprint.route('/webhook/github', methods=['POST'])
def webhook_handler():
    signature = request.headers.get('X-Hub-Signature-256')

    webhook_secret = os.environ.get('GITHUB_WEBHOOK_SECRET')
    if not webhook_secret:
        return jsonify({'error': 'Webhook secret is not set'}), 500

    hmac_gen = hmac.new(webhook_secret.encode(), request.data, hashlib.sha256)
    expected_signature = 'sha256=' + hmac_gen.hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        return jsonify({'error': 'Invalid signature'}), 403

    payload = request.json
    print("Received valid webhook from GitHub: ", payload)

    return jsonify({'status': 'success'}), 200