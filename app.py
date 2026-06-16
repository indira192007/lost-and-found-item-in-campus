from flask import Flask, render_template, request, redirect

app = Flask(__name__)

lost_items = []
found_items = []

@app.route('/')
def home():
    search = request.args.get('search', '').lower()

    filtered_lost = [item for item in lost_items
                     if search in item['name'].lower()] if search else lost_items

    filtered_found = [item for item in found_items
                      if search in item['name'].lower()] if search else found_items

    return render_template(
        'index.html',
        lost_items=filtered_lost,
        found_items=filtered_found
    )

@app.route('/add_lost', methods=['POST'])
def add_lost():
    lost_items.append({
        'name': request.form['name'],
        'description': request.form['description'],
        'location': request.form['location'],
        'date': request.form['date']
    })
    return redirect('/')

@app.route('/add_found', methods=['POST'])
def add_found():
    found_items.append({
        'name': request.form['name'],
        'description': request.form['description'],
        'location': request.form['location'],
        'date': request.form['date']
    })
    return redirect('/')

@app.route('/claim/<int:index>')
def claim(index):

    if 0 <= index < len(found_items):

        claimed_item = found_items.pop(index)

        for item in lost_items:
            if item['name'].lower() == claimed_item['name'].lower():
                lost_items.remove(item)
                break

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)