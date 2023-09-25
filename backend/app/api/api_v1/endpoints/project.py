"""

專案計畫相關路由

"""

from typing import Optional

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/", summary="取得所有的專案計畫資料")
def get_all_project(limit: Optional[int] = Query(default=10, ge=1, le=10, description="一次回傳的專案數量")):
    """取得所有的專案資料"""

    pass


@router.post("/", summary="新增一個專案計畫")
def create_project(item):
    """新增專案"""

    pass


@router.get("/me", summary="取得所有屬於使用者自己的專案計畫")
def get_user_project(
    limit: Optional[int] = Query(default=10, ge=1, le=10, description="一次回傳的專案數量")
):
    """取得使用者的專案資料"""

    pass


@router.get("/{project_id}", summary="取得指定專案計畫的詳細資料")
def get_project(project_id: int):
    """取得專案的詳細資料"""

    pass
