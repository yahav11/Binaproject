from flask import Flask, render_template, request, jsonify, redirect

app = Flask(__name__)

api_name = "Employee API"

employees = [
    {'id': '1234', 'name': 'Dan'},
    {'id': '12345', 'name': 'Maya'},
    {'id': '123456', 'name': 'Yuval'}
]


@app.route('/')
def index():
    return render_template('index.html', api_name=api_name, employees=employees)


@app.route('/edit', methods=['POST'])
def edit():
    id = request.form.get('id')
    new_name = request.form.get('new_name')

    if not new_name:
        return "New name is required", 400

    if any(e['name'] == new_name for e in employees if e['id'] != id):
        return "Employee with the same name already exists", 409

    employee = next((e for e in employees if e['id'] == id), None)
    if not employee:
        return "Employee not found", 404

    employee['name'] = new_name
    return redirect("/", code=302)


@app.route('/delete', methods=['POST'])
def delete():
    id = request.form.get('id')

    employee = next((e for e in employees if e['id'] == id), None)
    if not employee:
        return "Employee not found", 404

    employees.remove(employee)
    return redirect("/", code=302)


@app.route('/add', methods=['POST'])
def add():
    id = request.form.get('id')
    name = request.form.get('name')

    if not id or not name:
        return "ID and name are required", 400

    if any(e['id'] == id for e in employees):
        return "Employee with the same ID already exists", 409

    employees.append({'id': id, 'name': name})
    return redirect("/", code=302)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return "Query parameter 'query' is required", 400

    result = [e for e in employees if query.lower() in e['name'].lower() or query == e['id']]
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

