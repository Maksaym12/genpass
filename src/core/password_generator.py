import secrets
import string
import random

class PasswordGenerator:
    ALGORITHM_SECRETS = "secrets"
    ALGORITHM_PHONETIC = "phonetic"
    ALGORITHM_PATTERN = "pattern"
    ALGORITHM_MEMORABLE = "memorable"
    
    def __init__(self):
        self.uppercase = string.ascii_uppercase
        self.lowercase = string.ascii_lowercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.current_algorithm = self.ALGORITHM_SECRETS
        
        self.memorable_words = [
            "apple", "banana", "orange", "grape", "melon", "car", "house", "book", 
            "phone", "computer", "dog", "cat", "bird", "fish", "tree", "flower", 
            "sun", "moon", "star", "cloud", "river", "lake", "ocean", "mountain", 
            "forest", "city", "road", "bridge", "door", "window", "table", "chair",
            "ability", "able", "about", "above", "accept", "according", "account", "across", 
            "action", "activity", "actually", "address", "administration", "admit", "adult", 
            "affect", "after", "again", "against", "agency", "agent", "ago", "agree", 
            "agreement", "ahead", "allow", "almost", "alone", "along", "already", "also", 
            "although", "always", "american", "among", "amount", "analysis", "animal", 
            "another", "answer", "anyone", "anything", "appear", "apply", "approach", "area", 
            "argue", "around", "arrive", "article", "artist", "assume", "attack", "attention", 
            "attorney", "audience", "author", "authority", "available", "avoid", "away", "baby", 
            "back", "ball", "bank", "base", "beat", "beautiful", "because", "become", "before", 
            "begin", "behavior", "behind", "believe", "benefit", "best", "better", "between", 
            "beyond", "billion", "black", "blood", "blue", "board", "body", "book", "born", 
            "both", "break", "bring", "brother", "budget", "build", "building", "business", 
            "call", "camera", "campaign", "cancer", "candidate", "capital", "card", "care", 
            "career", "carry", "case", "catch", "cause", "cell", "center", "central", 
            "century", "certain", "certainly", "chair", "challenge", "chance", "change", 
            "character", "charge", "check", "child", "choice", "choose", "church", "citizen", 
            "city", "civil", "claim", "class", "clear", "clearly", "close", "coach", "cold", 
            "collection", "college", "color", "come", "commercial", "common", "community", 
            "company", "compare", "computer", "concern", "condition", "conference", "congress", 
            "consider", "consumer", "contain", "continue", "control", "cost", "could", "country", 
            "couple", "course", "court", "cover", "create", "crime", "cultural", "culture", 
            "current", "customer", "dark", "data", "daughter", "dead", "deal", "death", 
            "debate", "decade", "decide", "decision", "deep", "defense", "degree", "democratic", 
            "describe", "design", "despite", "detail", "determine", "develop", "development", 
            "difference", "different", "difficult", "dinner", "direction", "director", "discover", 
            "discuss", "discussion", "disease", "doctor", "door", "down", "draw", "dream", 
            "drive", "drop", "drug", "during", "each", "early", "east", "easy", "economic", 
            "economy", "edge", "education", "effect", "effort", "eight", "either", "election", 
            "else", "employee", "energy", "enjoy", "enough", "enter", "entire", "environment", 
            "environmental", "especially", "establish", "even", "evening", "event", "ever", 
            "every", "everybody", "everyone", "everything", "evidence", "exactly", "example", 
            "executive", "exist", "expect", "experience", "expert", "explain", "face", "fact", 
            "factor", "fail", "fall", "family", "fast", "father", "fear", "federal", "feel", 
            "feeling", "field", "fight", "figure", "fill", "film", "final", "finally", 
            "financial", "find", "fine", "finger", "finish", "fire", "firm", "first", "fish", 
            "five", "floor", "focus", "follow", "food", "foot", "force", "foreign", "forget", 
            "form", "former", "forward", "four", "free", "friend", "from", "front", "full", 
            "fund", "future", "game", "garden", "general", "generation", "girl", "give", 
            "glass", "goal", "good", "government", "great", "green", "ground", "group", "grow", 
            "growth", "guess", "hand", "hang", "happen", "happy", "hard", "have", "head", 
            "health", "hear", "heart", "heat", "heavy", "help", "here", "herself", "high", 
            "himself", "history", "hold", "home", "hope", "hospital", "hotel", "hour", "house", 
            "however", "huge", "human", "hundred", "husband", "idea", "identify", "image", 
            "imagine", "impact", "important", "improve", "include", "including", "increase", 
            "indeed", "indicate", "individual", "industry", "information", "inside", "instead", 
            "institution", "interest", "interesting", "international", "interview", "into", 
            "investment", "involve", "issue", "item", "itself", "join", "just", "keep", "kill", 
            "kind", "kitchen", "know", "knowledge", "land", "language", "large", "last", "late", 
            "later", "laugh", "lawyer", "lead", "leader", "learn", "least", "leave", "left", 
            "legal", "less", "letter", "level", "life", "light", "like", "likely", "line", 
            "list", "listen", "little", "live", "local", "long", "look", "lose", "loss", 
            "love", "machine", "magazine", "main", "maintain", "major", "majority", "make", 
            "manage", "management", "manager", "many", "market", "marriage", "material", 
            "matter", "maybe", "mean", "measure", "media", "medical", "meet", "meeting", 
            "member", "memory", "mention", "message", "method", "middle", "might", "military", 
            "million", "mind", "minute", "miss", "mission", "model", "modern", "moment", 
            "money", "month", "more", "morning", "most", "mother", "mouth", "move", "movement", 
            "movie", "much", "music", "must", "myself", "name", "nation", "national", "natural", 
            "nature", "near", "nearly", "necessary", "need", "network", "never", "news", 
            "newspaper", "next", "nice", "night", "none", "north", "note", "nothing", "notice", 
            "number", "occur", "offer", "office", "officer", "official", "often", "once", 
            "only", "onto", "open", "operation", "opportunity", "option", "order", "other", 
            "others", "outside", "over", "owner", "page", "pain", "painting", "paper", 
            "parent", "part", "participant", "particular", "particularly", "partner", "party", 
            "pass", "past", "patient", "pattern", "peace", "people", "perform", "performance", 
            "perhaps", "period", "person", "personal", "phone", "physical", "pick", "picture", 
            "piece", "place", "plan", "plant", "play", "player", "point", "police", "policy", 
            "political", "politics", "poor", "popular", "population", "position", "positive", 
            "possible", "power", "practice", "prepare", "present", "president", "pressure", 
            "pretty", "prevent", "price", "private", "probably", "problem", "process", "produce", 
            "product", "production", "professional", "professor", "program", "project", 
            "property", "protect", "prove", "provide", "public", "pull", "purpose", "push", 
            "quality", "question", "quickly", "quite", "race", "radio", "raise", "range", 
            "rate", "rather", "reach", "read", "ready", "real", "reality", "realize", "really", 
            "reason", "receive", "recent", "recently", "recognize", "record", "reduce", 
            "reflect", "region", "relate", "relationship", "religious", "remain", "remember", 
            "remove", "report", "represent", "require", "research", "resource", "respond", 
            "response", "responsibility", "rest", "result", "return", "reveal", "rich", "right", 
            "rise", "risk", "road", "rock", "role", "room", "rule", "safe", "same", "save", 
            "scene", "school", "science", "scientist", "score", "season", "seat", "second", 
            "section", "security", "seek", "seem", "sell", "send", "senior", "sense", "series", 
            "serious", "serve", "service", "seven", "several", "shake", "share", "shoot", 
            "short", "shot", "should", "shoulder", "show", "side", "sign", "significant", 
            "similar", "simple", "simply", "since", "sing", "single", "sister", "site", 
            "situation", "size", "skill", "skin", "small", "smile", "social", "society", 
            "soldier", "some", "somebody", "someone", "something", "sometimes", "song", "soon", 
            "sort", "sound", "source", "south", "southern", "space", "speak", "special", 
            "specific", "speech", "spend", "sport", "spring", "staff", "stage", "stand", 
            "standard", "star", "start", "state", "statement", "station", "stay", "step", 
            "still", "stock", "stop", "store", "story", "strategy", "street", "strong", 
            "structure", "student", "study", "stuff", "style", "subject", "success", "successful", 
            "such", "suddenly", "suffer", "suggest", "summer", "support", "sure", "surface", 
            "system", "table", "take", "talk", "task", "teach", "teacher", "team", "technology", 
            "television", "tell", "tend", "term", "test", "than", "thank", "that", "their", 
            "them", "themselves", "then", "theory", "there", "these", "they", "thing", "think", 
            "third", "this", "those", "though", "thought", "thousand", "threat", "three", 
            "through", "throughout", "throw", "thus", "time", "today", "together", "tonight", 
            "total", "tough", "toward", "town", "trade", "traditional", "training", "travel", 
            "treat", "treatment", "tree", "trial", "trip", "trouble", "true", "truth", "turn", 
            "type", "under", "understand", "unit", "until", "upon", "uses", "value", "various", 
            "very", "victim", "view", "violence", "visit", "voice", "vote", "wait", "walk", 
            "wall", "want", "watch", "water", "weapon", "wear", "week", "weight", "well", 
            "west", "western", "what", "whatever", "when", "where", "whether", "which", "while", 
            "white", "whole", "whom", "whose", "wide", "wife", "will", "wind", "window", "wish", 
            "with", "within", "without", "woman", "wonder", "word", "work", "worker", "world", 
            "worry", "would", "write", "writer", "wrong", "yard", "yeah", "year", "young", "your", 
            "yourself"
        ]
        
    def set_algorithm(self, algorithm):
        if algorithm not in [self.ALGORITHM_SECRETS, self.ALGORITHM_PHONETIC, 
                            self.ALGORITHM_PATTERN, self.ALGORITHM_MEMORABLE]:
            raise ValueError(f"Неподдерживаемый алгоритм: {algorithm}")
        
        self.current_algorithm = algorithm
        return True
        
    def generate(self, length, use_upper=True, use_lower=True, 
                use_digits=True, use_special=True):
        if not any([use_upper, use_lower, use_digits, use_special]):
            raise ValueError("Должен быть выбран хотя бы один тип символов")
        
        if self.current_algorithm == self.ALGORITHM_SECRETS:
            return self._generate_with_secrets(length, use_upper, use_lower, use_digits, use_special)
        elif self.current_algorithm == self.ALGORITHM_PHONETIC:
            return self._generate_phonetic(length, use_upper, use_digits, use_special)
        elif self.current_algorithm == self.ALGORITHM_PATTERN:
            return self._generate_pattern(length, use_upper, use_lower, use_digits, use_special)
        elif self.current_algorithm == self.ALGORITHM_MEMORABLE:
            return self._generate_memorable(use_digits, use_special)
        else:
            return self._generate_with_secrets(length, use_upper, use_lower, use_digits, use_special)
            
    def _generate_with_secrets(self, length, use_upper, use_lower, use_digits, use_special):
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
    
    def _generate_phonetic(self, length, use_upper, use_digits, use_special):
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        
        password = []
        for i in range(0, length, 2):
            if i < length:
                password.append(random.choice(consonants))
            if i + 1 < length:
                password.append(random.choice(vowels))
        
        if use_digits or use_special:
            positions = random.sample(range(len(password)), min(4, len(password)))
            
            for i, pos in enumerate(positions):
                if i < 2 and use_digits and pos < len(password):
                    password[pos] = random.choice(self.digits)
                elif use_special and pos < len(password):
                    password[pos] = random.choice(self.special)
        
        if use_upper:
            capital_positions = random.sample(range(len(password)), min(2, len(password)))
            for pos in capital_positions:
                if pos < len(password) and password[pos].isalpha():
                    password[pos] = password[pos].upper()
        
        result = ''.join(password)
        
        if len(result) > length:
            result = result[:length]
            
        return result
    
    def _generate_pattern(self, length, use_upper, use_lower, use_digits, use_special):
        pattern = ""
        
        if use_upper:
            pattern += "L" * (length // 4 + (1 if length % 4 > 0 else 0))
        if use_lower:
            pattern += "l" * (length // 4 + (1 if length % 4 > 1 else 0))
        if use_digits:
            pattern += "d" * (length // 4 + (1 if length % 4 > 2 else 0))
        if use_special:
            pattern += "s" * (length // 4)
            
        if not pattern:
            pattern = "Llds"
            
        pattern = pattern[:length]
        pattern_list = list(pattern)
        random.shuffle(pattern_list)
        pattern = ''.join(pattern_list)
        
        result = []
        for char in pattern:
            if char == 'L':
                result.append(secrets.choice(self.uppercase))
            elif char == 'l':
                result.append(secrets.choice(self.lowercase))
            elif char == 'd':
                result.append(secrets.choice(self.digits))
            elif char == 's':
                result.append(secrets.choice(self.special))
        
        return ''.join(result)
    
    def _generate_memorable(self, use_digits, use_special):
        word1 = random.choice(self.memorable_words).capitalize()
        word2 = random.choice(self.memorable_words).capitalize()
        
        result = word1 + word2
        
        if use_digits:
            digits = ''.join(secrets.choice(self.digits) for _ in range(2))
            result += digits
            
        if use_special:
            special = secrets.choice(self.special)
            result += special
            
        return result
        
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