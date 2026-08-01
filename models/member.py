class Member:
    def __init__(self, member_id, name, email):
        self.id = member_id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"[{self.id}] {self.name} <{self.email}>"
