import os
import json
import firebase_admin
from firebase_admin import credentials, auth

firebase_json = os.getenv("FIREBASE_KEY")

print("🔥 FIREBASE_KEY EXISTS:", firebase_json is not None)

if firebase_json:
    print("🔥 FIREBASE_KEY LENGTH:", len(firebase_json))
else:
    print("🔥 FIREBASE_KEY IS EMPTY")

if not firebase_json:
    raise Exception("FIREBASE_KEY NOT SET")

cred = credentials.Certificate(json.loads(firebase_json))

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
    print("🔥 Firebase initialized with service account")


def verify_firebase_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        print("✅ AUD:", decoded_token.get("aud"))
        return decoded_token
    except Exception as e:
        print("❌ TOKEN ERROR:", str(e))
        return None