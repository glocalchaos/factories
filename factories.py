from app import app
from app.utils.db_utils import populate_db

populate_db()
#from app import models

# parser = excel_parser.Parser()
# transport_set = parser.parseTransport()
# session = db.session
# session.add_all(transport_set)
# session.new
# session.commit()