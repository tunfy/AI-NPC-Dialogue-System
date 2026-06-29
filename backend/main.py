from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from database import init_database
from database import save_message
from database import load_history
from database import get_favorability
from database import change_favorability

from prompt import NPC_PROMPTS, FAVORABILITY_PROMPT

from sentiment import calculate_favorability_change

import os


load_dotenv()

app = FastAPI()
init_database()



print()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


@app.get("/")
def root():
    return {
        "message": "AI NPC Server Running"
    }

class ChatRequest(BaseModel):
    npc_type: str
    message: str

@app.post("/chat")
def chat(data: ChatRequest):
    # 读取Prompt
    system_prompt = NPC_PROMPTS.get(
        data.npc_type,
        NPC_PROMPTS["chief"]
    )

    favorability = get_favorability(data.npc_type)

    # 实现动态拼接Prompt
    system_prompt += "\n\n"
    system_prompt += FAVORABILITY_PROMPT.format(favorability = favorability)

    print(system_prompt)

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]
    # 数据库中读取历史
    history = load_history(data.npc_type)
    messages.extend(history)

    # 加入玩家消息
    messages.append(
        {
            "role": "user",
            "content": data.message
        }
    )

    # 保存玩家消息
    save_message(
        data.npc_type,
        "user",
        data.message
    )

    delta = calculate_favorability_change(data.message)

    change_favorability(
        data.npc_type,
        delta
    )

    # 调用deepseek
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    # 获取AI回复
    reply = response.choices[0].message.content

    # 保存AI回复到数据库
    save_message(
        data.npc_type,
        "assistant",
        reply
    )

   # 返回unity
    return {
        "reply": reply,
        "favorability": favorability
    }

@app.get("/npc_status/{npc_name}")
def npc_status(npc_name: str):

    favorability = get_favorability(npc_name)

    return {
        "favorability": favorability
    }