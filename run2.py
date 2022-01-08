from flask import Flask, Response, g
import time

app = Flask(__name__)

@app.before_request
def before_request_func():
    g.timings = {}

from functools import wraps
def time_this(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        g.timings[func.__name__] = end - start
        return r
    return wrapper


@time_this
def call_func():
    time.sleep(1)
    

@time_this
def another_func():
    time.sleep(2)

@app.after_request
def after_request_func(response):
    # just append timings to the output response:
    response.data += ('\n' + str(g.timings)).encode('ascii')
    return response

@app.route('/',methods=['GET','POST'])
@time_this
def hello2():
    call_func()
    another_func()
    return Response('Hello World', mimetype='text/plain')

if __name__ == "__main__":
    app.run(debug=True)