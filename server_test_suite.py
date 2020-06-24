'''
### GET USER TABLE ###
@app.route('/')
def init():
    con = create_connection()
    request = "SELECT * FROM users"
    resp = execute_read_query(con, request)
    to_send = app.response_class(response=json.dumps(resp), status=200, mimetype='application/json')
    return to_send

@app.route('/test/<col_type>')
def test(col_type):
    con = create_connection()
    query = f"SELECT {col_type} from users"
    resp = execute_read_query(con, query)
    to_send = app.response_class(response=json.dumps(resp), status=200, mimetype='application/json')
    return to_send
'''