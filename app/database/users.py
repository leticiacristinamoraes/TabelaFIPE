import sys
import os
import psycopg2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.config import get_connection

def create_users_table():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            papel VARCHAR(50) NOT NULL
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def create_user(nome, email, papel):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (nome, email, papel) VALUES (%s, %s, %s) RETURNING id;
    """, (nome, email, papel))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return user_id

def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def update_user(user_id, nome, email, papel):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users SET nome = %s, email = %s, papel = %s WHERE id = %s;
    """, (nome, email, papel, user_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_user(user_id):
    """Exclui um usuário, atribuindo as lojas a outro pesquisador, se necessário."""
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Verifica se o usuário a ser excluído é um pesquisador
        cur.execute("SELECT papel FROM users WHERE id = %s;", (user_id,))
        user_role = cur.fetchone()

        if user_role and user_role[0] == 'pesquisador':
            # Busca um novo pesquisador para atribuir às lojas
            cur.execute("SELECT id FROM users WHERE papel = 'pesquisador' AND id <> %s LIMIT 1;", (user_id,))
            new_pesquisador = cur.fetchone()

            if new_pesquisador:
                new_pesquisador_id = new_pesquisador[0]
                # Atualiza as lojas para o novo pesquisador
                cur.execute("UPDATE stores SET pesquisador_id = %s WHERE pesquisador_id = %s;", (new_pesquisador_id, user_id))
                print(f"🔄 Lojas transferidas para o pesquisador {new_pesquisador_id}.")
            else:
                print("⚠ Nenhum outro pesquisador disponível. Não é possível excluir este usuário.")
                return  # Sai da função sem excluir o usuário

        # Exclui o usuário
        cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        conn.commit()
        print(f"✅ Usuário {user_id} excluído com sucesso.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Erro ao excluir usuário: {e}")

    finally:
        cur.close()
        conn.close()
    # Agora pode excluir o usuário sem erro
    cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

def get_researcher_info(email):
    """Retorna o nome e email do pesquisador logado."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT nome, email
        FROM users
        WHERE email = %s
        """,
        (email,),
    )
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        return result
    else:
        return None, None
    
