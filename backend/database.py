import sqlite3

DATABASE_NAME = "npc_memory.db"


def init_database():
    """初始化数据库"""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS conversation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            npc_name TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS npc_status(
    npc_name TEXT PRIMARY KEY,
    favorability INTEGER DEFAULT 50
        )""")

    cursor.executemany("""INSERT OR IGNORE INTO npc_status
    (npc_name, favorability)

    VALUES (?, ?)
    """, [
        ("chief", 50),
        ("merchant", 50),
        ("blacksmith", 50),
        ("guard", 50)
    ])

    conn.commit()
    conn.close()

def save_message(npc_name, role, content):
    """保存一条聊天记录"""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO conversation (npc_name, role, content)
        VALUES (?, ?, ?)""", (npc_name, role, content))

    conn.commit()
    conn.close()

def load_history(npc_name, limit = 20):
    """读取指定NPC最近的聊天记录"""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
     SELECT role, content
        FROM conversation
        WHERE npc_name = ?
        ORDER BY id DESC
        LIMIT ?""", (npc_name, limit))

    rows = cursor.fetchall()

    conn.close()

    # SQL取出来的是最新在前，需要反转
    rows.reverse()

    history = []

    for role, content in rows:
        history.append({
            "role" : role,
            "content" : content
        })

    return history

def get_favorability(npc_name):
    """获取NPC好感度"""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(""" 
        SELECT favorability
        FROM npc_status
        WHERE npc_name = ?
    """, (npc_name,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return 50

def change_favorability(npc_name, delta):
    """修改NPC好感度"""

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE npc_status
        SET favorability = favorability + ?
        WHERE npc_name = ?
    """, (delta, npc_name))

    conn.commit()
    conn.close()
