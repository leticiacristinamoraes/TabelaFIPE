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
    conn = get_connection()
    cur = conn.cursor()

    # Verifica se o usuário é um pesquisador e está vinculado a alguma loja
    cur.execute("SELECT COUNT(*) FROM stores WHERE pesquisador_id = %s;", (user_id,))
    resultado = cur.fetchone()[0]

    if resultado > 0:
        # Caso tenha lojas associadas, podemos:
        # 1. Transferir para outro pesquisador
        cur.execute("UPDATE stores SET pesquisador_id = (SELECT id FROM users WHERE papel = 'pesquisador' LIMIT 1) WHERE pesquisador_id = %s;", (user_id,))

        # OU

        # 2. Excluir as lojas associadas
        #cur.execute("DELETE FROM stores WHERE pesquisador_id = %s;", (user_id,))

    # Agora pode excluir o usuário sem erro
    cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
