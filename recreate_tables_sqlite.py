from sqlalchemy import create_engine
from models import Base, Paciente

# Usando SQLite temporariamente para demonstração
SQLALCHEMY_DATABASE_URL = "sqlite:///./naturasync.db"

print("Conectando ao banco SQLite (temporário)...")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

print("Deletando tabelas existentes...")
Base.metadata.drop_all(bind=engine)

print("Recriando tabelas com nova estrutura...")
Base.metadata.create_all(bind=engine)

print("Tabelas recriadas com sucesso!")
print(f"Estrutura da tabela '{Paciente.__tablename__}':")
print("- Campos básicos: id, nome, data_nascimento, cpf, email")
print("- Anamnese: motivo_consulta, historico_saude, habitos_vida")
print("- JSON flexíveis: avaliacao_inicial, objetivos_tratamento, evolucao")
print("- Administrativos: data_cadastro, observacoes_gerais")
