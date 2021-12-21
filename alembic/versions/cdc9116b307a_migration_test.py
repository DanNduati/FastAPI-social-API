"""migration test

Revision ID: cdc9116b307a
Revises: 
Create Date: 2021-12-21 14:17:51.627237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdc9116b307a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'm_test',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )


def downgrade():
    op.drop_table('m_test')
