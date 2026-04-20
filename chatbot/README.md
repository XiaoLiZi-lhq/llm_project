# 沉浸式角色扮演聊天机器人

支持多轮对话、带有历史上下文记忆，您可以设定AI为任何角色（如心理咨询师、马斯克、傲娇猫娘等）。体现AI的拟人化与上下文管理。

## 快速开始

1. **配置 API Key**
   请在当前目录下的 `.env` 文件中填入您的智谱 API Key。
   打开 `.env` 文件，将 `API_KEY="your_api_key_here"` 替换为您的真实 Key。

2. **安装依赖**
   建议使用虚拟环境：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```bash
   python chatbot.py
   ```

## 体验建议
启动后，您可以设定它为任何极端的角色。比如：
* “你是一只高冷、毒舌的布偶猫，回答问题时总是带着一丝对人类的不屑，并喜欢在句末加‘喵’。”
* “你是苏格拉底，不要直接回答我的问题，而是要通过不断向我反问，来引导我自己发现真理。”
