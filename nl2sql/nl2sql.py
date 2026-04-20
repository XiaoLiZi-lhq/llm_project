import os
import sys
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

# 初始化客户端
# 目前大多数国内大模型（如DeepSeek, 通义千问, 智谱GLM等）都兼容 OpenAI SDK
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

SYSTEM_PROMPT = """你是一个专业的MySQL数据库架构师和SQL开发专家。
你的任务是将用户的自然语言描述准确地转换为高效、规范的MySQL查询语句。

规则：
1. 只输出纯SQL代码，不要包含任何Markdown格式（如 ```sql ）或多余的解释说明。
2. 确保SQL符合MySQL方言规范。
3. 尽可能使用最佳实践，例如合适的JOIN类型，并在需要时使用别名。
4. 如果用户的描述缺乏表结构信息，请根据常理推断合适的表名和字段名。
"""

def generate_sql(natural_language: str) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": natural_language}
            ],
            temperature=0.1, # 较低的temperature有助于生成更确定、准确的代码
            max_tokens=1000
        )
        # 获取返回内容并清理可能包含的markdown标记
        sql = response.choices[0].message.content.strip()
        if sql.startswith("```sql"):
            sql = sql[6:]
        if sql.startswith("```"):
            sql = sql[3:]
        if sql.endswith("```"):
            sql = sql[:-3]
        return sql.strip()
    except Exception as e:
        return f"-- 生成SQL时发生错误: {str(e)}"

def main():
    print("="*50)
    print("🤖 自然语言转 MySQL 助手已启动！")
    print(f"当前模型: {MODEL_NAME}")
    print("输入您的自然语言需求，按回车生成SQL。输入 'q', 'quit' 或 'exit' 退出。")
    print("="*50)
    
    while True:
        try:
            user_input = input("\n📝 请输入需求: ").strip()
            if user_input.lower() in ['q', 'quit', 'exit']:
                print("再见！👋")
                break
            
            if not user_input:
                continue
                
            print("\n⏳ 正在生成 SQL，请稍候...")
            sql_result = generate_sql(user_input)
            
            print("\n" + "-"*40)
            print("✨ 生成的 MySQL 语句如下:")
            print("\033[96m" + sql_result + "\033[0m") # 使用青色打印SQL，方便阅读
            print("-"*40)
            
        except KeyboardInterrupt:
            print("\n再见！👋")
            break
        except Exception as e:
            print(f"\n❌ 程序发生异常: {str(e)}")

if __name__ == "__main__":
    main()
