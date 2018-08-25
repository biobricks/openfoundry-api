from sqlalchemy.orm import sessionmaker, relationship

import schema
import sqlalchemy

CONNECTION_STRING = 'sqlite:///database.db'

engine = sqlalchemy.create_engine(CONNECTION_STRING, echo=False)
schema.Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

