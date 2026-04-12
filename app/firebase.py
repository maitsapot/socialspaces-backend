import os
import json
import firebase_admin
from firebase_admin import credentials, auth

# 🔐 Load Firebase key
firebase_json = os.getenv("FIREBASE_KEY")

# 🔥 Detect mode
IS_DEV_MODE = not firebase_json

if IS_DEV_MODE:
    print("⚠️ Firebase NOT configured — running in DEV MODE")
else:
    try:
        cred = credentials.Certificate(json.loads(firebase_json))

        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)

        print("🔥 Firebase initialized successfully")

    except Exception as e:
        print("❌ Firebase init failed:", str(e))
        IS_DEV_MODE = True


# 🔥 VERIFY FUNCTION (THIS WAS MISSING / BROKEN)
def verify_firebase_token(id_token: str):
    """
    Verifies Firebase token.
    Works in both DEV and PROD.
    """

    # 🔹 DEV MODE → skip verification
    if IS_DEV_MODE:
        print("⚠️ DEV MODE: Skipping Firebase verification")
        return {"uid": "dev-user"}

    # 🔹 PROD MODE → verify token
    try:
        decoded_token = auth.verify_id_token(id_token)
        print("✅ TOKEN VALID:", decoded_token)
        return decoded_token

    except Exception as e:
        print("❌ TOKEN ERROR:", str(e))
        return None