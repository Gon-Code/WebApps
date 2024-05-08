from flask import Flask, render_template

app = Flask(__name__)

## ESTO ESTA POR REVISAR

#app.secret_key = "s3cr3t_k3y"

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # 16 MB

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ver-productos')
def ver_productos():
    return render_template('ver-productos.html')

if __name__ == '__main__' :
    app.run(debug=True)