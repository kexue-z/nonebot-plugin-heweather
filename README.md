# nonebot-plugin-heweather

获取和风天气信息并转换为图片

# 使用html+playwright来渲染好看的！

- 使用了~~自产自销的~~[nonebot-plugin-htmlrender](https://github.com/kexue-z/nonebot-plugin-htmlrender)
- 需要先保证playwright可以正常运行并在系统（或容器中）存在中文字体


# 安装

直接使用 `pip install nonebot-plugin-heweather` 进行安装
如果是`beta1` 需要 `pip install nonebot-plugin-heweather==0.4.1.1-beta.1`

在 `bot.py` 中 写入 `nonebot.load_plugin("nonebot_plugin_heweather")`

# 指令

`天气+地区` 或 `地区+天气`

# 配置

## apikey 必须配置 环境配置

```
QWEATHER_APIKEY = xxx
```

## api类型 可选配置 环境配置

0 = 普通版(3天天气预报)
1 = 个人开发版(7天天气预报)
2 = 商业版 (7天天气预报)


```
QWEATHER_APITYPE = 
```

