# API 規格

## 使用者 endpoint

- `/user/`
  
  (POST)  
  新增使用者
  ```json
  {
    "username" : "jay",
    "email" : "test@gamil",
    "password" : "test"
  }
  ```

- `/user/<user_id>/profile/`
  
  (GET)  
  取得使用者個人資料
  ```json
  {
    "user_id" : 1,
    "username" : "jay",
    "city" : "Taipei",
    "age" : 24,
    "gender" : "male",
    "email" : "test@gamil.com",
    "is_email_public" : true,
    "github" : "weijay0804",
    "is_github_public" : false,
    "discord" : "weijay0804",
    "is_discord_public" : false,
    "skill" : ["Python", "JS", "React", "Backend", "MySQL"]
  }
  ```

  (PATCH)  
  (**authenticate**)  

  更新使用者個人資料
  ```json
  {
    "city" : "Taipei",
    "age" : 24,
    "gender" : "male",
    "github" : "weijay0804",
    "is_github_public" : false,
    "discord" : "weijay0804",
    "is_discord_public" : false,
    "skill" : ["Python", "JS", "React", "Backend", "MySQL"]
  } 
  ```

- `/user/<user_id>/profile/simple`  
  
  (GET)  
  取得使用者的部分個人資料
  ```json
    {
    "user_id" : 1,
    "username" : "jay",
    "avatar_url" : "https://....."
    }
  ```

# project endpoin

- `/project/`
  
  (GET)  
  取得所有專案計畫基本資料  

  query:  
  - limit (int): 回傳資料數量  

  ```json
  {
    "items" : [
      {
        "project_id" : 1,
        "title" : "my side project",
        "host_username" : "jay",
        "host_user_avatar_url" : "https://....",
        "max_member_number" : 3,
        "current_member_number" : 0,
        "status" : "recruit",
        "project_intor" : "This is a side project introduction.",
        "topic" : [
          {
            "topic_id" : 1,
            "name" : "Python"
          },
        ]
      }
    ]
  }
  
  ```

  (POST)  
  **(authenticate)**  

  新增專案計畫

  ```json
  {
    "title" : "my side project",
    "project_intro" : "This is a side project introduction",
    "project_desc" : "This is a project description, more detail",
    "project_image_url" : "https://",
    "max_member_number" : 3,
    "topic_id_list" : [1, 3, 5]
  }
  ```

- `/project/me`
  
  (GET)  
  **(authenticate)**  
  
  取得使用者的全部專案計畫

  query:  
  - limit (int): 回傳資料數量  

  ```json
  {
    "items" : [
      {
        "project_id" : 1,
        "title" : "my side project",
        "max_member_number" : 3,
        "current_member_number" : 0,
        "status" : "recruit",
        "project_intro" : "This is a side project introduction.",
        "topic" : [
          {
            "topic_id" : 1,
            "name" : "Python"
          },
        ]
      }
    ]
  }
  ```

- `/project/<project_id>/`
  
  (GET)  
  取得專案計畫詳細資料
  ```json
  {
    "project_id" : 1,
    "title" : "my side project",
    "host_user_id" : 1,
    "host_username" : "jay",
    "host_avatar_url" : "https://....",
    "max_member_number" : 3,
    "current_member_number" : 1,
    "status" : "recruit",
    "project_intor" : "This is a side project introduction.",
    "project_desc" : "This is a project description, more detail",
    "project_image_url" : "https://",
    "topic" : [
      {
        "topic_id" : 1,
        "name" : "Python"
      },
    ],
    "member" : [
      {
        "user_id" : 2,
        "username" : "ben",
        "user_avatar_url" : "https://...."
      }
    ]
  }
  ```
