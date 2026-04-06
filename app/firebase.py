import os
import json
import firebase_admin
from firebase_admin import credentials, auth

# 🔐 Get Firebase key from environment
firebase_json = os.getenv("FIREBASE_KEY")

# ⚠️ Safety check (very important)
if not firebase_json:
    raise Exception("FIREBASE_KEY environment variable not set")

# 🔥 Initialize Firebase
cred = credentials.Certificate(json.loads(firebase_json))

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)


def verify_firebase_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        return None