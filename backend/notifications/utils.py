import firebase_admin
from firebase_admin import firestore

db = firestore.client()

def send_notification(title, message, django_user_ids=None,scheduled_time=None,initial_page_name="calendar"):
    users_ref = db.collection("users")

    user_refs_str = ""
    if django_user_ids:
        query = users_ref.where(filter=firestore.FieldFilter("django_id", "in", django_user_ids))
        user_docs = list(query.stream())

        if not user_docs:
            print(f"No matching users found for provided Django IDs: {django_user_ids}")
            return False

        user_refs_str = ",".join([f"/users/{user.id}" for user in user_docs])

    notification_payload = {
        "notification_title": title,
        "notification_text": message,
        "initial_page_name": initial_page_name,
        "user_refs": user_refs_str,
        "timestamp": firestore.SERVER_TIMESTAMP,
    }

    if scheduled_time:
        notification_payload["scheduled_time"] = scheduled_time
        
    try:
        db.collection("ff_push_notifications").add(notification_payload)
        print(f"Notification created in ff_push_notifications for users: {django_user_ids}")
        return True
    except Exception as e:
        print(f"Error creating notification: {e}")
        return False
