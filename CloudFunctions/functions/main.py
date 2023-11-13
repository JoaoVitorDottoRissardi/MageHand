# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import db_fn, https_fn, scheduler_fn

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, db, messaging, exceptions, auth
import firebase_admin
from datetime import datetime, timedelta

app = initialize_app()


# @https_fn.on_request()
# def addmessage(req: https_fn.Request) -> https_fn.Response:
#     """Take the text parameter passed to this HTTP endpoint and insert it into
#     a new document in the messages collection."""
#     # Grab the text parameter.
#     original = req.args.get("text")
#     if original is None:
#         return https_fn.Response("No text parameter provided", status=400)

#     firestore_client: google.cloud.firestore.Client = firestore.client()

#     # Push the new message into Cloud Firestore using the Firebase Admin SDK.
#     _, doc_ref = firestore_client.collection("messages").add({"original": original})

#     # Send back a message that we've successfully written the message
#     return https_fn.Response(f"Message with ID {doc_ref.id} added.")


# @firestore_fn.on_document_created(document="messages/{pushId}")
# def makeuppercase(event: firestore_fn.Event[firestore_fn.DocumentSnapshot | None]) -> None:
#     """Listens for new documents to be added to /messages. If the document has
#     an "original" field, creates an "uppercase" field containg the contents of
#     "original" in upper case."""

#     # Get the value of "original" if it exists.
#     if event.data is None:
#         return
#     try:
#         original = event.data.get("original")
#     except KeyError:
#         # No "original" field, so do nothing.
#         return

# @db_fn.on_value_written(reference=r"{uid}/CandyInformation")
# def syncedStatus(event: db_fn.Event[db_fn.Change]) -> None:
#     # Set the "uppercase" field.
#     print(f"Uppercasing {event.params['pushId']}: {original}")
#     upper = original.upper()
#     event.data.reference.update({"uppercase": upper})
@db_fn.on_value_written(reference=r"{uid}/candyInformation/{candy}/Volume")
def send_volume_notification(event: db_fn.Event[db_fn.Change]) -> None:
    uid = event.params["uid"]
    candy = event.params["candy"]
    min_volume = 10

    volume = db.reference(f"{uid}/candyInformation/{candy}/Volume").get()
    name = db.reference(f"{uid}/candyInformation/{candy}/Name").get()
    if volume <= min_volume:
        print(f"{name} is empty!")
        notification_token = db.reference(f"{uid}/notificationToken").get()
        notification = messaging.Notification(
            title=f"{name} is empty",
            body="Please replenish the storage",
        )

        # Send notifications to all tokens.
        msg = messaging.Message(token=notification_token, notification=notification)
        response: messaging.Response = messaging.send(msg)


@db_fn.on_value_written(reference=r"{uid}/Online")
def send_status_notification(event: db_fn.Event[db_fn.Change]) -> None:
    """Triggers when a user gets a new follower and sends a notification.

    Followers add a flag to `/followers/{followedUid}/{followerUid}`.
    Users save their device notification tokens to
    `/users/{followedUid}/notificationTokens/{notificationToken}`.
    """
    uid = event.params["uid"]

    # If un-follow we exit the function.
    change = event.data
    print(change)
    if change.after:
        title = "Machine is Online! 💡"
        body = "machine is online!"
    else:
        title = "Machine is Offline! 💤"
        body = "machine is offline!"
    print("uid: " + uid)
    token_ref = db.reference(f"{uid}/notificationToken")
    notification_token = token_ref.get()
    print(notification_token)
    if not notification_token:
        print("no notification token")
        return

    notification = messaging.Notification(
        title=title,
        body=body,
    )

    # Send notifications to all tokens.
    msg = messaging.Message(token=notification_token, notification=notification)
    response: messaging.Response = messaging.send(msg)

    # Clean up the tokens that are not registered any more.
    # exception = response.exception
    # message = exception.http_response.json()["error"]["message"]
    # print(message)

@https_fn.on_request()
def machine_is_online(req: https_fn.Request) -> https_fn.Response:
    uid = req.args.get("uid")
    if uid is None:
        return https_fn.Response("No uid parameter provided", status=400)
    online_ref = db.reference(f"{uid}/Online")
    time_ref = db.reference(f"{uid}/LastTime")
    time_ref.set(datetime.now().isoformat())
    if not online_ref.get():
        online_ref.set(True)
    return https_fn.Response("Online status updated")

@https_fn.on_request()
def machine_is_offline(req: https_fn.Request) -> https_fn.Response:
    uid = req.args.get("uid")
    if uid is None:
        return https_fn.Response("No uid parameter provided", status=400)
    online_ref = db.reference(f"{uid}/Online")
    if online_ref.get():
        online_ref.set(False)
    return https_fn.Response("Online status updated")

@scheduler_fn.on_schedule(schedule="*/5  * * * *")
def check_online_status(event: scheduler_fn.ScheduledEvent) -> None:
    result = auth.list_users()
    for user in result.users:
        print("user: " + user.uid)
        time_ref = db.reference(f"{user.uid}/LastTime")
        online_ref = db.reference(f"{user.uid}/Online")
        last_time = time_ref.get()
        print(last_time)
        delta = datetime.now() - datetime.fromisoformat(last_time)
        print(delta)
        status = online_ref.get()
        if status and delta > timedelta(minutes=5):
            online_ref.set(False)

# @https_fn.on_request()
# def test_schedule(req: https_fn.Request) -> https_fn.Response:
#     result = auth.list_users()
#     for user in result.users:
#         print("user: " + user.uid)
#         time_ref = db.reference(f"{user.uid}/LastTime")
#         online_ref = db.reference(f"{user.uid}/Online")
#         last_time = time_ref.get()
#         print(last_time)
#         delta = datetime.now() - datetime.fromisoformat(last_time)
#         print(delta)
#         status = online_ref.get()
#         if status and delta > timedelta(minutes=5):
#             online_ref.set(False)
#     return https_fn.Response("testing")
