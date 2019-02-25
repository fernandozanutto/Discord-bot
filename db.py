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
    #print(cursor.fetchall())

    cursor.execute("SELECT * FROM jogos")
    #print(cursor.fetchall())

def leaderboard_usuarios(usuarios: list = [], data_limite: list = []):

    sql = """
    SELECT usuario, SUM((JULIANDAY(data_fim) - JULIANDAY(data_inicio))) * 24 * 60 AS tempo
    FROM usuarios_jogos
    LEFT JOIN jogos ON jogos.id_jogo = usuarios_jogos.jogo
    WHERE usuario IN ({})
    GROUP BY usuario
    ORDER BY TEMPO DESC
    """.format(("?, " * len(usuarios))[:-2])
    #print(sql)
    cursor.execute(sql, usuarios)

    resultado = cursor.fetchall()

    #print(resultado)

    return resultado

def leaderboard_jogos(data_limite: list=['0000-00-00', '2999-12-31']):

    sql = """
    SELECT nome, SUM((JULIANDAY(data_fim) - JULIANDAY(data_inicio))) * 24 * 60 AS tempo
    FROM usuarios_jogos
    LEFT JOIN jogos ON jogos.id_jogo = usuarios_jogos.jogo
    WHERE data_inicio >= "{}" AND data_fim <= "{}"
    GROUP BY nome
    ORDER BY tempo DESC
    """.format(*data_limite)
    #print(sql)
    cursor.execute(sql)

    resultado = cursor.fetchall()

    print(resultado)

    return resultado
