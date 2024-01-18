from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    commit_message = ""
    if request.method == 'POST':
        description = request.form['description']
        commit_message = generate_commit_message(description)
    return render_template('index.html', commit_message=commit_message)


def generate_commit_message(description):
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt="Shorten for a Git commit message without losing context or information and make it be under 10 words: {}".format(
                description),
            max_tokens=60
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
