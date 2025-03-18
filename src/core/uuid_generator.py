import uuid

class UUIDGenerator:
    @staticmethod
    def generate():
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_hyphen_free():
        return str(uuid.uuid4()).replace('-', '')
    
    @staticmethod
    def generate_uppercase():
        return str(uuid.uuid4()).upper()
    
    @staticmethod
    def generate_uppercase_hyphen_free():
        return str(uuid.uuid4()).replace('-', '').upper() 