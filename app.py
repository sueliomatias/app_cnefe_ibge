from flask import Flask, request
import flask
import sqlite3

app = Flask(__name__)

def calculate_pagination_info(result, page, per_page, total_records, offset):

    # determinando a quantidade de valores por página
    max_per_page = total_records if total_records < per_page else per_page

    # calcular o número total de páginas
    total_pages = (total_records + per_page - 1) // per_page

    # determinar números de páginas anteriores e posteriores
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    response_data = {
        "result": result,
        "info": {
            "offset": offset,
            "page": page,
            "per_page": max_per_page,
            "total_pages": total_pages,
            "total_records": total_records,
            "prev_page": prev_page,
            "next_page": next_page,
        }
    }
    
    return flask.jsonify(response_data)

def get_total_records():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM enderecos")
    total_records = cursor.fetchone()[0]

    conn.close()

    return total_records

@app.route('/api', methods=['GET'])
def api():
    # conecta ao banco de dados SQLite
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # obtém os parâmetros da paginação
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # calcula o offset com base na página e quantidade por página
    offset = (page - 1) * per_page

    # calcula total de registros
    total_records = get_total_records()

    # obtém o CEP da query string e adiciona a cláusula WHERE se presente
    cep = request.args.get('cep', False)
    cep = f" WHERE CEP = {cep}" if cep else ""

    # executa uma consulta no banco de dados com paginação
    cursor.execute(f"SELECT * FROM enderecos {cep} LIMIT {per_page} OFFSET {offset}")

    # obtém os nomes das colunas da tabela
    col_name = [i[0] for i in cursor.description]

    # obtém os resultados da consulta
    results = cursor.fetchall()

    # unir col_name com results
    results = [dict(zip(col_name, row)) for row in results]

    # calcula as informações de paginação e retorna os resultados em formato JSON
    json_results = calculate_pagination_info(results, page, per_page, total_records, offset)

    # fecha a conexão com o banco de dados
    conn.close()

    return json_results

if __name__ == '__main__':
    app.run()