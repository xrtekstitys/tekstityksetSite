from werkzeug.utils import secure_filename
class transfer():
    def things(unsecure_filename, method, data: None):
        filename = secure_filename(f"{unsecure_filename}.txt") # Check if file contains unsecure letters
        if method == "r": # User wants to read contains of file
            f = open(filename, method) 
            data = f.read()
            f.close()
            return data
        else: # User wants to write something into file
            f = open(filename, method) 
            f.write(data)
            f.close()
            return "OK"
        