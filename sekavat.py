@id_route("/signup-1/")
def signup_id1():
	return render_template("signup-1.html")
@id_route("/signup-1/", methods=["POST"])
def signup_send1():
	username = request.form.get("username")
	password = request.form.get("password")
	matrix.create_user(request)
	return f"User {username} created with password {password}, chat.xrtekstitys.fi"