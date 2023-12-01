"""

project topic 相關路由

以下的 endpoint 會以 "<api_prefix>/topic" 開頭

"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import api_schemas
from app.schemas import db_schemas
from app.api import deps
from app import crud

router = APIRouter()


@router.get("/", summary="取得所有 topic 資料", response_model=List[api_schemas.Topic])
def get_all_topic(db: Session = Depends(deps.get_db)):
    topics = crud.topic.get_multi(db)

    return topics


# TODO 這邊需要認證使用者，管理員身份才能新增
@router.post("/", summary="新增 topic", response_model=api_schemas.Topic, status_code=201)
def create_topic(item: api_schemas.TopicCreate, db: Session = Depends(deps.get_db)):
    topic_obj = db_schemas.TopicDBCreate(name=item.name)

    if crud.topic.get_by_name(db, name=item.name):
        raise HTTPException(status_code=409, detail="The topic name is exist.")

    topic = crud.topic.create(db, obj_in=topic_obj)

    return topic


# TODO 這邊需要認證使用者，管理員身份才能新增
@router.patch("/{topic_id}", summary="更新 topic", response_model=api_schemas.Topic)
def update_topic(topic_id: int, item: api_schemas.TopicUpdate, db: Session = Depends(deps.get_db)):
    topic = crud.topic.get(db, topic_id)

    if topic is None:
        raise HTTPException(status_code=404)

    if crud.topic.get_by_name(db, name=item.name):
        raise HTTPException(status_code=409, detail="The topic name is exist.")

    update_topic_obj = db_schemas.TopicDBUpdate(name=item.name)

    update_topic = crud.topic.update(db, db_obj=topic, obj_in=update_topic_obj)

    return update_topic
