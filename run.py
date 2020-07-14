from flask import Flask, jsonify
from flask import request
from flask_cors import *

from report_of_epidemic_Linux import *

# 实例化，可视为固定格式
app = Flask(__name__)
CORS(app, supports_credentials=True)


# route()方法用于设定路由；类似spring路由配置
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/doLogin', methods=["POST"])
def doLogin():
    username = request.form.get("username")
    password = request.form.get("password")

    print(username, "请求登录")
    return jsonify(run(username, password))


if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host=127.0.0.1, port=5000, debug=false
    app.run(port='5000', host='0.0.0.0')
