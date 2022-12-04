# nonebot-plugin-heweather

获取和风天气信息并转换为图片

# 使用html+playwright来渲染好看的！

- 使用了~~自产自销的~~[nonebot-plugin-htmlrender](https://github.com/kexue-z/nonebot-plugin-htmlrender)
- **需要先保证playwright可以正常运行并在系统（或容器中）存在中文字体**


# 安装

直接使用 `pip install nonebot-plugin-heweather` 进行安装

在 `bot.py` 中 写入 `nonebot.load_plugin("nonebot_plugin_heweather")`

# 指令

`天气+地区` 或 `地区+天气`  
例如：`上海天气` 或 `天气广州`

# 配置

## apikey 必须配置 环境配置

```
QWEATHER_APIKEY = xxx
```

## api类型 必须配置 环境配置

0 = 普通版(3天天气预报)
1 = 个人开发版(7天天气预报)
2 = 商业版 (7天天气预报)


```
QWEATHER_APITYPE = 0
```

## APIKEY获取方式

**1、注册和风天气账号**  
进入官网注册[https://id.qweather.com/#/login](https://id.qweather.com/#/login)  
**2、进入控制台**  
登录后，点击 “和风天气开发者控制台”  
**3、创建项目**  
点击控制台左侧 “项目管理”，然后点击 “创建项目”，根据提示自行填写  
“选择订阅” -> “免费订阅”，“设置KEY” -> “Web API”，都填好后“创建”  
**4、获取key并配置.env.xx**  
返回 “项目管理”，可以看到创建的项目，点击KEY下面的 “查看”，复制KEY到你的.env.xx即可。  
 

