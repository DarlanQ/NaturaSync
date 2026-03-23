from sqlalchemy import Column, Integer, String, Date, Text, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    
    # Campos genéricos de anamnese para múltiplas abordagens terapêuticas
    motivo_consulta = Column(Text, nullable=False)  # Razão principal da busca
    historico_saude = Column(Text, nullable=True)   # Histórico médico e saúde geral
    habitos_vida = Column(Text, nullable=True)     # Hábitos diários, alimentação, sono
    
    # Campos específicos organizados por categorias (JSON para flexibilidade)
    avaliacao_inicial = Column(JSON, nullable=True)  # Dados específicos por abordagem
    objetivos_tratamento = Column(JSON, nullable=True)  # Metas personalizadas
    evolucao = Column(JSON, nullable=True)  # Registro do progresso
    
    # Campos administrativos
    data_cadastro = Column(DateTime, nullable=False, default=datetime.utcnow)
    observacoes_gerais = Column(Text, nullable=True)
    
    # Relacionamento com consultas
    consultas = relationship("Consulta", back_populates="paciente")

class Consulta(Base):
    __tablename__ = "consultas"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    data_consulta = Column(DateTime, nullable=False)
    tipo_consulta = Column(String(50), nullable=False)  # "Naturologia" ou "Terapia Ocupacional"
    status = Column(String(20), default="agendada")  # "agendada", "realizada", "cancelada"
    observacoes = Column(Text, nullable=True)
    
    # Relacionamento com paciente
    paciente = relationship("Paciente", back_populates="consultas")
