import os
import sys
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

if not API_KEY or "your_api_key_here" in API_KEY:
    print("错误: 未配置 API_KEY。请在 .env 文件中配置您的 API_KEY。")
    sys.exit(1)

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

# ==========================================
# 1. 定义本地的外部工具函数 (Function/Skill)
# ==========================================
def get_weather(city: str) -> str:
    """获取指定城市的实时天气（这是一个真实的外部 API 调用）"""
    try:
        # 使用免费的开源天气 API (wttr.in)
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            temp = current['temp_C']
            desc = current['lang_zh'][0]['value'] if 'lang_zh' in current else current['weatherDesc'][0]['value']
            return f"{city}当前天气：{desc}，气温 {temp}℃"
        return f"抱歉，无法获取 {city} 的天气信息。"
    except Exception as e:
        return f"查询天气时发生错误: {str(e)}"

# ==========================================
# 2. 将工具注册给大模型 (Tools Schema)
# ==========================================
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的实时天气情况。当用户询问某地的天气时，必须调用此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京, 广州, New York",
                    }
                },
                "required": ["city"],
            },
        }
    }
]

# 工具映射表，用于通过字符串名称找到对应的 Python 函数
available_functions = {
    "get_weather": get_weather,
}

def main():
    print("="*50)
    print("🎭 全能 Agent 智能体 (带记忆与联网能力) 已启动！")
    print("="*50)
    
    # 角色设定阶段
    print("\n💡 提示：你可以设定具体的角色，比如：")
    print(" - 暴躁但技术很牛的编程导师")
    print(" - 一只总觉得人类很愚蠢的布偶猫")
    
    character = input("\n👤 请输入您想让AI扮演的角色设定：\n").strip()
    if not character:
        character = "一个友好、全能的AI助手"
        
    system_prompt = f"""你现在的身份是：{character}。
请你完全沉浸在这个角色中，从现在开始，你所有的回答都必须严格符合该角色的语气、口癖、性格和思维方式。
你具备调用外部工具的能力。如果用户询问实时天气，请务必使用提供的 get_weather 工具来获取真实数据，然后再用你的角色语气回答用户。
"""
    
    # 初始化消息列表（记忆系统）
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    print(f"\n🎉 设定成功！[{character}] 已经准备好与您对话了。")
    print("(输入 'q' 或 'quit' 退出对话，输入 'clear' 清空记忆)\n")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("🧑 你: ").strip()
            
            if user_input.lower() in ['q', 'quit', 'exit']:
                print("👋 结束对话，再见！")
                break
            elif user_input.lower() == 'clear':
                messages = [messages[0]]
                print("🧹 (记忆已清空)")
                continue
            elif not user_input:
                continue
                
            messages.append({"role": "user", "content": user_input})
            
            # ==========================================
            # 3. 第一次调用大模型：带上 Tools 让它决策
            # ==========================================
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=tools, # 告诉大模型它拥有哪些工具
                tool_choice="auto", # 让大模型自己决定是否需要调用工具
                temperature=0.8,
            )
            
            response_message = response.choices[0].message
            
            # ==========================================
            # 4. 判断大模型是否决定调用工具 (Function Calling 核心逻辑)
            # ==========================================
            if response_message.tool_calls:
                # 把大模型的“调用指令”存入历史记录
                messages.append(response_message)
                
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)
                    
                    print(f"   [Agent 正在思考] 👉 决定调用工具查数据: {function_name}({function_args})")
                    
                    # 真正执行本地 Python 函数
                    function_response = function_to_call(
                        city=function_args.get("city")
                    )
                    
                    # 把函数执行的结果（天气数据）追加到对话历史中，发给大模型
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )
                
                # ==========================================
                # 5. 第二次调用大模型：让它结合工具返回的数据，生成最终回答
                # ==========================================
                second_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=0.8,
                )
                reply = second_response.choices[0].message.content.strip()
                messages.append({"role": "assistant", "content": reply})
                print(f"\n🤖 [{character}]: {reply}\n")
                
            else:
                # 如果不需要调用工具，直接像普通聊天一样回复
                reply = response_message.content.strip()
                messages.append({"role": "assistant", "content": reply})
                print(f"\n🤖 [{character}]: {reply}\n")
            
            # ==========================================
            # 6. 记忆管理：滑动窗口截断 (Sliding Window)
            # ==========================================
            # 如果对话太长，保留 System Prompt 和最近的 20 条记录，防止 Token 超限
            if len(messages) > 21:
                messages = [messages[0]] + messages[-20:]
                
        except KeyboardInterrupt:
            print("\n👋 结束对话，再见！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {str(e)}")
            if messages and messages[-1].get("role") == "user":
                messages.pop()

if __name__ == "__main__":
    main()
