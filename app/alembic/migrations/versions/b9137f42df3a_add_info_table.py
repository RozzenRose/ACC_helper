"""add Info table

Revision ID: b9137f42df3a
Revises: 8c2a1d6b3f44
Create Date: 2025-07-01 12:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9137f42df3a'
down_revision = '8c2a1d6b3f44'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'Info',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('car_id', sa.Integer(), sa.ForeignKey('Cars.id')),
        sa.Column('track_id', sa.Integer(), sa.ForeignKey('Tracks.id')),
        sa.Column('track_guide', sa.String(length=200)),
        sa.Column('setups', sa.String(length=120)),
    )


def downgrade():
    op.drop_table('Info')
