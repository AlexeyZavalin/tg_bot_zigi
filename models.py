from sqlalchemy import create_engine, Column, Integer, String, Boolean, MetaData
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite3:', echo=True)
meta = MetaData()


class ServiceState(Base):
    """
    модель сервиса
    """

    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    enabled = Column(Boolean, default=True)

    def __repr__(self):
        enabled = 'включен' if self.enabled else 'отключен'
        return f'{self.name} - {enabled}'
