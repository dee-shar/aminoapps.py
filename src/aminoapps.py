from json import loads
from utils import objects
from base64 import b64decode
from requests import Session
from html_to_json import convert


class AminoApps:
	def __init__(self, device_id: str) -> None:
		self.api = "https://aminoapps.com/api"
		self.web_api = "https://aminoapps.com/web"
		self.community_api = "https://aminoapps.com/c"
		self.partial_api = "https://aminoapps.com/partial"
		self.device_id = device_id
		self.session = Session()
		self.session.headers = {
			"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36",
			"X-Requested-With": "XMLHttpRequest"}

	def _post(self, endpoint: str, data: dict) -> dict:
		return self.session.post(f"{self.api}{endpoint}", json=data).json()

	def _get(self, endpoint: str, params: dict = None) -> dict:
		return self.session.get(f"{self.api}{endpoint}", params=params).json()

	def login_sid(self, sid: str) -> dict:
		padded = sid + "=" * (-len(sid) % 4)
		decoded = b64decode(
			padded.replace("-", "+").replace("_", "/").encode())
		data = loads(decoded[1:-20].decode())
		self.sid = sid
		self.user_id = data["2"]
		self.session.headers["Cookie"] = f"sid={self.sid}"
		return data

	def my_chat_threads(
			self,
			ndc_id: int,
			start: int = 0,
			size: int = 10) -> objects.ChatThreads:
		data = {
			"ndcId": f"x{ndc_id}",
			"start": start,
			"size": size
		}
		response = self._post("/my-chat-threads", data)
		return objects.ChatThreads(response["result"]["threadList"]).parse()

	def get_joined_communities(self) -> dict:
		return convert(self.session.get(
			f"{self.partial_api}/global-chat-communities").text)

	def search_community(self, query: str, page: int = 1) -> dict:
		params = {
			"q": query,
			"page": page
		}
		return convert(self.session.get(
			f"{self.partial_api}/community/search-suggestion", params=params).text)

	def send_message(
			self,
			ndc_id: int,
			thread_id: str,
			message: str,
			message_type: int = 0) -> dict:
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id,
			"message": {
				"content": message,
				"mediaType": 0,
				"type": message_type,
				"sendFailed": False,
				"clientRefId": 0
			}
		}
		return self._post("/add-chat-message", data)

	def send_image(
			self,
			ndc_id: int,
			thread_id: str,
			image_url: str) -> dict:
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id,
			"message": {
				"content": None,
				"mediaType": 100,
				"mediaValue": image_url,
				"type": 0,
				"uploadId": 0,
				"sendFailed": False,
				"clientRefId": 0
			}
		}
		return self._post("/add-chat-message", data)

	def send_sticker(
			self,
			ndc_id: int,
			thread_id: str,
			sticker_id: str) -> dict:
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id,
			"message": {
				"stickerId": sticker_id,
				"stickerType": "Emoji Sticker",
				"mediaValue": f"ndcsticker://{sticker_id}",
				"type": 3,
				"sendFailed": False,
				"clientRefId": 0
			}
		}
		return self._post("/add-chat-message", data)

	def submit_comment(
			self,
			ndc_id: int,
			content: str,
			user_id: str = None,
			blog_id: str = None,
			wiki_id: str = None) -> dict:
		data = {
			"ndcId": ndc_id,
			"content": content
		}
		if blog_id:
			data["postType"] = "blog"
			data["postId"] = blog_id
		elif wiki_id:
			data["postType"] = "wiki"
			data["postId"] = wiki_id
		elif user_id:
			data["postType"] = "user"
			data["postId"] = user_id
		return self._post("/submit_comment", data)

	def update_account(self, nickname: str) -> dict:
		data = {"nickname": nickname}
		return self._post(f"/update-account/{self.user_id}", data)

	def join_thread(self, ndc_id: int, thread_id: str) -> dict:
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id
		}
		return self._post("/join-thread", data)

	def leave_thread(self, ndc_id: int, thread_id: str) -> dict:
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id
		}
		return self._post("/leave-thread", data)

	def follow_user(self, ndc_id: int, user_id: str) -> dict:
		data = {
			"followee_id": user_id,
			"ndcId": f"x{ndc_id}"
		}
		return self._post("/follow-user", data)

	def unfollow_user(self, ndc_id: int, user_id: str) -> dict:
		data = {
			"followee_id": user_id,
			"follower_id": self.user_id,
			"ndcId": f"x{ndc_id}"
		}
		return self._post("/unfollow-user", data)

	def vote(
			self,
			ndc_id: int,
			blog_id: str = None,
			wiki_id: str = None) -> dict:
		data = {"ndcId": ndc_id}
		if blog_id:
			data["logType"] = "blog"
			data["postType"] = "blog"
			data["postId"] = blog_id
		elif wiki_id:
			data["logType"] = "wiki"
			data["postType"] = "wiki"
			data["postId"] = wiki_id
		return self._post("/vote", data)

	def unvote(
			self,
			ndc_id: int,
			blog_id: str = None,
			wiki_id: str = None) -> dict:
		data = {"ndcId": ndc_id}
		if blog_id:
			data["logType"] = "blog"
			data["postType"] = "blog"
			data["postId"] = blog_id
		elif wiki_id:
			data["logType"] = "wiki"
			data["postType"] = "wiki"
			data["postId"] = wiki_id
		return self._post("/unvote", data)

	def join_community(
			self,
			ndc_id: int,
			invite_code: str = None) -> dict:
		data = {"ndcId": ndc_id}
		if invite_code:
			data["InviteCode"] = invite_code
		return self._post("/join", data)

	def leave_community(self, ndc_id: int) -> dict:
		data = {"ndcId": ndc_id}
		return self._post("/leave", data)

	def request_to_join_community(
			self,
			ndc_id: int,
			message: str = None) -> dict:
		data = {"ndcId": ndc_id}
		if message:
			data["message"] = message
		return self._post("/request_join", data)

	def add_flag(
			self,
			ndc_id: int,
			reason: str,
			flag_type: int,
			user_id: str = None,
			blog_id: str = None,
			wiki_id: str = None,
			thread_id: str = None) -> dict:
		data = {
			"flagType": flag_type,
			"message": reason,
			"ndcId": f"x{ndc_id}"
		}
		if user_id:
			data["objectId"] = user_id
			data["objectType"] = 0
		elif blog_id:
			data["objectId"] = blog_id
			data["objectType"] = 1
		elif wiki_id:
			data["objectId"] = wiki_id
			data["objectType"] = 2
		elif thread_id:
			data["objectId"] = thread_id
			data["objectType"] = 12
		return self._post("/add-flag", data)

	def send_active_object(self, ndc_id: int) -> dict:
		data = {
			"ndcId": ndc_id
		}
		return self._post("/community/stats/web-user-active-time", data)

	def get_wss_url(self) -> dict:
		return self._get("/chat/web-socket-url")

	def get_blocked_users(self) -> dict:
		return self._get("/block/full-list")

	def create_chat_thread(
			self,
			ndc_id: int,
			user_id: str,
			message: str,
			thread_type: int = 0) -> dict:
		data = {
			"ndcId": ndc_id,
			"inviteeUids": [user_id],
			"initialMessageContent": message,
			"type": thread_type
		}
		return self._post("/create-chat-thread", data)

	def get_online_users(self, ndc_id: int) -> objects.MembersList:
		response = self._get(f"/x{ndc_id}/online-members")
		return objects.MembersList(
			response["result"]["onlineMembersList"]).parse()

	def check_thread(self, ndc_id: int) -> dict:
		data = {
			"ndcId": f"x{ndc_id}"
		}
		return self._post("/thread-check", data)

	def link_translation(
			self,
			ndc_id: int,
			user_id: str = None,
			blog_id: str = None,
			wiki_id: str = None,
			thread_id: str = None) -> dict:
		data = {
			"ndcId": f"x{ndc_id}"
		}
		if user_id:
			data["objectId"] = user_id
			data["objectType"] = 0
		elif blog_id:
			data["objectId"] = blog_id
			data["objectType"] = 1
		elif wiki_id:
			data["objectId"] = wiki_id
			data["objectType"] = 2
		elif thread_id:
			data["objectId"] = thread_id
			data["objectType"] = 12
		return self._post("/link-translation", data)

	def get_blog_categories(self, ndc_id: int) -> dict:
		params = {"ndcId": ndc_id}
		return self._get("/get-blog-category", params=params)

	def delete_blog(self, ndc_id: int, blog_id: str) -> dict:
		data = {
			"ndcId": f"x{ndc_id}",
			"postId": blog_id,
			"postType": "blog"
		}
		return self._post("/post/delete", data)

	def get_thread_users(
			self,
			ndc_id: int,
			thread_id: str,
			thread_type: str = "default",
			start: int = 0,
			size: int = 10) -> dict:
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id,
			"type": thread_type,
			"start": start,
			"size": size
		}
		return self._post("/members-in-thread", data)

	def get_thread_messages(
			self,
			ndc_id: int,
			thread_id: str,
			size: int = 10) -> dict:
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id,
			"size": size
		}
		return self._post("/chat-thread-messages", data)

	def get_blog_votes(self, ndc_id: int, blog_id: str) -> dict:
		return self._get(f"/x{ndc_id}/blog/{blog_id}/votes")

	def poll_option(
			self,
			ndc_id: int,
			blog_id: str,
			option_id: str) -> dict:
		return self.session.post(
			f"{self.api}/poll-option/x{ndc_id}/{blog_id}/{option_id}/vote").json()

	def register(
			self,
			email: str,
			password: str,
			nickname: str,
			verification_code: str) -> dict:
		data = {
			"email": email,
			"nickname": nickname,
			"phoneNumber": "",
			"secret2": password,
			"validationContext": {
				"data": {"code": verification_code},
				"code": verification_code,
				"identity": email,
				"type": 1,
				"__original": {
					"data": {"code": verification_code},
					"code": verification_code,
					"identity": email,
					"type": 1,
					"__response": {}
				}
			}
		}
		return self._post("/register", data)

	def check_security_validation(
			self,
			email: str,
			verification_code: str) -> dict:
		data = {
			"validationContext": {
				"data": {"code": verification_code},
				"identity": email,
				"type": 1,
				"verifyInfoKey": None
			}
		}
		return self._post("/auth/check-security-validation", data)

	def remove_comment(
			self,
			ndc_id: int,
			comment_id: int,
			blog_id: str = None,
			wiki_id: str = None) -> dict:
		data = {
			"ndcId": ndc_id,
			"commentId": comment_id
		}
		if blog_id:
			data["postType"] = "blog"
			data["postId"] = blog_id
		elif wiki_id:
			data["postType"] = "wiki"
			data["postId"] = wiki_id
		return self._post("/remove_comment", data)

	def find_exist_single_chat(self, ndc_id: int, user_id: str) -> dict:
		data = {
			"ndcId": ndc_id,
			"uid": user_id
		}
		return self._post("/find-exist-single-chat", data)

	def delete_account(self, secret: str) -> dict:
		data = {"secret": secret}
		return self._post("/account/delete-request", data)

	def get_live_threads(
			self,
			ndc_id: int,
			start: int = 0,
			size: int = 10) -> dict:
		params = {"ndcId": f"x{ndc_id}", "start": start, "size": size}
		return self._get("/chat/live-threads", params=params)

	def get_thread(self, ndc_id: int, thread_id: str) -> dict:
		data = {
			"ndcId": f"x{ndc_id}",
			"threadId": thread_id
		}
		return self._post("/get-one-thread", data)

	def get_blog(self, ndc_id: int, blog_id: str) -> dict:
		return self.session.get(
			f"{self.web_api}/x{ndc_id}/blog/{blog_id}").json()

	def get_user_profile(self, ndc_id: int, user_id: str) -> dict:
		data = {
			"ndcId": f"x{ndc_id}",
			"userId": user_id
		}
		return self._post("/chat/get-user-profile", data)

	def pick_locale(self, locale: str = "en") -> dict:
		data = {
			"locale": locale
		}
		return self._post("/pick-locale", data)

	def get_public_chats(self, ndc_id: int) -> dict:
		return convert(self.session.get(
			f"{self.partial_api}/public-chat-threads/x{ndc_id}").text)
