import sqlite3
import hashlib
import secrets
from datetime import datetime

def hash_password(password: str) -> str:
    """Criptografa a senha usando SHA-256 com salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${password_hash}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha plain corresponde ao hash"""
    try:
        salt, password_hash = hashed_password.split('$')
        computed_hash = hashlib.sha256((plain_password + salt).encode()).hexdigest()
        return password_hash == computed_hash
    except:
        return False

# Conectar ao banco
conn = sqlite3.connect('naturasync.db')
cursor = conn.cursor()

# Criar tabela de usuários se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_login DATETIME
    )
''')

# Limpar usuários existentes
cursor.execute('DELETE FROM users')

# Usuários iniciais
usuarios = [
    {
        'username': 'darlan',
        'password': 'naturasync2026',
        'email': 'darlan@natursync.com'
    },
    {
        'username': 'esposa',
        'password': 'mudar123',
        'email': 'esposa@naturasync.com'
    }
]

# Inserir usuários com senhas criptografadas
for usuario in usuarios:
    password_hash = hash_password(usuario['password'])
    cursor.execute('''
        INSERT INTO users (username, password_hash, email, created_at)
        VALUES (?, ?, ?, ?)
    ''', (usuario['username'], password_hash, usuario['email'], datetime.now()))

conn.commit()
conn.close()

print("✅ Usuários criados com sucesso!")
print(f"✅ {len(usuarios)} usuários cadastrados:")
for usuario in usuarios:
    print(f"  - {usuario['username']} (senha: {usuario['password']})")
print("\n⚠️  Importante: A usuária 'esposa' deve alterar sua senha no primeiro login!")
