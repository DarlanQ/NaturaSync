import sqlite3
import json
from datetime import datetime

# Conectar ao banco SQLite que você está usando
conn = sqlite3.connect('naturasync.db')
cursor = conn.cursor()

# Limpar tabela
cursor.execute('DELETE FROM pacientes')

# Dados de teste
pacientes = [
    (
        'Darlan de Quadros (Teste Naturo)', '1966-10-23', '000.000.000-01', 'darlan@teste.com',
        'Cansaço crônico e busca por equilíbrio', 'Praticante de Artes Marciais', 'Mora no litoral',
        json.dumps({
            "abordagem": "naturopatia",
            "iridologia": {
                "olho_direito": {
                    "iris": "Coloração marrom média com áreas mais claras na zona digestiva",
                    "sinais": {
                        "zona_gastrica": "Anéis de estresse visíveis",
                        "zona_hepatica": "Radios solares na região hepática"
                    }
                },
                "olho_esquerdo": {
                    "iris": "Padrão similar ao direito, com mais fibras radiais",
                    "sinais": {
                        "zona_pancreatica": "Criptas profundas indicando possível disfunção"
                    }
                },
                "interpretacao": {
                    "tendencia_constitucional": "Sensibilidade digestiva e hepática",
                    "pontos_atencao": ["Sistema digestivo", "Fígado", "Pâncreas"],
                    "recomendacoes": ["Desintoxicação", "Alimentação viva", "Fitoterapia"]
                }
            }
        }),
        json.dumps({
            "curto_prazo": ["Alívio do cansaço", "Melhora digestiva"],
            "medio_prazo": ["Equilíbrio energético", "Redução do estresse"],
            "longo_prazo": ["Qualidade de vida otimizada", "Bem-estar integral"]
        }),
        json.dumps({}), 
        datetime.now().isoformat(), 
        "Paciente focado em abordagens naturais, com boa adesão ao tratamento."
    ),
    (
        'Maria Silva (Teste TO)', '1980-05-15', '000.000.000-02', 'maria@teste.com',
        'Dificuldade motora fina', 'Pós-operatório de punho direito', 'Trabalha em escritório como digitadora',
        json.dumps({
            "abordagem": "terapia_ocupacional",
            "avds": {
                "banho": {
                    "nivel_independencia": "independente",
                    "dificuldades": [],
                    "adaptacoes_necessarias": []
                },
                "vestuario": {
                    "nivel_independencia": "dependencia_parcial",
                    "dificuldades": ["Dificuldade com botões", "Fechar zíper"],
                    "adaptacoes_necessarias": ["Velcro em substituição a botões", "Gancho para zíper"]
                },
                "alimentacao": {
                    "nivel_independencia": "dependencia_parcial",
                    "dificuldades": ["Dificuldade com pinça fina", "Cortar alimentos"],
                    "adaptacoes_necessarias": ["Talheres adaptados", "Prato antiderrapante"]
                },
                "higiene_pessoal": {
                    "nivel_independencia": "independente",
                    "dificuldades": ["Dificuldade leve com escova dental"],
                    "adaptacoes_necessarias": ["Escova dental com cabo espesso"]
                }
            },
            "avaliacao_motora": {
                "forca_muscular": {
                    "membro_superior_direito": "4/5",
                    "membro_superior_esquerdo": "5/5"
                },
                "coordenacao": "Levemente prejudicada em tarefas finas",
                "sensibilidade": "Preservada"
            }
        }),
        json.dumps({
            "curto_prazo": ["Independência no vestuário", "Melhora na alimentação"],
            "medio_prazo": ["Retorno ao trabalho com adaptações", "Força muscular otimizada"],
            "longo_prazo": ["Autonomia completa nas AVDs", "Qualidade de vida no trabalho"]
        }),
        json.dumps({}), 
        datetime.now().isoformat(), 
        "Paciente motivada, com bom prognóstico de recuperação funcional."
    )
]

# Inserir os dados
cursor.executemany('''
    INSERT INTO pacientes (nome, data_nascimento, cpf, email, motivo_consulta, historico_saude, habitos_vida, avaliacao_inicial, objetivos_tratamento, evolucao, data_cadastro, observacoes_gerais)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', pacientes)

conn.commit()
conn.close()
print("✅ Dados de teste inseridos com sucesso!")
print(f"✅ {len(pacientes)} pacientes criados com dados detalhados")
