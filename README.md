# pixiv_api
the network traffic captured from android pixiv app 

# 声明
### 以下所有 API 均由产品公司自身提供，本人皆从网络获取。获取与共享之行为或有侵犯产品权益的嫌疑。若被告知需停止共享与使用，本人会及时删除此页面与整个项目。请您暸解相关情况，并遵守产品协议。

# 内容
* 登录 
  #### 请求地址: https://oauth.secure.pixiv.net/auth/token  请求方式: POST

  ##### Header部分：

  | 请求头        | 值           |
  | ------------- |:-------------:|
  | UA | PixivAndroidApp/5.0.64 (Android 6.0; Google Pixel C - 6.0.0 - API 23 - 2560x1800 |
  |Content-Type | application/x-www-form-urlencoded |

  ##### Data部分：

  | 参数        | 值           |
  | ------------- |:-------------:|
  | client_id | MOBrBDS8blbauoSck0ZfDbtuzpyT |
  | client_secret | lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj |
  | grant_type | password |
  | username | \<username\> |
  | password | \<password\> |
  | device_token | \<device_token\> |
  | get_secure_url | true |

  #### 返回json:
  ```json
  {
      "response": {
          "access_token": "<access_token>",
          "device_token": "<device_token>",
          "expires_in": 3600,
          "refresh_token": "<refresh_token>",
          "scope": "",
          "token_type": "bearer",  
          "user": {
              "account": "<account>",
              "id": "<id>",
              "is_mail_authorized": true,
              "is_premium": true,
              "mail_address": "<mail_address>",
              "name": "<name>",
              "profile_image_urls": {
                  "px_16x16": "https://source.pixiv.net/common/images/no_profile_ss.png",
                  "px_170x170": "https://source.pixiv.net/common/images/no_profile.png",
                  "px_50x50": "https://source.pixiv.net/common/images/no_profile_s.png"
              },
              "x_restrict": 1
          }
      }
  }
  ```
  #### JSON内容：

  | 参数       | 值           |
  | ------------- |:-------------:|
  | access_token | 用作验证的token，添加到请求的header中 |
  | device_token | 设备token，根据request中的device_token而定 |
  | refresh_token | 用于刷新access_token用 |

******************

* 获取推荐内容
  #### 请求地址: https://app-api.pixiv.net/v1/illust/recommended?filter=for_android&include_ranking_illusts=true 请求方式:GET
  
  ##### Header部分：

  | 请求头        | 值           |
  | ------------- |:-------------:|
  | Authorization | Bearer <access_token> |
  | UA | PixivAndroidApp/5.0.64 (Android 6.0; Google Pixel C - 6.0.0 - API 23 - 2560x1800 |
  |Content-Type | application/x-www-form-urlencoded |
  
  * 其中Authorization字段是一个字符串，格式是"Bearer sometoken",accss_token为登录时返回json中的access_token，也是请求用户相关内容的核心。
  
  ##### 参数值：
  
  | 参数        | 值           |
  | ------------- |:-------------:|
  | filter |    for_android  |
  | include_ranking_illusts | true |
  
  ##### 图片URL可从返回JSON中获取，返回JSON过长
   
******************************
  
* 获取收藏内容
  #### 请求地址:https://app-api.pixiv.net/v1/user/bookmarks/illust?user_id=<user_id>&restrict=public
  ##### Header部分：

  | 请求头        | 值           |
  | ------------- |:-------------:|
  | Authorization | Bearer <access_token> |
  | UA | PixivAndroidApp/5.0.64 (Android 6.0; Google Pixel C - 6.0.0 - API 23 - 2560x1800 |
  |Content-Type | application/x-www-form-urlencoded |
  
  ##### 参数值：
  
  | 参数        | 值           |
  | ------------- |:-------------:|
  | user_id |    <user_id> |
  | restrict | public |
  
  ##### 图片URL可从返回JSON中获取，返回JSON过长
  
***********************************
  
  ### 获取图片
  
  * 获取图片的协议是HTTP/2.0 因此HTTP/1.1的响应是403
  * 在HTTP/2.0 存在pesudo-header,以":"开头 
  
  ##### Header部分：

  | 请求头        | 值           |
  | ------------- |:-------------:|
  | :authority | i.pximg.net |
  | UA | PixivAndroidApp/5.0.64 (Android 6.0; Google Pixel C - 6.0.0 - API 23 - 2560x1800 | 
  | referer | https://app-api.pixiv.net/ |
  
  * 其中:authority是HTTP/2.0的一个伪头
