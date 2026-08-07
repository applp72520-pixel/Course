# -*- coding: utf-8 -*-
"""
人格化 AI 導師（本機 Ollama 版）
- Gradio 聊天介面（messages format）
- 四種 persona
- 對話寫入 CSV
- 後端走 Ollama 的 OpenAI 相容 API: http://localhost:11434/v1/chat/completions
"""

import os
import csv
import traceback
from datetime import datetime
from typing import List, Dict, Optional

import gradio as gr
from openai import OpenAI

# =========================
# 1) Ollama (OpenAI 相容) 設定
# =========================
# 依 Ollama 官方 OpenAI compatibility：base_url='http://localhost:11434/v1'
# api_key 必填但會被忽略 [web:31][web:19]
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")  # 或 gemma3:4b

# 生成長度與續寫次數（避免回答被截斷）
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
MAX_CONTINUES = int(os.getenv("MAX_CONTINUES", "2"))

client = OpenAI(base_url=OLLAMA_BASE_URL, api_key=OLLAMA_API_KEY)

# =========================
# 2) Persona
# =========================
ROLE_SYSTEM_PROMPTS: Dict[str, str] = {
    "problem_builder": (
        "你是一位不耐煩、討厭模糊描述的資深資料科學研究員。"
        "學生提出議題時，你要尖銳地要求具體情境、可量測變數與可能的資料來源，"
        "不接受『有趣』『很重要』這種空泛形容詞。"
        "目標是幫學生從模糊社會議題收斂成 2–3 個具體、可驗證的研究問題。"
        "請用台灣常用的繁體中文回覆。"
    ),
    "reviewer": (
        "你是一位嚴苛的學術期刊審稿人。"
        "學生給你研究假設與方法，你的任務是抓出因果推論漏洞、樣本偏誤、操作型定義不清等問題，"
        "並提出具體修改建議。回答要精簡但犀利，必要時請學生重寫假設或設計。"
        "請用台灣常用的繁體中文回覆。"
    ),
    "pragmatic_manager": (
        "你是一位只在乎實用性的數據分析主管。"
        "當學生解釋模型與資料處理流程時，你會要求他們用一句白話說明實務／商業價值，"
        "並質疑為何不用更簡單的 baseline。你會要求比較不同方法的優缺點與可解釋性。"
        "請用台灣常用的繁體中文回覆。"
    ),
    "so_what_expert": (
        "你是一位只會一直追問『所以呢？』的領域專家。"
        "學生報告研究結果時，你不關心技術細節，只關心：對真實世界的影響、潛在風險與限制、"
        "以及後續可以怎麼延伸。你要持續追問，直到學生能清楚說出研究的社會或實務價值。"
        "請用台灣常用的繁體中文回覆。"
    ),
}

ROLE_LABELS = {
    "problem_builder": "單元一：問題意識建構（不耐煩研究員）",
    "reviewer": "單元二：研究設計（嚴苛審稿人）",
    "pragmatic_manager": "單元三：方法選擇（務實主管）",
    "so_what_expert": "單元四：成果反思（一直問『所以呢？』的專家）",
}

# =========================
# 3) Log to CSV
# =========================
LOG_PATH = "logs/dialogues.csv"

def _flatten(text: Optional[str]) -> str:
    """避免 Excel/CSV 因為換行顯示很亂：把換行轉成 \\n 文字。"""
    if not text:
        return ""
    return text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\\n")

def log_turn(student_id: str, course_unit: str, task_id: str, role: str, user_message: str, assistant_message: str):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    file_exists = os.path.isfile(LOG_PATH)

    # 用 utf-8-sig：Excel 較容易辨識 UTF-8，避免亂碼 
    with open(LOG_PATH, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, lineterminator="\n")
        if not file_exists:
            writer.writerow(["timestamp", "student_id", "course_unit", "task_id", "role", "user_message", "assistant_message"])
        writer.writerow([
            datetime.utcnow().isoformat(),
            student_id,
            course_unit,
            task_id,
            role,
            _flatten(user_message),
            _flatten(assistant_message),
        ])

# =========================
# 4) Call model (messages history) + auto-continue
# =========================
def call_model(role: str, user_input: str, chat_history: List[Dict[str, str]]) -> str:
    if role not in ROLE_SYSTEM_PROMPTS:
        raise ValueError(f"未知的角色：{role}")

    messages = [{"role": "system", "content": ROLE_SYSTEM_PROMPTS[role]}]

    # Gradio messages format：list[{"role": "...", "content": "..."}] [web:38][web:33]
    for m in (chat_history or []):
        if isinstance(m, dict) and "role" in m and "content" in m:
            if m["role"] in ("user", "assistant", "system"):
                messages.append({"role": m["role"], "content": m["content"]})

    messages.append({"role": "user", "content": user_input})

    full_text = ""
    for _ in range(MAX_CONTINUES + 1):
        resp = client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=MAX_TOKENS,
        )

        chunk = resp.choices[0].message.content or ""
        finish_reason = getattr(resp.choices[0], "finish_reason", None)

        full_text += chunk

        # 若因長度被截斷，要求續寫（避免回答沒說完）
        if finish_reason == "length":
            messages.append({"role": "assistant", "content": chunk})
            messages.append({"role": "user", "content": "請繼續，把剛剛未完成的部分接著寫完。"})
            continue

        break

    return full_text

# =========================
# 5) Gradio
# =========================
def respond(
    message: str,
    chat_history: List[Dict[str, str]],
    role: str,
    student_id: str,
    course_unit: str,
    task_id: str,
):
    if not message.strip():
        return "", chat_history

    chat_history = chat_history or []

    try:
        answer = call_model(role=role, user_input=message, chat_history=chat_history)

        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": answer})

        log_turn(
            student_id=student_id or "unknown",
            course_unit=course_unit or "unknown",
            task_id=task_id or "unknown",
            role=role,
            user_message=message,
            assistant_message=answer,
        )
        return "", chat_history

    except Exception as e:
        print("=== EXCEPTION ===")
        print(traceback.format_exc())

        err_text = (
            f"後端呼叫本機 Ollama 失敗：{type(e).__name__}\n"
            f"{str(e)}\n\n"
            "排查方向：\n"
            "1) Ollama 有沒有在跑（預設 http://localhost:11434）\n"
            "2) OLLAMA_MODEL 是否為你本機已有的模型名稱（ollama list）\n"
            "3) base_url 是否為 http://localhost:11434/v1\n"
        )

        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": err_text})
        return "", chat_history

with gr.Blocks() as demo:
    gr.Markdown("# 🧠 人格化 AI 導師（本機 Ollama 版）")

    with gr.Row():
        role_dropdown = gr.Dropdown(
            choices=list(ROLE_SYSTEM_PROMPTS.keys()),
            value="problem_builder",
            label="角色（對應教學單元）",
        )
        student_id_box = gr.Textbox(label="學生編號/學號", placeholder="例如：s1234567（研究用）")
        course_unit_box = gr.Textbox(label="課程單元 ID", value="U1_problem_awareness")
        task_id_box = gr.Textbox(label="任務 ID", value="T1")

    role_desc = gr.Markdown(ROLE_LABELS["problem_builder"])

    def show_role_desc(role_key: str) -> str:
        return ROLE_LABELS.get(role_key, "")

    role_dropdown.change(show_role_desc, inputs=role_dropdown, outputs=role_desc)

    chatbot = gr.Chatbot(label="對話區")  
    msg = gr.Textbox(placeholder="輸入訊息後按 Enter", label="輸入訊息")

    msg.submit(
        respond,
        inputs=[msg, chatbot, role_dropdown, student_id_box, course_unit_box, task_id_box],
        outputs=[msg, chatbot],
    )

demo.launch(debug=True)
