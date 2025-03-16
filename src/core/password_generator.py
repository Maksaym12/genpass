import random
import string

class PasswordGenerator:
    def __init__(self):
        self.uppercase = string.ascii_uppercase
        self.lowercase = string.ascii_lowercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
    def generate(self, length, use_upper=True, use_lower=True, 
                use_digits=True, use_special=True):
        if not any([use_upper, use_lower, use_digits, use_special]):
            raise ValueError("Должен быть выбран хотя бы один тип символов")
            
        chars = ""
        if use_upper:
            chars += self.uppercase
        if use_lower:
            chars += self.lowercase
        if use_digits:
            chars += self.digits
        if use_special:
            chars += self.special
            
        password = ''.join(random.choice(chars) for _ in range(length))
        return password
        
    def check_strength(self, password):
        score = 0
        
        if len(password) >= 8:
            score += 25
        elif len(password) >= 6:
            score += 10
            
        if any(c in self.uppercase for c in password):
            score += 25
        if any(c in self.lowercase for c in password):
            score += 25
        if any(c in self.digits for c in password):
            score += 15
        if any(c in self.special for c in password):
            score += 10
            
        return min(score, 100) 