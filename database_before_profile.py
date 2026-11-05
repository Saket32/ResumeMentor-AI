
import sqlite3

DB_NAME = "chat_history.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Store chat sessions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Store chat messages
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Store uploaded document information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            document_id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            session_id TEXT,
            access_type TEXT NOT NULL
                CHECK(access_type IN ('private', 'shared')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Migrate existing conversations without deleting messages
    cursor.execute("""
        SELECT DISTINCT session_id FROM messages
    """)

    old_sessions = cursor.fetchall()

    for (session_id,) in old_sessions:
        cursor.execute("""
            SELECT content FROM messages
            WHERE session_id = ? AND role = 'user'
            ORDER BY id LIMIT 1
        """, (session_id,))

        first_message = cursor.fetchone()
        title = first_message[0][:35] if first_message else "Old Chat"

        cursor.execute("""
            INSERT OR IGNORE INTO sessions (session_id, title)
            VALUES (?, ?)
        """, (session_id, title))

    connection.commit()
    connection.close()


# ---------------- CHAT SESSION FUNCTIONS ----------------

def create_session(session_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO sessions (session_id, title)
        VALUES (?, ?)
    """, (session_id, "New Chat"))

    connection.commit()
    connection.close()


def get_sessions():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT session_id, title
        FROM sessions
        ORDER BY created_at DESC
    """)

    sessions = cursor.fetchall()
    connection.close()

    return sessions


def rename_session(session_id, new_title):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE sessions
        SET title = ?
        WHERE session_id = ?
    """, (new_title, session_id))

    connection.commit()
    connection.close()


# ---------------- CHAT MESSAGE FUNCTIONS ----------------

def save_message(session_id, role, content):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO messages (session_id, role, content)
        VALUES (?, ?, ?)
    """, (session_id, role, content))

    # Give a new chat its title from the first user message
    if role == "user":
        cursor.execute("""
            UPDATE sessions
            SET title = ?
            WHERE session_id = ? AND title = 'New Chat'
        """, (content[:35], session_id))

    connection.commit()
    connection.close()


def get_messages(session_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT role, content
        FROM messages
        WHERE session_id = ?
        ORDER BY id
    """, (session_id,))

    messages = cursor.fetchall()
    connection.close()

    return [
        {"role": role, "content": content}
        for role, content in messages
    ]


def delete_session(session_id):
    connection = get_connection()
    cursor = connection.cursor()

    # Delete chat messages
    cursor.execute("""
        DELETE FROM messages
        WHERE session_id = ?
    """, (session_id,))

    # Delete private document records belonging to this chat
    cursor.execute("""
        DELETE FROM documents
        WHERE session_id = ?
          AND access_type = 'private'
    """, (session_id,))

    # Delete chat session
    cursor.execute("""
        DELETE FROM sessions
        WHERE session_id = ?
    """, (session_id,))

    connection.commit()
    connection.close()


# ---------------- DOCUMENT FUNCTIONS ----------------

def save_document(document_id, filename, session_id, access_type):
    if access_type not in ("private", "shared"):
        raise ValueError("access_type must be 'private' or 'shared'")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO documents (
            document_id,
            filename,
            session_id,
            access_type
        )
        VALUES (?, ?, ?, ?)
    """, (
        document_id,
        filename,
        session_id,
        access_type
    ))

    connection.commit()
    connection.close()


def get_available_documents(session_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT document_id, filename, access_type
        FROM documents
        WHERE access_type = 'shared'
           OR (
               access_type = 'private'
               AND session_id = ?
           )
        ORDER BY created_at DESC
    """, (session_id,))

    documents = cursor.fetchall()
    connection.close()

    return documents
