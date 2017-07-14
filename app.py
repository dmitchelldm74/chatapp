from flask import Flask, request, render_template, make_response
from database import AUTH, KEY_AUTH, SEND_MESSAGE, GET_MESSAGES, LOG

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
    session_key = request.cookies.get('AUTH',"None")
    if session_key == "None":
        response = make_response(render_template('index.html'))
        if request.method == "POST":
            method = request.form.get("id","POST")
            auth = AUTH(response)
            if method == "LOGIN":
                if "username" in request.form and "password" in request.form:
                    auth.login(request.form.get("username"), request.form.get("password"))
            elif method == "CREATE":
                if "username" in request.form and "password" in request.form:
                    username, password = request.form.get("username"), request.form.get("password")
                    if auth.new(username, password) == True:
                        auth.login(username, password)
                    else:
                        return "Failed to create an account..."
            auth.close()
            del auth      
    else:
        to = request.args.get("to",None)
        auth = KEY_AUTH(session_key)
        response = make_response(render_template('messages.html', to=to, messages=GET_MESSAGES(auth)))
        auth.response = response
        if request.method == "POST":
            method = request.form.get("id","POST")
            if method == "MESSAGE":
                if "to" in request.form and "content" in request.form:
                    SEND_MESSAGE(auth, request.form.get("to",""), request.form.get("content",""))
            elif method == "LOGOUT":
                auth.logout()
            elif method == "LOG":
                return LOG(auth)
        auth.login()
        auth.close()
    return response
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=9323)
