import sqlite3
import json
from datetime import datetime, timedelta

# Conectar ao banco
conn = sqlite3.connect('naturasync.db')
cursor = conn.cursor()

# Criar tabela de consultas se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        data_consulta TEXT NOT NULL,
        tipo_consulta TEXT NOT NULL,
        status TEXT DEFAULT 'agendada',
        observacoes TEXT,
        FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
    )
''')

# Limpar consultas existentes
cursor.execute('DELETE FROM consultas')

# Buscar pacientes existentes
cursor.execute('SELECT id, nome FROM pacientes')
pacientes = cursor.fetchall()

if len(pacientes) >= 2:
    # Adicionar algumas consultas de teste
    
    # Consulta para hoje (primeiro paciente)
    hoje = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    cursor.execute('''
        INSERT INTO consultas (paciente_id, data_consulta, tipo_consulta, status, observacoes)
        VALUES (?, ?, ?, ?, ?)
    ''', (pacientes[0][0], hoje.isoformat(), 'Naturologia', 'agendada', 'Primeira consulta - avaliação completa'))
    
    # Consulta para amanhã (segundo paciente)
    amanha = (datetime.now() + timedelta(days=1)).replace(hour=14, minute=0, second=0, microsecond=0)
    cursor.execute('''
        INSERT INTO consultas (paciente_id, data_consulta, tipo_consulta, status, observacoes)
        VALUES (?, ?, ?, ?, ?)
    ''', (pacientes[1][0], amanha.isoformat(), 'Terapia Ocupacional', 'agendada', 'Sessão de AVDs'))
    
    # Consulta para daqui a 3 dias (primeiro paciente)
    futuro = (datetime.now() + timedelta(days=3)).replace(hour=10, minute=30, second=0, microsecond=0)
    cursor.execute('''
        INSERT INTO consultas (paciente_id, data_consulta, tipo_consulta, status, observacoes)
        VALUES (?, ?, ?, ?, ?)
    ''', (pacientes[0][0], futuro.isoformat(), 'Naturologia', 'agendada', 'Retorno'))
    
    print(f"✅ {len(pacientes)} pacientes encontrados")
    print("✅ Consultas de teste criadas:")
    print(f"  - Hoje 09:00 - {pacientes[0][1]} (Naturologia)")
    print(f"  - Amanhã 14:00 - {pacientes[1][1]} (Terapia Ocupacional)")
    print(f"  - Em 3 dias 10:30 - {pacientes[0][1]} (Naturologia)")
else:
    print("❌ Nenhum paciente encontrado. Execute seed_data.py primeiro.")

conn.commit()
conn.close()
