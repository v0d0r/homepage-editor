#!/usr/bin/env python3
from flask import Flask, render_template_string, request, redirect, jsonify
import yaml
import os

app = Flask(__name__)
YAML_FILE = os.getenv('YAML_FILE', '/data/settings.yaml')
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')

def load_yaml():
    if not os.path.exists(YAML_FILE):
        return []
    with open(YAML_FILE, 'r') as f:
        data = yaml.safe_load(f)
        return data if data is not None else []

def save_yaml(data):
    with open(YAML_FILE, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Homepage Editor</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .categories-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-bottom: 20px; }
        .category { border: 1px solid #ddd; padding: 15px; border-radius: 5px; background: white; }
        .category-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .category-name { font-size: 16px; font-weight: bold; color: #333; }
        .service { background: #f9f9f9; padding: 8px; margin: 8px 0; border-left: 3px solid #4CAF50; }
        .service-name { font-weight: bold; color: #2196F3; font-size: 13px; }
        .service div { font-size: 11px; }
        input, button { padding: 6px; margin: 3px; border: 1px solid #ddd; border-radius: 4px; font-size: 11px; }
        button { background: #4CAF50; color: white; cursor: pointer; border: none; }
        button:hover { background: #45a049; }
        .delete-btn { background: #f44336; }
        .delete-btn:hover { background: #da190b; }
        .add-form { background: #e3f2fd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .field { margin: 10px 0; }
        label { display: inline-block; width: 100px; font-weight: bold; }
        @media (max-width: 1400px) { .categories-grid { grid-template-columns: 1fr 1fr; } }
        @media (max-width: 768px) { .categories-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <h1>Homepage Editor</h1>

        <div class="categories-grid">
        {% for category_dict in data %}
            {% for category_name, services in category_dict.items() %}
            <div class="category">
                <div class="category-header">
                    <span class="category-name">{{ category_name }}</span>
                    <button class="delete-btn" onclick="deleteCategory('{{ category_name }}')">Delete Category</button>
                </div>

                {% for service_dict in services %}
                    {% for service_name, service_data in service_dict.items() %}
                    <div class="service">
                        <div class="service-name">{{ service_name }}</div>
                        <div>href: {{ service_data.href }}</div>
                        <div>ping: {{ service_data.ping }}</div>
                        <div>icon: {{ service_data.get('icon', 'N/A') }}</div>
                        {% if service_data.get('description') %}
                        <div>description: {{ service_data.description }}</div>
                        {% endif %}
                        <button onclick="editService('{{ category_name }}', '{{ service_name }}')">Edit</button>
                        <button class="delete-btn" onclick="deleteService('{{ category_name }}', '{{ service_name }}')">Delete</button>
                    </div>
                    {% endfor %}
                {% endfor %}

                <button onclick="showAddService('{{ category_name }}')">+ Add Service</button>
                <div id="add-{{ category_name }}" style="display:none;" class="add-form">
                    <h4>Add Service to {{ category_name }}</h4>
                    <form action="/add_service/{{ category_name }}" method="post">
                        <div class="field"><label>Name:</label><input name="name" required></div>
                        <div class="field"><label>href:</label><input name="href" required></div>
                        <div class="field"><label>ping:</label><input name="ping" required></div>
                        <div class="field"><label>icon:</label><input name="icon"></div>
                        <div class="field"><label>description:</label><input name="description"></div>
                        <button type="submit">Add</button>
                        <button type="button" onclick="hideAddService('{{ category_name }}')">Cancel</button>
                    </form>
                </div>
            </div>
            {% endfor %}
        {% endfor %}
        </div>

        <div class="add-form">
            <h3>Add New Category</h3>
            <form action="/add_category" method="post">
                <input name="category_name" placeholder="Category Name" required>
                <button type="submit">Add Category</button>
            </form>
        </div>
    </div>

    <script>
        function showAddService(cat) { document.getElementById('add-' + cat).style.display = 'block'; }
        function hideAddService(cat) { document.getElementById('add-' + cat).style.display = 'none'; }
        function deleteCategory(cat) {
            if(confirm('Delete category "' + cat + '"?')) {
                fetch('/delete_category/' + encodeURIComponent(cat), {method: 'POST'})
                    .then(() => location.reload());
            }
        }
        function deleteService(cat, svc) {
            if(confirm('Delete service "' + svc + '"?')) {
                fetch('/delete_service/' + encodeURIComponent(cat) + '/' + encodeURIComponent(svc), {method: 'POST'})
                    .then(() => location.reload());
            }
        }
        function editService(cat, svc) {
            const newHref = prompt('New href:');
            const newPing = prompt('New ping:');
            const newIcon = prompt('New icon:');
            const newDesc = prompt('New description (optional):');
            if(newHref && newPing) {
                fetch('/edit_service/' + encodeURIComponent(cat) + '/' + encodeURIComponent(svc), {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({href: newHref, ping: newPing, icon: newIcon, description: newDesc})
                }).then(() => location.reload());
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    data = load_yaml()
    return render_template_string(HTML, data=data)

@app.route('/add_category', methods=['POST'])
def add_category():
    data = load_yaml()
    category_name = request.form['category_name']
    data.append({category_name: []})
    save_yaml(data)
    return redirect('/')

@app.route('/add_service/<category>', methods=['POST'])
def add_service(category):
    data = load_yaml()
    for cat_dict in data:
        if category in cat_dict:
            service = {
                request.form['name']: {
                    'href': request.form['href'],
                    'ping': request.form['ping'],
                }
            }
            if request.form.get('icon'):
                service[request.form['name']]['icon'] = request.form['icon']
            if request.form.get('description'):
                service[request.form['name']]['description'] = request.form['description']
            cat_dict[category].append(service)
            break
    save_yaml(data)
    return redirect('/')

@app.route('/delete_category/<category>', methods=['POST'])
def delete_category(category):
    data = load_yaml()
    data[:] = [cat_dict for cat_dict in data if category not in cat_dict]
    save_yaml(data)
    return '', 204

@app.route('/delete_service/<category>/<service>', methods=['POST'])
def delete_service(category, service):
    data = load_yaml()
    for cat_dict in data:
        if category in cat_dict:
            cat_dict[category][:] = [s for s in cat_dict[category] if service not in s]
            break
    save_yaml(data)
    return '', 204

@app.route('/edit_service/<category>/<service>', methods=['POST'])
def edit_service(category, service):
    data = load_yaml()
    updates = request.json
    for cat_dict in data:
        if category in cat_dict:
            for svc_dict in cat_dict[category]:
                if service in svc_dict:
                    svc_dict[service]['href'] = updates['href']
                    svc_dict[service]['ping'] = updates['ping']
                    if updates.get('icon'):
                        svc_dict[service]['icon'] = updates['icon']
                    if updates.get('description'):
                        svc_dict[service]['description'] = updates['description']
                    break
            break
    save_yaml(data)
    return '', 204

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=False)
