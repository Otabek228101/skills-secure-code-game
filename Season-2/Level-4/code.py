import os
from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)
template_dir = os.path.abspath('Season-2/Level-4/templates')
app.template_folder = template_dir

planet_data = {
    "Mercury": "The smallest and fastest planet in the Solar System.",
    "Venus": "The second planet from the Sun and the hottest planet.",
    "Earth": "Our home planet and the only known celestial body to support life.",
    "Mars": "The fourth planet from the Sun and often called the 'Red Planet'.",
    "Jupiter": "The largest planet in the Solar System and known for its great red spot.",
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        planet = request.form.get('planet')
        sanitized_planet = escape(planet if planet else '')

        if sanitized_planet:
            if 'script' in sanitized_planet.lower():
                return '<h2>Blocked</h2></p>'

            return render_template('details.html',
                                   planet=sanitized_planet,
                                   info=get_planet_info(planet))
        else:
            return '<h2>Please enter a planet name.</h2>'

    return render_template('index.html')

def get_planet_info(planet):
    return planet_data.get(planet, 'Unknown planet.')

if __name__ == '__main__':
    app.run()