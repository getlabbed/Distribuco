Ce template jinja est permet de créé une boisson selon les goûts de l'utilisateur

Args:
    data (list): A list of items to be displayed in the list.

Example:
    {% for item in data %}
    <li>{{ item }}</li>
    {% endfor %}