"""OAuth2

Revision ID: 08c9fb0f646e
Revises: 
Create Date: 2024-12-08 00:20:41.454067

"""
from typing import Sequence, Union

from alembic import op
import fastapi_users_db_sqlalchemy
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08c9fb0f646e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('houses',
    sa.Column('style', sa.String(), nullable=False),
    sa.Column('color', sa.String(), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('add', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('tg_id', sa.Integer(), nullable=True),
    sa.Column('number', sa.String(length=18), nullable=True),
    sa.Column('id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.Date(), server_default='2024-12-08', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('oauth_account',
    sa.Column('id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.Column('user_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.Column('oauth_name', sa.String(length=100), nullable=False),
    sa.Column('access_token', sa.String(length=1024), nullable=False),
    sa.Column('expires_at', sa.Integer(), nullable=True),
    sa.Column('refresh_token', sa.String(length=1024), nullable=True),
    sa.Column('account_id', sa.String(length=320), nullable=False),
    sa.Column('account_email', sa.String(length=320), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_oauth_account_account_id'), 'oauth_account', ['account_id'], unique=False)
    op.create_index(op.f('ix_oauth_account_oauth_name'), 'oauth_account', ['oauth_name'], unique=False)
    op.create_table('reservations',
    sa.Column('start', sa.Date(), nullable=False),
    sa.Column('end', sa.Date(), nullable=False),
    sa.Column('full_price', sa.Integer(), nullable=False),
    sa.Column('was_paid', sa.Boolean(), nullable=False),
    sa.Column('add', sa.Boolean(), nullable=False),
    sa.Column('house_id', sa.Integer(), nullable=False),
    sa.Column('user_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['house_id'], ['houses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('reservations')
    op.drop_index(op.f('ix_oauth_account_oauth_name'), table_name='oauth_account')
    op.drop_index(op.f('ix_oauth_account_account_id'), table_name='oauth_account')
    op.drop_table('oauth_account')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('houses')
