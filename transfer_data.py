from werkzeug.utils import secure_filename


class transfer():
    def things(unsecure_filename, method, data: None):
        # Check if file contains unsecure letters
        filename = secure_filename(f"{unsecure_filename}.txt")
        if method == "r":  # User wants to read contains of file
            with open(filename, method) as f:
                data = f.read()
            return data
        else:  # User wants to write something into file
            with open(filename, method) as f:
                f.write(data)
            return "OK"
