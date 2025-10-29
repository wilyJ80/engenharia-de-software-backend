"""Seed dados de configuracao (Fase, Artefato)

Revision ID: 920dca1eafe2
Revises: c8125272ace2
Create Date: 2025-10-29 09:15:40.102494

"""
from alembic import op
import sqlalchemy as sa
# Se o Alembic gerar 'sqlmodel.sql.sqltypes.AutoString()'
# adicione: import sqlmodel 


# revision identifiers, used by Alembic.
revision = '920dca1eafe2' # Cole o ID gerado aqui
down_revision = 'c8125272ace2' # Cole o ID anterior aqui
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### INÍCIO DOS DADOS DE SEED ###
    
    # 1. Definimos as tabelas (temporariamente) para o Alembic
    fase_table = sa.Table(
        'fase',
        sa.MetaData(),
        sa.Column('id', sa.UUID),
        sa.Column('nome', sa.String),
        sa.Column('descritivo', sa.Text),
        sa.Column('ordem', sa.Integer),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    artefato_table = sa.Table(
        'artefato',
        sa.MetaData(),
        sa.Column('id', sa.UUID),
        sa.Column('nome', sa.String),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # 2. Inserimos os dados de Fase
    #
    op.bulk_insert(fase_table,
        [
            {'nome': 'Prospecção', 'descritivo': 'Fase de Elaboração da Proposta Executiva', 'ordem': 1},
            {'nome': 'Análise', 'descritivo': 'Fase de Especificação de Requisitos e Modelagem Conceitual', 'ordem': 2},
            {'nome': 'Projeto', 'descritivo': 'Fase de Projeto de Software', 'ordem': 3},
            {'nome': 'Implementação', 'descritivo': 'Fase de Codificação', 'ordem': 4},
            {'nome': 'Testes', 'descritivo': 'Fase de Teste', 'ordem': 5},
            {'nome': 'Implantação', 'descritivo': 'Implantação de Software', 'ordem': 6},
        ]
    )
    
    # 3. Inserimos os dados de Artefato
    #
    op.bulk_insert(artefato_table,
        [
            {'nome': 'Proposta Executiva'},
            {'nome': 'Modelo Conceitual'},
            {'nome': 'Requisitos'},
            {'nome': 'Casos de Uso'},
            {'nome': 'Projeto Arquitetural'},
            {'nome': 'Protótipo de Interface'},
            {'nome': 'Diagrama de Classe'},
            {'nome': 'Esquema Entidade Relacionamento'},
            {'nome': 'Teste Unitário'},
            {'nome': 'Teste Funcional'}, #
            {'nome': 'Código Front-End'},
            {'nome': 'Código Back-End'},
            {'nome': 'Implantação Servidor Homologação'},
            {'nome': 'Implantação Servidor Produção'},
        ]
    )
    
    # 4. Criamos os relacionamentos N:N na tabela 'fase_artefato'
    #   
    
    link_sql = """
    INSERT INTO fase_artefato (fase_id, artefato_id, created_at)
    SELECT 
        (SELECT id FROM fase WHERE nome = :fase_nome),
        (SELECT id FROM artefato WHERE nome = :artefato_nome),
        NOW()
    """
    
    # Dados extraídos do slide "Cadastro de Fase de Projeto"
    op.execute(sa.text(link_sql).bindparams(fase_nome='Prospecção', artefato_nome='Proposta Executiva'))
    
    op.execute(sa.text(link_sql).bindparams(fase_nome='Análise', artefato_nome='Requisitos'))
    op.execute(sa.text(link_sql).bindparams(fase_nome='Análise', artefato_nome='Casos de Uso'))
    op.execute(sa.text(link_sql).bindparams(fase_nome='Análise', artefato_nome='Modelo Conceitual'))
    
    op.execute(sa.text(link_sql).bindparams(fase_nome='Projeto', artefato_nome='Projeto Arquitetural'))
    op.execute(sa.text(link_sql).bindparams(fase_nome='Projeto', artefato_nome='Protótipo de Interface'))
    op.execute(sa.text(link_sql).bindparams(fase_nome='Projeto', artefato_nome='Diagrama de Classe'))
    op.execute(sa.text(link_sql).bindparams(fase_nome='Projeto', artefato_nome='Esquema Entidade Relacionamento'))
    
    op.execute(sa.text(link_sql).bindparams(fase_nome='Implementação', artefato_nome='Código Front-End'))
    op.execute(sa.text(link_sql).bindparams(fase_nome='Implementação', artefato_nome='Código Back-End'))
    
    op.execute(sa.text(link_sql).bindparams(fase_nome='Testes', artefato_nome='Teste Unitário'))
    op.execute(sa.text(link_sql).bindparams(fase_nome='Testes', artefato_nome='Teste Funcional'))

    op.execute(sa.text(link_sql).bindparams(fase_nome='Implantação', artefato_nome='Implantação Servidor Homologação'))
    op.execute(sa.text(link_sql).bindparams(fase_nome='Implantação', artefato_nome='Implantação Servidor Produção'))

    # ### FIM DOS DADOS DE SEED ###


def downgrade() -> None:
    # ### INÍCIO DA LIMPEZA DOS DADOS DE SEED ###
    # A ordem é inversa da criação (N:N primeiro)
    op.execute("DELETE FROM fase_artefato")
    op.execute("DELETE FROM fase")
    op.execute("DELETE FROM artefato")
    # ### FIM DA LIMPEZA DOS DADOS DE SEED ###
    pass