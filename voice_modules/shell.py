import os
import threading
import time
import pyaudio
import wave
import speech_recognition as sr
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from pyannote.audio.pipelines import SpeakerDiarization
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# variable definition
chat_history = []
recognition_buffer = []
BUFFER_TIME = 2  
last_speaker = None
recognizer = sr.Recognizer()
buffer_lock = threading.Lock()  # buffer lock
current_user = None  # default user
speaker_model = SpeakerDiarization.from_pretrained("pyannote/speaker-diarization", use_auth_token="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")  # load speaker model

# add message logic in recognize_speech_with_pyaudio
def recognize_speech_with_pyaudio():
    global current_user, last_speaker, recognition_buffer

    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Start voice monitoring...")

        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language='zh-CN')
                print(f"Recognize：{text}")

                # get speaker info and reset user
                user = identify_speaker(audio)
                if user != current_user:
                    current_user = user
                    print(f"Switch to user: {current_user}")

                with buffer_lock:
                    # check user switch
                    if last_speaker != current_user:
                        if last_speaker is not None:
                            submit_buffer(last_speaker)
                        last_speaker = current_user
                        recognition_buffer.clear()

                    recognition_buffer.append(text)

                # use Flask return text
                submit_buffer(current_user)
                
            except sr.UnknownValueError:
                print("Can't recognize speech")
            except sr.RequestError:
                print("Unable to connect to the speech recognition service")


# Identify the speaker
def identify_speaker(audio):
    # Passing audio data to pyannote.audio for speaker recognition
    # pyannote.audio requires an audio file or buffer as input, where the audio is temporarily stored and recognized
    with wave.open("temp_audio.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio.get_wav_data())

    diarization = speaker_model({'uri': 'audio', 'audio': 'temp_audio.wav'})
    
    # Get the most likely speaker label
    speaker = None
    for _, _, label in diarization.itertracks(yield_label=True):
        speaker = label
        break  # Take the first identified speaker
    return f"User {speaker}" if speaker else "User 1"

# Submit buffered content periodically
def periodic_submit_buffer():
    while True:
        time.sleep(BUFFER_TIME)
        with buffer_lock:
            if recognition_buffer:
                submit_buffer(current_user)

# Submit buffer contents
def submit_buffer(user):
    global recognition_buffer
    if recognition_buffer:
        combined_text = ' '.join(recognition_buffer)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # submit to chat_history
        message = {
            'user': user,
            'time': timestamp,
            'content': combined_text,
            'avatar': 'user.png' if user != 'Model' else 'model.png'
        }
        chat_history.append(message)
        print(f"Submit {user}'s chat content: {combined_text}")
        
        # use SocketIO to send frontend update
        socketio.emit('new_message', message)
        #print(f"Send {message} to frontend", message)

        # clean buffer
        recognition_buffer.clear()

'''
# 更新后的 /new_messages 路由
@app.route('/new_messages', methods=['GET'])
def new_messages():
    # 获取最新消息并返回
    if chat_history:
        latest_message = chat_history[-1]
        return jsonify(latest_message)
    return jsonify({'error': 'No new messages'})
'''

'''
# 输入模块：处理文本或语音输入请求
@app.route('/input', methods=['POST'])
def input_message():
    print("============================================input 模块在工作")
    global current_user
    data = request.json
    user = data.get('user', 'User 1')
    content = data.get('content', '')

    if content:  # 处理文本输入
        print("\n\n =================\n Content 处理文本输入 \n\n")
        current_user = user
        with buffer_lock:
            submit_buffer(current_user)  # 提交缓冲区内容
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        chat_history.append({'user': user, 'time': timestamp, 'content': content, 'avatar': 'user.png'})
        return jsonify({'message': 'Message received', 'timestamp': timestamp})
    
    elif data.get('voice') == 'start':  # 启动语音输入线程
        print("\n\n =================\n Content 语音输入线程 \n\n")
        threading.Thread(target=recognize_speech_with_pyaudio, daemon=True).start()
        threading.Thread(target=periodic_submit_buffer, daemon=True).start()
        return jsonify({'message': f'{user} 开始语音输入...'})

    return jsonify({'error': 'Invalid input'})
'''






# Model interaction module: processes model output and submits the previous speaker’s content
@app.route('/model', methods=['POST'])
def model_interaction():
    global last_speaker
    model_output = request.json.get('output', '默认模型响应')

    with buffer_lock:
        if last_speaker != "Model":
            submit_buffer(last_speaker)
            last_speaker = "Model"

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    chat_history.append({
        'user': 'Model',
        'time': timestamp,
        'content': model_output,
        'avatar': 'model.png'
    })
    return jsonify({'message': 'Model output received', 'timestamp': timestamp})



# Display module: Rendering chat history page
@app.route('/display', methods=['GET'])
def display_chat():
    return render_template('chat.html', chat_history=chat_history)


# pre_data for test
def preload_chat_history():
    chat_history.append({'user': 'Model', 'time': '2024-12-05 11:01:00', 'content': 'Hello，I am dialogue system.', 'avatar': 'model.png'})

if __name__ == '__main__':
    preload_chat_history()
    threading.Thread(target=recognize_speech_with_pyaudio, daemon=True).start()
    threading.Thread(target=periodic_submit_buffer, daemon=True).start()
    app.run(debug=True)

