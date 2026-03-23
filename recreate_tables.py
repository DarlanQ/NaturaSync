from sqlalchemy import create_engine
from models import Base, Paciente

# Configuração do banco de dados
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/naturasync"

print("Conectando ao banco: naturasync")
# Criar engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

print("Deletando tabelas existentes...")
Base.metadata.drop_all(bind=engine)

print("Recriando tabelas com nova estrutura...")
Base.metadata.create_all(bind=engine)

print("Tabelas recriadas com sucesso!")
print(f"Tabela '{Paciente.__tablename__}' atualizada com nova estrutura genérica.")
