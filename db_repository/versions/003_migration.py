from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
answer = Table('answer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=30000)),
    Column('timestamp', DateTime),
    Column('up_vote', Integer),
    Column('down_vote', Integer),
    Column('user_id', Integer),
    Column('post_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['answer'].columns['post_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['answer'].columns['post_id'].drop()
