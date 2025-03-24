
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.config import get_connection
import streamlit as st
import matplotlib.pyplot as plt
def create_producaomens_table():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS producao_mediamensal_pesquisador (
            id SERIAL PRIMARY KEY,
            pesquisador_id INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            media_pesquisas_diarias FLOAT NOT NULL,
            FOREIGN KEY (pesquisador_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Tabela 'producao_media_pesquisador' criada com sucesso!")




def criar_funcao_media():
    """Cria a função no banco de dados (executar apenas uma vez)."""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
       CREATE OR REPLACE FUNCTION calcular_media_pesquisas_diarias_mes_anteriord()
       RETURNS TABLE(
           pesquisador_id INT,
           ano INT,
           mes INT,
           media_pesquisas_diarias NUMERIC
       ) AS $$
       DECLARE
           dias_do_mes INT;
       BEGIN
           
           SELECT EXTRACT(DAY FROM DATE_TRUNC('MONTH', CURRENT_DATE - INTERVAL '1 month') + INTERVAL '1 MONTH' - INTERVAL '1 DAY')
           INTO dias_do_mes;

           
           INSERT INTO producao_mediamensal_pesquisador (pesquisador_id, ano, mes, media_pesquisas_diarias)
           SELECT 
               s.pesquisador_id,
               CAST(EXTRACT(YEAR FROM p.data) AS INT) AS ano,  
               CAST(EXTRACT(MONTH FROM p.data) AS INT) AS mes,  
               (COUNT(p.id)::numeric) / NULLIF(dias_do_mes, 0) AS media_pesquisas_diarias  
           FROM prices p
           INNER JOIN stores s ON p.loja_id = s.id
           WHERE EXTRACT(MONTH FROM p.data) = EXTRACT(MONTH FROM CURRENT_DATE - INTERVAL '1 month')  
             AND EXTRACT(YEAR FROM p.data) = EXTRACT(YEAR FROM CURRENT_DATE - INTERVAL '1 month')  
           GROUP BY s.pesquisador_id, ano, mes;

           
           RETURN QUERY
           SELECT 
               s.pesquisador_id,
               CAST(EXTRACT(YEAR FROM p.data) AS INT) AS ano,  
               CAST(EXTRACT(MONTH FROM p.data) AS INT) AS mes,  
               (COUNT(p.id)::numeric) / NULLIF(dias_do_mes, 0) AS media_pesquisas_diarias  
           FROM prices p
           INNER JOIN stores s ON p.loja_id = s.id
           WHERE EXTRACT(MONTH FROM p.data) = EXTRACT(MONTH FROM CURRENT_DATE - INTERVAL '1 month')  
             AND EXTRACT(YEAR FROM p.data) = EXTRACT(YEAR FROM CURRENT_DATE - INTERVAL '1 month')  
           GROUP BY s.pesquisador_id, ano, mes;
       END;
       $$ LANGUAGE plpgsql;

    """)
    
    conn.commit()
    cur.close()
    conn.close()
def calcular_media():
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT calcular_media_pesquisas_diarias_mes_anteriord();")  

    conn.commit()
    cur.close()
    conn.close()
    
    print("✅ Média de pesquisas diárias calculada e armazenada!")

def criar_funcao_topdez():
    conn = get_connection()
    cur = conn.cursor()

    func_sql = """
                CREATE OR REPLACE FUNCTION topdez(IN mes_inic INT, IN ano_inic INT, IN mes_fim INT, IN ano_fim INT)
                RETURNS TABLE(
                    pesquisador_id INT,
                    nome TEXT,
                    media_total NUMERIC
                ) AS $$
                BEGIN
                    RETURN QUERY
                    SELECT 
                        p.pesquisador_id,
                        u.nome::TEXT,  
                        AVG(p.media_pesquisas_diarias)::NUMERIC AS media_total
                    FROM producao_mediamensal_pesquisador p
                    JOIN users u ON p.pesquisador_id = u.id  
                    WHERE (p.ano > ano_inic OR (p.ano = ano_inic AND p.mes >= mes_inic))
                    AND (p.ano < ano_fim OR (p.ano = ano_fim AND p.mes <= mes_fim))
                    GROUP BY p.pesquisador_id, u.nome
                    ORDER BY media_total DESC
                    LIMIT 10;
                END;
                $$ LANGUAGE plpgsql;

    """

    cur.execute(func_sql)  
    conn.commit()

    cur.close()
    conn.close()

    print("✅ Função topdez() criada ou atualizada com sucesso!")






import pandas as pd
import psycopg2
import plotly.express as px
import streamlit as st

def mostrar_top_10_grafico():
    st.title("Top 10 Pesquisadores - Produção Média Mensal")

    
    periodos_disponiveis = get_periodos_disponiveis()
    
    if not periodos_disponiveis:
        st.error("⚠️ Nenhum dado disponível no banco de dados.")
        return

    anos_disponiveis = sorted(set(ano for _, ano in periodos_disponiveis))
    
    
    col1, col2 = st.columns(2)

    with col1:
        ano_inic = st.selectbox("Ano Inicial", anos_disponiveis, index=0)
        meses_validos_inic = [mes for mes, ano in periodos_disponiveis if ano == ano_inic]
        mes_inic = st.selectbox("Mês Inicial", meses_validos_inic, index=0)

    with col2:
        ano_fim = st.selectbox("Ano Final", anos_disponiveis, index=len(anos_disponiveis) - 1)
        meses_validos_fim = [mes for mes, ano in periodos_disponiveis if ano == ano_fim]
        mes_fim = st.selectbox("Mês Final", meses_validos_fim, index=len(meses_validos_fim) - 1)

    
    if (ano_inic > ano_fim) or (ano_inic == ano_fim and mes_inic > mes_fim):
        st.error("⚠️ A data inicial não pode ser maior que a data final!")
        return

    
    if st.button("Gerar Gráfico"):
        df = get_top_10_pesquisadores(mes_inic, ano_inic, mes_fim, ano_fim)

        if df.empty:
            st.warning("Nenhum dado encontrado para esse período.")
        else:
            
            fig = px.bar(df, x="nome", y="media_total", 
                         title="Média da Produção Mensal dos Top 10 Pesquisadores",
                         labels={"nome": "Pesquisador", "media_total": "Média de Pesquisas por Dia"},
                         text_auto=True)
            
            st.plotly_chart(fig)


def get_top_10_pesquisadores(mes_inic, ano_inic, mes_fim, ano_fim):
    conn = get_connection()
    cur = conn.cursor()

    query = "SELECT pesquisador_id, nome, media_total FROM topdez(%s, %s, %s, %s);"
    cur.execute(query, (mes_inic, ano_inic, mes_fim, ano_fim))
    
    resultados = cur.fetchall()
    
    cur.close()
    conn.close()

    
    df = pd.DataFrame(resultados, columns=["pesquisador_id", "nome", "media_total"])

    return df

def get_periodos_disponiveis():
    
    conn = get_connection()
    cur = conn.cursor()

    query = "SELECT DISTINCT mes, ano FROM producao_mediamensal_pesquisador ORDER BY ano, mes;"
    cur.execute(query)
    resultados = cur.fetchall()

    cur.close()
    conn.close()

    return resultados  
