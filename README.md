<h1>
  <img src="https://static.wikia.nocookie.net/logopedia/images/a/a2/Amino-apps-logo.png/revision/latest?cb=20191209165950" width="100" style="vertical-align:middle;" />
  aminoapps.py
</h1>

> Web-API for the **[aminoapps.com](https://aminoapps.com)** (`aminoapps.com/api`). Unlike the mobile API wrapper, this targets the browser-facing web endpoints such as authentication via session ID, web-based chat, communities, blogs, and more.

---

## Requirements

```
requests
html-to-json
```

> A local `utils/objects.py` module is also required for parsing responses from `my_chat_threads` and `get_online_users`.

---

## Quick Start

```python
from aminoapps import AminoApps

client = AminoApps(device_id="your-device-id")
client.login_sid("your-sid-here")
print(client.user_id)
```

---

## Initialization

```python
AminoApps(device_id: str)
```

| Parameter   | Type  | Description                          |
|-------------|-------|--------------------------------------|
| `device_id` | `str` | Your Amino device ID (required).     |

The client uses a browser-style `User-Agent` and sets `X-Requested-With: XMLHttpRequest` to mimic web requests.

---

## Authentication

### Login with SID
```python
client.login_sid(sid)
```
Decodes the base64 session ID to extract the `user_id`, then attaches it as a cookie for all future requests. This is the only supported login method — no email/password flow (use the mobile wrapper for that).

### Register
```python
client.register(email, password, nickname, verification_code)
```

### Check Security Validation
```python
client.check_security_validation(email, verification_code)
```
Validates a verification code before completing registration.

### Delete Account
```python
client.delete_account(secret)
```

---

## Communities

```python
# Get communities the account has joined (returns parsed HTML)
client.get_joined_communities()

# Search for a community
client.search_community(query, page=1)

# Join a community (optional invite code)
client.join_community(ndc_id, invite_code=None)

# Leave a community
client.leave_community(ndc_id)

# Request to join a private community
client.request_to_join_community(ndc_id, message=None)

# Get public chats in a community (returns parsed HTML)
client.get_public_chats(ndc_id)

# Get blog categories
client.get_blog_categories(ndc_id)

# Send active time (keep-alive ping)
client.send_active_object(ndc_id)
```

---

## Chat (Threads)

```python
# List joined chat threads
client.my_chat_threads(ndc_id, start=0, size=10)

# Get a single thread
client.get_thread(ndc_id, thread_id)

# Check a thread's status
client.check_thread(ndc_id)

# Create a new DM thread
client.create_chat_thread(ndc_id, user_id, message, thread_type=0)

# Find an existing DM thread with a user
client.find_exist_single_chat(ndc_id, user_id)

# Join / leave a thread
client.join_thread(ndc_id, thread_id)
client.leave_thread(ndc_id, thread_id)

# Get thread members
client.get_thread_users(ndc_id, thread_id, thread_type="default", start=0, size=10)

# Get thread messages
client.get_thread_messages(ndc_id, thread_id, size=10)

# Live chat threads
client.get_live_threads(ndc_id, start=0, size=10)

# Get WebSocket URL
client.get_wss_url()
```

---

## Messaging

```python
# Send a text message
client.send_message(ndc_id, thread_id, message, message_type=0)

# Send an image (by URL)
client.send_image(ndc_id, thread_id, image_url)

# Send a sticker
client.send_sticker(ndc_id, thread_id, sticker_id)
```

---

## Users

```python
# Get a user's profile
client.get_user_profile(ndc_id, user_id)

# Get online members in a community
client.get_online_users(ndc_id)

# Follow / unfollow a user
client.follow_user(ndc_id, user_id)
client.unfollow_user(ndc_id, user_id)

# Get blocked users
client.get_blocked_users()

# Update account nickname
client.update_account(nickname)

# Set UI locale
client.pick_locale(locale="en")
```

---

## Blogs & Wikis

```python
# Get a blog post (returns web JSON)
client.get_blog(ndc_id, blog_id)

# Get blog vote counts
client.get_blog_votes(ndc_id, blog_id)

# Vote / unvote on a blog or wiki
client.vote(ndc_id, blog_id=None, wiki_id=None)
client.unvote(ndc_id, blog_id=None, wiki_id=None)

# Delete a blog post
client.delete_blog(ndc_id, blog_id)

# Vote on a poll option
client.poll_option(ndc_id, blog_id, option_id)
```

---

## Comments

```python
# Submit a comment on a blog, wiki, or user profile
client.submit_comment(ndc_id, content, user_id=None, blog_id=None, wiki_id=None)

# Remove a comment
client.remove_comment(ndc_id, comment_id, blog_id=None, wiki_id=None)
```

---

## Reporting

```python
# Flag a user, blog, wiki, or thread
client.add_flag(ndc_id, reason, flag_type, user_id=None, blog_id=None,
                wiki_id=None, thread_id=None)
```

Object type mapping used internally:

| Object   | `objectType` |
|----------|-------------|
| User     | `0`         |
| Blog     | `1`         |
| Wiki     | `2`         |
| Thread   | `12`        |

---

## Utilities

```python
# Translate an object ID into a shareable link
client.link_translation(ndc_id, user_id=None, blog_id=None,
                        wiki_id=None, thread_id=None)
```

---

## Notes

- All methods return raw `dict` responses unless noted otherwise (`get_joined_communities`, `search_community`, and `get_public_chats` return **parsed HTML** via `html-to-json`).
- `my_chat_threads` and `get_online_users` return parsed `objects` from the local `utils` module.
- `ndc_id` is the numeric community ID (used as `x<ndc_id>` in Amino URLs).
- This wrapper targets the **web frontend API** — for the full mobile API (WebSocket listening, device signatures, etc.) see the mobile wrapper.

---
