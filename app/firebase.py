import os
import json
import firebase_admin
from firebase_admin import credentials, auth

firebase_json = os.getenv("FIREBASE_KEY")

if not firebase_json:
    raise Exception("FIREBASE_KEY not set")

cred = credentials.Certificate(json.loads(firebase_json))

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
    print("🔥 Firebase initialized with service account")


def verify_firebase_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        print("✅ TOKEN VALID:", decoded_token)
        return decoded_token
    except Exception as e:
        print("❌ TOKEN ERROR:", str(e))
        return None