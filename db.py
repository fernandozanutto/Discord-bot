import sqlite3

conn = sqlite3.connect('discord.db')

cursor = conn.cursor()

def create_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios_jogos (
     usuario INT NOT NULL,
    jogo INT NOT NULL,
    data_inicio DATETIME NOT NULL,
    data_fim DATETIME NOT NULL)
    """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS jogos (
    id_jogo int,
    nome text,
    UNIQUE(id_jogo)
    )
    """)

    conn.commit()


def insert(id_usuario, id_jogo, data_inicio, data_fim, nome_jogo):
    cursor.execute("INSERT INTO usuarios_jogos (usuario, jogo, data_inicio, data_fim) VALUES (?,?,?,?)", (id_usuario, id_jogo, data_inicio, data_fim))

    cursor.execute("INSERT OR IGNORE INTO jogos (id_jogo, nome) VALUES (?, ?)", (id_jogo, nome_jogo))

    conn.commit()

    cursor.execute("SELECT * FROM usuarios_jogos")
    print(cursor.fetchall())
    print()
    cursor.execute("SELECT * FROM jogos")
    print(cursor.fetchall())
