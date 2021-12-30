# nonebot-plugin-heweather

获取和风天气信息并转换为图片

# 使用html+playwright来渲染好看的！

- 使用了~~自产自销的~~[nonebot-plugin-htmlrender](https://github.com/kexue-z/nonebot-plugin-htmlrender)
- 需要先保证playwright可以正常运行并在系统（或容器中）存在中文字体


# 安装

直接使用 `pip install nonebot-plugin-heweather` 进行安装

不仅要在 `bot.py` 中 写入 `nonebot.load_plugin("nonebot_plugin_htmlrender")`
还要在 `bot.py` 中 写入 `nonebot.load_plugin("nonebot_plugin_heweather")`

> 因为用到了require 所以 `nonebot_plugin_htmlrender` 要先载入（虽然

# 指令

`天气+地区` 或 `地区+天气`

# 配置

## apikey 必须配置 环境配置

```
QWEATHER_APIKEY = xxx
```

## 是否使用商业版 可选 环境配置

- 不添加则默认开发版

```
QWEATHER_COMMERCIAL = true
```

