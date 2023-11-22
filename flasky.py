from flask import Flask, render_template, request, jsonify
# from chatbot import question, answer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chatty():
    if request.method == 'GET':
     return render_template('index.html')
    elif request.method == 'POST':
       question = request.form.get('question')
       answer = get_answer(question)
       return jsonify({'answer': answer})
    
def get_answer(question):
    from chatbot import get_answer
    return get_answer(question)

if __name__ == '__main__':
    app.run(debug=True)
