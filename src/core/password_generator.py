import secrets
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
        required_chars = []
        
        if use_upper:
            chars += self.uppercase
            required_chars.append(secrets.choice(self.uppercase))
        if use_lower:
            chars += self.lowercase
            required_chars.append(secrets.choice(self.lowercase))
        if use_digits:
            chars += self.digits
            required_chars.append(secrets.choice(self.digits))
        if use_special:
            chars += self.special
            required_chars.append(secrets.choice(self.special))
            
        password_list = [secrets.choice(chars) for _ in range(length - len(required_chars))]
        
        password_list.extend(required_chars)
        
        secrets.SystemRandom().shuffle(password_list)
        
        password = ''.join(password_list)
        return password
        
    def check_strength(self, password):

        length_score = 0
        if len(password) >= 16:
            length_score = 40
        elif len(password) >= 12:
            length_score = 30
        elif len(password) >= 10:
            length_score = 25
        elif len(password) >= 8:
            length_score = 15
        elif len(password) >= 6:
            length_score = 5
        else:
            length_score = 0
        
        char_types_used = 0
        char_type_score = 0
        
        if any(c in self.uppercase for c in password):
            char_types_used += 1
            char_type_score += 10
        
        if any(c in self.lowercase for c in password):
            char_types_used += 1
            char_type_score += 10
        
        if any(c in self.digits for c in password):
            char_types_used += 1
            char_type_score += 10
        
        if any(c in self.special for c in password):
            char_types_used += 1
            char_type_score += 15
        
        diversity_bonus = 0
        if char_types_used >= 4:
            diversity_bonus = 15
        elif char_types_used == 3:
            diversity_bonus = 10
        elif char_types_used == 2:
            diversity_bonus = 5
        
        entropy_bonus = 0
        unique_chars_ratio = len(set(password)) / len(password) if password else 0
        entropy_bonus = int(unique_chars_ratio * 10)
        
        total_score = length_score + char_type_score + diversity_bonus + entropy_bonus
        
        if len(password) < 6:
            total_score = min(total_score, 30)
        
        if len(password) > 16:
            extra_length_bonus = min(10, (len(password) - 16) // 2)
            total_score += extra_length_bonus
        
        return min(total_score, 100) 