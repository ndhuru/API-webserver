'''

Made by Scrum Team Doornail

             _ _ 
            (_) |
 _ __   __ _ _| |
| '_ \ / _` | | |
| | | | (_| | | |
|_| |_|\__,_|_|_|


Pizza is on us, enjoy it Mr. Stern!
                                   ,(  `-.
                                 ,': `.   `.
                               ,` *   `-.   \
                             ,'  ` :+  = `.  `.
                           ,~  (o):  .,   `.  `.
                         ,'  ; :   ,(__) x;`.  ;
                       ,'  :'  itz  ;  ; ; _,-'
                     .'O ; = _' C ; ;'_,_ ;
                   ,;  _;   ` : ;'_,-'   i'
                 ,` `;(_)  0 ; ','       :
               .';6     ; ' ,-'~
             ,' Q  ,& ;',-.'
           ,( :` ; _,-'~  ;
         ,~.`c _','
       .';^_,-' ~
     ,'_;-''
    ,,~
    i'
    :


'''

from flask import Flask, request, jsonify
from adafruit_motorkit import MotorKit
import time

kit = MotorKit(0x40)
#flask app
app = Flask(__name__)

#route for index
@app.route('/')
def index():
  #html
    return '''
    <html>
    <head>
        <style>
        .stop-button {
            background-color: red;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 50%;
            font-size: 20px;
        }
        
        .play-button {
            background-color: green;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 50%;
            font-size: 20px;
        }
        </style>
    </head>
    <body>
        <h1>Robot Control</h1>
        <div style="display: flex; justify-content: center;">
            <button onclick="sendCommand('forward')" style="padding: 10px 20px;">&#8593;</button>
        </div>
        <div style="display: flex; justify-content: center;">
            <button onclick="sendCommand('left')" style="padding: 10px 20px;">&#8592;</button>
            <button onclick="sendCommand('stop')" class="stop-button">Stop</button>
            <button onclick="sendCommand('play')" class="play-button">&#9654;</button>
            <button onclick="sendCommand('right')" style="padding: 10px 20px;">&#8594;</button>
        </div>
        <div style="display: flex; justify-content: center;">
            <button onclick="sendCommand('backward')" style="padding: 10px 20px;">&#8595;</button>
        </div>
        <script>
        function sendCommand(command) {
            fetch('/control', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 'command': command })
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
        }
        </script>
    </body>
    </html>
    '''

#route for control functions
@app.route('/control', methods=['POST'])
def control():
    #extract command from POST request
    command = request.json['command']
    #implement control logic based on received command
    if command == 'forward':
        forward(2.6)
      #forward statement, i set it to 2.6 as an example
    elif command == 'backward':
        backward(2.6)
      #backward statement, i set it to 2.6 as an example
    elif command == 'left':
        left(2.6)
      #left statement, i set it to 2.6 as an example
    elif command == 'right':
        right(2.6)
      #right statement, i set it to 2.6 as an example
    elif command == 'stop':
        stop()
      #stop statement
    elif command == 'play':
        play()
      #play statement, I just had it run something
    else:
        return jsonify({'status': 'error', 'message': 'Invalid command'})
    return jsonify({'status': 'success', 'message': 'Command executed'})

#define functions for movement commands
def forward(amount_of_time_to_run):
    #adjust motor throttle for forward movement
    #notice how they amde the motors backwards
    #-0.5 and 0.64 to move forward
    kit.motor1.throttle = -0.5
    kit.motor2.throttle = 0.64
    time.sleep(amount_of_time_to_run)
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

def backward(amount_of_time_to_run):
  #same confusion
    kit.motor1.throttle = 0.7
    kit.motor2.throttle = -0.7
    time.sleep(amount_of_time_to_run)
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

def left(amount_of_time_to_run):
  #left, 
  #now need to negate both motor throttles for some reason instead of negating just one...
    kit.motor1.throttle = -0.64
    kit.motor2.throttle = -0.64
    time.sleep(amount_of_time_to_run)
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

def right(amount_of_time_to_run):
  #right, now they're both positive?
    kit.motor1.throttle = 0.64
    kit.motor2.throttle = 0.64
    time.sleep(amount_of_time_to_run)
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

def stop():
  #straightforward stop function
    kit.motor1.throttle = 0.0
    kit.motor2.throttle = 0.0

def play():
  #set play to move
    kit.motor1.throttle = 0.5
    kit.motor2.throttle = 0.5

#define similar functions for backward, left, right, stop, and play commands
#(backward, left, right, stop, play functions follow a similar structure)

#run the Flask app
if __name__ == '__main__':
    #start the app on a specific host and port, I don't know how the port part works though
    #will research ports more
    app.run(host='0.0.0.0', port=4444)
