import bcrypt

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password.decode('utf-8')  # 🔥 Convertit en str pour la base de données

def check_password(password: str, hashed_password: str) -> bool:
    if isinstance(hashed_password, str):  
        hashed_password = hashed_password.encode('utf-8')  # 🔥 Assure que c'est en bytes
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
