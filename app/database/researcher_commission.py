import sys
import os
from datetime import date
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database.config import get_connection

def create_researcher_commission_table():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS researcher_commission (
            id SERIAL PRIMARY KEY,
            pesquisador_id INTEGER NOT NULL,
            mes integer NOT NULL,
            ano INTEGER NOT NULL,
            comissao NUMERIC(10,2) NOT NULL,
            FOREIGN KEY (pesquisador_id) REFERENCES users(id) ON DELETE SET NULL
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

    def update_commission():
        today = date.today()
        month, year = [today.month-1, today.year] if today.month > 1 else [12, today.year-1]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"""SELECT * FROM public.researcher_commission
                    WHERE EXISTS(SELECT 1 FROM researcher_commission where mes={month} and ano={year});""")
        confirmacao = cur.fetchall()
        if len(confirmacao) == 0:
            cur.execute("""SELECT pesquisador_id,
            COUNT(*) AS comissoes
            FROM  (SELECT * FROM (SELECT
                prices.loja_id,
                prices.data,
                stores.pesquisador_id
            FROM prices
                INNER JOIN stores ON prices.loja_id = stores.id) T 
                WHERE DATE_PART('MONTH',data)={} AND DATE_PART('YEAR',data)={}) R
            GROUP BY pesquisador_id;""".format(month,year))
            comissao = cur.fetchall()
            for i in comissao:
                cur.execute("""
                    INSERT INTO researcher_commission (pesquisador_id, mes, ano, comissao) 
                    VALUES (%s, %s, %s, %s) RETURNING id;
                """, (i[0], mes, ano, i[1]))
            cur.close()
            conn.close()
            return print("Comissão calculada com sucesso.")
        else:
            return print("Comissão desta data já calculada.")

    def insert_commission(mes,ano):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""SELECT * FROM public.researcher_commission
                    WHERE EXISTS(SELECT 1 FROM researcher_commission where mes={} and ano={});""".format(mes,ano))
        confirmacao = cur.fetchall()
        if len(confirmacao) != 0:
            cur.execute("""SELECT pesquisador_id,
            COUNT(*) AS comissoes
            FROM  (SELECT * FROM (SELECT
                prices.loja_id,
                prices.data,
                stores.pesquisador_id
            FROM prices
                INNER JOIN stores ON prices.loja_id = stores.id) T 
                WHERE DATE_PART('MONTH',data)={} AND DATE_PART('YEAR',data)={}) R
            GROUP BY pesquisador_id;""".format(mes,ano))
            comissao = cur.fetchall()
            for i in comissao:
                cur.execute("""
                    INSERT INTO researcher_commission (pesquisador_id, mes, ano, comissao) 
                    VALUES (%s, %s, %s, %s) RETURNING id;
                """, (i[0], mes, ano, i[1]))
            cur.close()
            conn.close()
            return print("Comissão calculada com sucesso.")
        else:
            return print("Comissão desta data já calculada.")
        
    def commission_consult(mes,ano):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""SELECT * FROM public.researcher_commission
                    WHERE mes={} AND ano={};""".format(mes,ano))
        exibicao = cur.fetchall()
        df = pd.DataFrame(exibicao, columns=['Data', 'Quantidade'])

        cur.close()
        conn.close()
    