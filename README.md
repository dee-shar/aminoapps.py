# `aminoapps.py`
A lightweight Web-API wrapper for the social network [Amino](https://aminoapps.com).  
Provides simple access to login, chats, profiles, and Amino internal objects.

## 🚀 Features
- Login via `sid` or email/password  
- Fetch and manage chat threads  
- Send messages  
- Access and edit profile data  
- Fetch community and user information  
- Clean object models (`objects.*`)


## 🧩 Basic Usage
```python
import aminoapps

amino = aminoapps.AminoApps(device_id="")
amino.login_sid(sid="")

account = amino.get_user_profile()
print(f"Logged in as: {account.nickname}")
```
![](https://play-lh.googleusercontent.com/DxURGS6RxF4zwTczWWsPwvaCAHcFUdaJH2JufTAq4fmq6vP4g1ec-U0UweTO-mNtXA=h500)
