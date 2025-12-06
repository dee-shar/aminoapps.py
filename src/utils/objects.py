class BaseModel:
    @staticmethod
    def safe_get(object: dict, *keys, default: str = None):
        try:
            for key in keys:
                object = object[key]
            return object
        except (KeyError, TypeError):
            return default

class ChatThreads(BaseModel):
    def __init__(self, data: list) -> None:
        self.json = data
        self.title: list = []
        self.ndc_id: list = []
        self.content: list = []
        self.thread_id: list = []

    def parse(self):
        for thread in self.json:
            self.title.append(self.safe_get(thread, "title"))
            self.content.append(self.safe_get(thread, "content"))
            self.thread_id.append(self.safe_get(thread, "threadId"))
            self.ndc_id.append(self.safe_get(thread, "ndcId"))
        return self

class CommunityList(BaseModel):
    def __init__(self, data: list) -> None:
        self.json = data
        self.name: list = []
        self.link: list = []
        self.ndc_id: list = []
        self.amino_id: list = []

    def parse(self):
        for community in self.json:
            self.name.append(self.safe_get(community, "name"))
            self.link.append(self.safe_get(community, "link"))
            self.ndc_id.append(self.safe_get(community, "ndcId"))
            self.amino_id.append(self.safe_get(community, "endpoint"))
        return self

class MembersList(BaseModel):
    def __init__(self, data: list)-> None:
        self.json = data
        self.icon: list = []
        self.user_id: list = []
        self.nickname: list = []
        self.created_time: list = []

    def parse(self):
        for member in self.json:
            self.nickname.append(self.safe_get(member, "nickname"))
            self.user_id.append(self.safe_get(member, "uid"))
            self.created_time.append(self.safe_get(member, "createdTime"))
            self.icon.append(self.safe_get(member, "icon"))
        return self

class FromLink(BaseModel):
    def __init__(self, data: dict) -> None:
        self.json = data
        self.path: str | None = None
        self.ndc_id: int | None = None
        self.full_url: str | None = None
        self.object_id: str | None = None
        self.short_url: str | None = None
        self.full_path: str | None = None
        self.short_code: str | None = None
        self.object_type: int | None = None
        self.target_code: int | None = None

    def parse(self):
        extensions = ("extensions", "linkInfo")
        self.path = self.safe_get(self.json, "path")
        self.object_type = self.safe_get(self.json, *extensions, "objectType")
        self.short_code = self.safe_get(self.json, *extensions, "shortCode")
        self.full_path = self.safe_get(self.json, *extensions, "fullPath")
        self.target_code = self.safe_get(self.json, *extensions, "targetCode")
        self.object_id = self.safe_get(self.json, *extensions, "objectId")
        self.short_url = self.safe_get(self.json, *extensions, "shareURLShortCode")
        self.full_url = self.safe_get(self.json, *extensions, "shareURLFullPath")
        self.ndc_id = self.safe_get(self.json, *extensions, "ndcId")
        return self

class UserInfo(BaseModel):
    def __init__(self, data: dict) -> None:
        self.json = data
        self.icon: str | None = None
        self.web_URL: str | None = None
        self.user_id: str | None = None
        self.content: str | None = None
        self.amino_id: str | None = None
        self.nickname: str | None = None
        self.created_time: str | None = None
        self.modified_time: str | None = None

    def parse(self):
        self.amino_id = self.safe_get(self.json, "aminoId")
        self.user_id = self.safe_get(self.json, "uid")
        self.nickname = self.safe_get(self.json, "nickname")
        self.content = self.safe_get(self.json, "content")
        self.icon = self.safe_get(self.json, "icon")
        self.web_URL = self.safe_get(self.json, "webURL")
        self.created_time = self.safe_get(self.json, "createdTime")
        self.modified_time = self.safe_get(self.json, "modifiedTime")
        return self

class BlogsList(BaseModel):
    def __init__(self, data: list) -> None:
        self.json = data
        self.title: list = []
        self.blog_id: list = []
        self.content: list = []
        self.created_time: list = []
        self.modified_time: list = []
        self.comments_count: list = []

    def parse(self):
        for blog in self.json:
            self.blog_id.append(self.safe_get(blog, "blogId"))
            self.title.append(self.safe_get(blog, "title"))
            self.content.append(self.safe_get(blog, "content"))
            self.comments_count.append(self.safe_get(blog, "commentsCount"))
            self.created_time.append(self.safe_get(blog, "createdTime"))
            self.modified_time.append(self.safe_get(blog, "modifiedTime"))
        return self
