import firebase_admin
from firebase_admin import credentials, auth

# 🔥 Load service account file directly
cred = credentials.Certificate("app/firebase_key.json")

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