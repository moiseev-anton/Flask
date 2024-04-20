from databases import Database
from sqlalchemy import MetaData, create_engine
import sqlalchemy as sa

DATABASE_URL = "sqlite:///mydatabase.db"

database = Database(DATABASE_URL)
metadata = MetaData()

users = sa.Table(
    'users',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('firstname', sa.String(50), nullable=False),
    sa.Column('lastname', sa.String(50)),
    sa.Column('email', sa.String(128), unique=True, nullable=False),
    sa.Column('password', sa.String(128), nullable=False),
)

products = sa.Table(
    'products',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('title', sa.String(100), nullable=False),
    sa.Column('description', sa.Text),
    sa.Column('price', sa.Numeric(10, 2), nullable=False),
)

orders = sa.Table(
    'orders',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id'), nullable=False),
    sa.Column('date', sa.DateTime, default=sa.sql.func.now()),
    sa.Column('status', sa.String(20)),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)
