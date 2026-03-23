from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import date, datetime, timedelta
import os
import hashlib
import secrets
from dotenv import load_dotenv

from database import get_db
from models import Paciente, Consulta, User, Base
from sqlalchemy import create_engine

# Carregar variáveis de ambiente
load_dotenv()

# Funções de criptografia
def get_password_hash(password: str) -> str:
    """Gera hash da senha usando SHA-256 com salt"""
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

# Configuração do banco
SQLALCHEMY_DATABASE_URL = "sqlite:///./naturasync.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NaturaSync", description="Sistema de gestão para Naturologia e Terapia Ocupacional")

# Configurar templates
templates = Jinja2Templates(directory="templates")

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    public_paths = ["/", "/login", "/static"]
    if request.url.path in public_paths:
        return await call_next(request)
    return await call_next(request)

# Rotas de autenticação
@app.get("/")
async def root():
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    # CORREÇÃO: Usando argumentos nomeados para evitar o erro 500
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, username, password)
    if user:
        user.last_login = datetime.utcnow()
        db.commit()
        return {"message": "Login successful", "user": user.username}
    else:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

@app.get("/logout")
async def logout():
    return RedirectResponse(url="/login", status_code=302)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    pacientes = db.query(Paciente).all()
    total_pacientes = len(pacientes)
    
    hoje = datetime.now().date()
    consultas_hoje = db.query(Consulta).filter(
        Consulta.data_consulta >= datetime.combine(hoje, datetime.min.time()),
        Consulta.data_consulta < datetime.combine(hoje + timedelta(days=1), datetime.min.time()),
        Consulta.status == 'agendada'
    ).count()
    
    inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    novos_mes = len([p for p in pacientes if p.data_cadastro and p.data_cadastro >= inicio_mes])
    pacientes_recentes = pacientes[:5]
    
    count_naturopatia = len([p for p in pacientes if p.avaliacao_inicial and p.avaliacao_inicial.get('abordagem') == 'naturopatia'])
    count_to = len([p for p in pacientes if p.avaliacao_inicial and p.avaliacao_inicial.get('abordagem') == 'terapia_ocupacional'])
    
    proximas_consas_db = db.query(Consulta).filter(
        Consulta.data_consulta >= datetime.now(),
        Consulta.status == 'agendada'
    ).order_by(Consulta.data_consulta).limit(5).all()
    
    proximas_consultas = []
    for consulta in proximas_consas_db:
        paciente = db.query(Paciente).filter(Paciente.id == consulta.paciente_id).first()
        if paciente:
            dt_c = consulta.data_consulta
            proximas_consultas.append({
                "dia": dt_c.day,
                "mes": dt_c.strftime('%b').upper(),
                "paciente": paciente.nome,
                "horario": dt_c.strftime('%H:%M'),
                "tipo": consulta.tipo_consulta
            })
    
    # CORREÇÃO: Passando request e context separadamente
    return templates.TemplateResponse(
        request=request, 
        name="dashboard.html", 
        context={
            "total_pacientes": total_pacientes,
            "consultas_hoje": consultas_hoje,
            "novos_mes": novos_mes,
            "pacientes_recentes": pacientes_recentes,
            "count_naturopatia": count_naturopatia,
            "count_to": count_to,
            "proximas_consultas": proximas_consultas
        }
    )

@app.get("/pacientes", response_class=HTMLResponse)
async def listar_pacientes(request: Request, db: Session = Depends(get_db)):
    pacientes = db.query(Paciente).all()
    return templates.TemplateResponse(request=request, name="pacientes.html", context={"pacientes": pacientes})

@app.get("/pacientes/novo", response_class=HTMLResponse)
async def novo_paciente_form(request: Request):
    return templates.TemplateResponse(request=request, name="form_paciente.html", context={"paciente": None})

@app.get("/pacientes/{paciente_id}/editar", response_class=HTMLResponse)
async def editar_paciente_form(paciente_id: int, request: Request, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return templates.TemplateResponse(request=request, name="form_paciente.html", context={"paciente": paciente})

@app.get("/consultas/novo", response_class=HTMLResponse)
async def nova_consulta_form(request: Request, db: Session = Depends(get_db)):
    pacientes = db.query(Paciente).all()
    return templates.TemplateResponse(request=request, name="agendar_consulta.html", context={"pacientes": pacientes})

@app.post("/consultas")
async def criar_consulta(
    paciente_id: int = Form(...),
    data_consulta: str = Form(...),
    tipo_consulta: str = Form(...),
    status: str = Form("agendada"),
    observacoes: str = Form(""),
    db: Session = Depends(get_db)
):
    try:
        dt = datetime.fromisoformat(data_consulta.replace('T', ' '))
        consulta = Consulta(
            paciente_id=paciente_id,
            data_consulta=dt,
            tipo_consulta=tipo_consulta,
            status=status,
            observacoes=observacoes
        )
        db.add(consulta)
        db.commit()
        return RedirectResponse(url="/dashboard", status_code=302)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao agendar consulta: {str(e)}")

@app.get("/admin/usuarios", response_class=HTMLResponse)
async def admin_usuarios(request: Request, db: Session = Depends(get_db)):
    usuarios = db.query(User).all()
    return templates.TemplateResponse(
        request=request, 
        name="admin_usuarios.html", 
        context={"usuarios": usuarios, "current_user": "darlan"}
    )

@app.get("/perfil/alterar-senha", response_class=HTMLResponse)
async def alterar_senha_page(request: Request):
    return templates.TemplateResponse(request=request, name="alterar_senha.html")

# Mantive as rotas de API (POST/PUT/DELETE) que retornam JSON, pois elas não usam templates.
# ... (restante do código original de API)

