from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if username == "admin" and password == "123456":
        return jsonify({"code": 200, "msg": "登录成功"})
    else:
        return jsonify({"code": 401, "msg": "用户名或密码错误"})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "running", "service": "本地测试接口"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)