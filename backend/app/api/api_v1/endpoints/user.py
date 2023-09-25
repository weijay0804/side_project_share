"""

使用者相關路由

以下的 endpoint 會以 "<api_prefix>/user" 開頭

"""

from fastapi import APIRouter


router = APIRouter()


@router.post("/", status_code=201, summary="新增一個使用者")
def create_user(item):
    """新增使用者"""

    pass


@router.get("/{user_id}/profile", summary="取得詳細的使用者個人資料")
def get_user_profile(user_id: int):
    """取得用戶個人資料"""

    pass


@router.patch("/{user_id}/profile", summary="更新使用者個人資料")
def update_user_profile(user_id: int, item):
    """更新用戶個人資料"""

    pass


@router.get("/{user_id}/profile/simple", summary="取得簡易的使用者個人資料")
def get_user_profile_simple(user_id: int):
    """取得簡易版的用戶個人資料"""

    pass
