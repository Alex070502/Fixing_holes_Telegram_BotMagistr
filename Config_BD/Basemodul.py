from sqlalchemy import create_engine, Table, MetaData, Column, Integer, Text, Float, ForeignKey, LargeBinary, VARCHAR, Date
import psycopg2
conn = psycopg2.connect(dbname='pathole', user='postgres',
                        password='2002', host='localhost')
engine = create_engine("postgresql+psycopg2://postgres:2002@localhost/pathole")
engine.connect()

metadata1 = MetaData()
metadata2 = MetaData()
metadata3 = MetaData()

wa = Table(
    'well_applications',
    metadata1,
    Column('id', Integer(), unique=True, primary_key=True),
    Column('address', Text()),
    Column('longtitude', Float()),
    Column('latitude', Float()),
    Column('user_id', Integer(), ForeignKey('users.tid'), nullable=False),
    Column('photo', LargeBinary()),
    Column('detected_photo', LargeBinary()),
    Column('date', Date()),
    Column('status', VARCHAR(20))
)

pa = Table(
    'pathole_applications',
    metadata2,
    Column('id', Integer(), unique=True, primary_key=True),
    Column('address', Text()),
    Column('longtitude', Float()),
    Column('latitude', Float()),
    Column('user_id', Integer(), ForeignKey('users.tid'), nullable=False),
    Column('photo', LargeBinary()),
    Column('detected_photo', LargeBinary()),
    Column('date', Date()),
    Column('status', VARCHAR(20))
)

users = Table(
    'users',
    metadata3,
    Column('id', Integer(), unique=True, primary_key=True),
    Column('username', Text()),
    Column('tid', Integer(), unique=True),
    Column('number', VARCHAR(20), default=None),
    Column('role', VARCHAR(), default='user')
)