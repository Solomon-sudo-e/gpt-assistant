from flask import Flask, render_template, request, jsonify, send_file
import openai
import io
import logging
from chatbot import get_answer
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
    
@app.route('/audio', methods=['GET'])
def get_audio():
    question = request.args.get('question')
    if not question:
       return "Question parameter is missing", 400
    try:
        answer = get_answer(question)
        response = openai.audio.speech.create(
            model="tts-1",
            voice="fable",
            input=answer
        )
        audio_data = response.content
        audio_io = io.BytesIO(audio_data)
        app.logger.debug(f'Response object type: {type(response)}')
        return send_file(audio_io, mimetype='audio/mpeg')
    except Exception as e:
       app.logger.error('Failed to generate speech', exc_info=True)
       return jsonify({'error': str(e)}), 500

logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

if __name__ == '__main__':
    app.run(debug=True)
