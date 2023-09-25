# Database Schema

[關聯圖](https://dbdiagram.io/d/65088e4002bd1c4a5ecd0f45)

## Users table

使用者表  

|       欄位        |     類型     |    默認值    |       備註       | nullable |
| :---------------: | :----------: | :----------: | :--------------: | :------: |
|        id         |   integer    |              |        PK        |  false   |
|     username      | varchar(30)  |              |      unique      |  false   |
|       email       | varchar(128) |              |      unique      |  false   |
|   password_hash   | varchar(128) |              |                  |  false   |
|    avatar_url     |     text     |              |       null       |   true   |
|       city        | varchar(30)  |     null     |                  |   true   |
|        age        |   tinyint    |     null     |                  |   true   |
|      gender       | varchar(15)  |     null     | (male or female) |   true   |
|  is_email_public  |   boolean    |    false     |                  |  false   |
|      github       | varchar(128) |     null     |                  |   true   |
| is_github_public  |   boolean    |    false     |                  |  false   |
|      discord      | varchar(128) |     null     |                  |   true   |
| is_discord_public |   boolean    |    false     |                  |  false   |
|       skill       |     text     |              |                  |   true   |
|     create_at     |  timestamp   | current_time |                  |  false   |


# Projects table

專案計畫表

|         欄位          |    類型     |    默認值    |                備註                | nullable |
| :-------------------: | :---------: | :----------: | :--------------------------------: | :------: |
|          id           |   integer   |              |                 PK                 |  false   |
|     host_user_id      |   integer   |              |                                    |   true   |
|         title         | varchar(50) |              |                                    |   true   |
|   max_member_number   |   tinyint   |      10      |                                    |  false   |
| current_memner_number |   tinyint   |      0       |                                    |  false   |
|        status         | varchar(20) |   recruit    | (`recruit` or `progress` or `end`) |  false   |
|         intro         | varchar(50) |     null     |                                    |   true   |
|         desc          |    text     |     null     |                                    |   true   |
|       image_url       |    text     |     null     |                                    |   true   |
|       create_at       |  timestamp  | current_time |                                    |  false   |

# Topics table

技術種類表

|   欄位    |    類型     |    默認值    | 備註  | nullable |
| :-------: | :---------: | :----------: | :---: | :------: |
|    id     |   integer   |              |  PK   |  false   |
|   name    | varchar(50) |              |       |  false   |
| create_at |  timestamp  | current_time |       |  false   |
