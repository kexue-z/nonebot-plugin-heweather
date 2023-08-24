<p align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://user-images.githubusercontent.com/44545625/209862575-acdc9feb-3c76-471d-ad89-cc78927e5875.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
</p>

<div align="center">

# nonebot-plugin-heweather

_✨ 获取和风天气信息并转换为图片 ✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/kexue-z/nonebot-plugin-heweather/master/LICENSE">
    <img src="https://img.shields.io/github/license/kexue-z/nonebot-plugin-heweather.svg" alt="license">
  </a>
  <a href="https://pypi.org/project/nonebot-plugin-heweather/">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-heweather" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</p>

<div align="center">

# 使用 html+playwright 来渲染好看的！

<img src="docs/weather.png"  width="50%">
</div>

- 使用了~~自产自销的~~[nonebot-plugin-htmlrender](https://github.com/kexue-z/nonebot-plugin-htmlrender)
- **需要先保证 playwright 可以正常运行并在系统（或容器中）存在中文字体**

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

## api 类型 必须配置 环境配置

0 = 普通版 **免费订阅** (3 天天气预报)
1 = 个人开发版 **标准订阅** (7 天天气预报)
2 = 商业版 (7 天天气预报)

```
QWEATHER_APITYPE = 0
```

## 逐小时类型 可选配置 环境变量

1 = 未来12小时 (默认值)
2 = 未来24小时

```
QWEATHER_HOURLYTYPE = 1
```

## APIKEY 获取方式

**1、注册和风天气账号**  
进入官网注册[https://id.qweather.com/#/login](https://id.qweather.com/#/login)  
**2、进入控制台**  
登录后，点击 “和风天气开发者控制台”  
**3、创建项目**  
点击控制台左侧 “项目管理”，然后点击 “创建项目”，根据提示自行填写  
“选择订阅” -> “免费订阅”，“设置 KEY” -> “Web API”，都填好后“创建”  
**4、获取 key 并配置.env.xx**  
返回 “项目管理”，可以看到创建的项目，点击 KEY 下面的 “查看”，复制 KEY 到你的.env.xx 即可。
