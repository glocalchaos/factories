from app import app
from app import db
from . import excel_parser

@app.route('/')
@app.route('/index')
def index():
    return "Hello world"

@app.route('/uploadTransport', methods=['GET', 'POST'])
def upload_file():
    parser = excel_parser.Parser()
    transport_set = parser.parseTransport()
    print(transport_set)
    session = db.session
    session.add_all(transport_set)
    session.commit()
    session.close()