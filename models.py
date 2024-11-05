import settings
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, DateTime, String, create_engine
from datetime import datetime

Base = declarative_base()
     
class Ad(Base):
    __tablename__ = 'ad'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    user_id = Column(Integer, nullable=False)

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id
        }


    def ad_get_by_id(session, ad_id):
        q = session.query(Ad).filter(Ad.id == ad_id)
        return q.one_or_none()
    
    def ad_insert(session, title, description, user_id):
        ad = Ad(title=title, description=description, user_id=user_id)
        session.add(ad)
        session.flush()
        session.commit()
        return ad
    
    def ad_delete(session, ad_id):
        ad = session.query(Ad).filter(Ad.id == ad_id).one_or_none()
        session.delete(ad)
        session.commit()

class BdInstruments():
    engine = create_engine(settings.DSN, pool_size=40, max_overflow=0)
    def get_session():
        Session = sessionmaker(bind=BdInstruments.engine)
        session = Session()
        return session
    
    def create_tables():
        Base.metadata.create_all(BdInstruments.engine)

    def drop_tables():
        Base.metadata.drop_all(BdInstruments.engine)