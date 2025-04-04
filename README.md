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

## API 认证方式

插件支持两种 API 认证方式：

1. API Key (传统方式，不推荐)
2. JWT 认证 (更安全，推荐使用)

### JWT 认证配置（推荐）

参考文档 [身份认证](https://dev.qweather.com/docs/configuration/authentication/) 生成 生成 Ed25519 密钥，并且上传公钥

```env
# 是否使用 JWT 认证，默认为 True
QWEATHER_USE_JWT=true

# JWT sub，即控制台中的项目管理的项目ID
QWEATHER_JWT_SUB=

# JWT Key ID，在控制台上传公钥后获取，凭据 ID
QWEATHER_JWT_KID=

# JWT 私钥文本，需要自行生成，需要单行填写，例如
# qweather_jwt_private_key="-----BEGIN PRIVATE KEY-----\n123abc\n-----END PRIVATE KEY-----"
QWEATHER_JWT_PRIVATE_KEY=
```

### API Key 认证配置（不推荐）

```env
QWEATHER_APIKEY=
```

## API 主机配置

参考文档 [API 配置](https://dev.qweather.com/docs/configuration/api-config/) 在 [控制台-设置](https://console.qweather.com/setting) 获取地址。务必添加 scheme `https://`

```env
# API 主机地址，默认为 https://api.qweather.com
QWEATHER_APIHOST=https://api.qweather.com
```

## API 订阅类型

参考 [订阅](https://dev.qweather.com/docs/finance/subscription/#comparison)

```env
# 0 = 免费订阅 (3-7 天天气预报)
# 1 = 标准订阅 (3-30 天天气预报)
# 2 = 高级订阅 (3-30 天天气预报)
QWEATHER_APITYPE=0
```

## 天气预报配置

```env
# 每日预报天数，默认 3 天 根据订阅类型可选最多 30 天
QWEATHER_FORECASE_DAYS=3

# 逐小时预报类型
# 1 = 未来12小时 (默认值)
# 2 = 未来24小时
QWEATHER_HOURLYTYPE=1
```

## 调试配置

```env
# 是否开启调试模式，默认为 false
DEBUG=false
```

## 配置获取方式

1. 进入[控制台](https://console.qweather.com/)
2. 项目管理 -> 创建项目
3. 创建凭据
4. 选择 JWT 类型，并按照文档创建公钥和私钥
5. 上传公钥并保存提交
6. 设置 -> 开发者信息 -> API Host 获取地址
7. 填写 .env 文件

## 参考文档

[和风天气文档-订阅](https://dev.qweather.com/docs/finance/subscription/)
