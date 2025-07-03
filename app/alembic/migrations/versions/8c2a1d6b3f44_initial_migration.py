"""create initial tables

Revision ID: 8c2a1d6b3f44
Revises:
Create Date: 2025-07-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c2a1d6b3f44'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'Cars',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('car_name', sa.String(length=40)),
    )

    op.create_table(
        'Tracks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('track_name', sa.String(length=40)),
        sa.Column('turns', sa.Integer()),
        sa.Column('aproximate_flow', sa.Numeric()),
        sa.Column('aproximate_time', sa.Interval()),
    )

    op.create_table(
        'Users',
        sa.Column('user_id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=20)),
        sa.Column('user_language', sa.String(length=5)),
    )


def downgrade():
    op.drop_table('workers')
    op.drop_table('Users')
    op.drop_table('Tracks')
    op.drop_table('Cars')
