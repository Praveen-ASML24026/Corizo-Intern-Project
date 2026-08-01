from .db_config import get_connection
from src.models.member import Member

class MemberDAO:
    def add_member(self, name, email):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO members (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        conn.close()

    def get_all_members(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM members")
        result = cur.fetchall()
        conn.close()
        return [Member(*row) for row in result]

    def get_by_id(self, member_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM members WHERE id=%s", (member_id,))
        row = cur.fetchone()
        conn.close()
        return Member(*row) if row else None
