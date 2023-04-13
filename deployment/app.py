from flask import Flask, request, render_template, send_from_directory
import os
import subprocess

app = Flask(__name__)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('last_frame/', filename, as_attachment=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file and other required parts
        if 'image' not in request.files:
            return 'No image file selected'
        if 'email' not in request.form:
            return 'No email specified'
        if 'conv' not in request.form:
            return 'No confidence threshold specified'
        # if 'stream' not in request.form:
        #     return 'No stream specified'
        
        email = request.form['email']
        conv = request.form['conv']
        stream = request.form['stream']

        
        
        # Save the file to the uploads folder
        if len(stream) == 0:
            file = request.files['image']
            filename = file.filename
            file.save('uploads/' + filename)
            filepath = os.path.join(os.getcwd(), 'uploads', filename)

        if len(stream):
            source = stream
        else:
            source = filepath
        
        # Call the Python script and pass the file path as a command line argument
        cmd = ['python', 'run_model.py', "--source", source,'--weights', '../models/trained_model.pt', "--conf", conv, '--email_id', email]
        # cmd = 'ls'
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
        except Exception as e:
            raise
            print(f"Error running script.py: {e}")
            result = "Error running script.py"
        
        # Create a list of files in the uploads directory
        files = os.listdir('last_frame/')
        
        return render_template('index.html', result=result, files=files)
        
    # If the request is a GET request, display the form
    files = os.listdir('last_frame/')
    return render_template('index.html', files=files)


if __name__ == '__main__':
    app.run(debug=True)
