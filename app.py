from flask import Flask
import flask
import sqlite3

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    # conecta ao banco de dados SQLite
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # executa uma consulta no banco de dados
    cursor.execute("SELECT * FROM enderecos limit 100")

    # obtém os nomes das colunas da tabela
    col_name = [i[0] for i in cursor.description]

    # obtém os resultados da consulta
    results = cursor.fetchall()
    
    # unir col_name com results
    results = [dict(zip(col_name, row)) for row in results]

    # transformar em JSON
    json_results = flask.jsonify(results)

    # fecha a conexão com o banco de dados
    conn.close()

    return json_results

if __name__ == '__main__':
    app.run()