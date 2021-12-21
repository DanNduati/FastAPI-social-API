"""comparision test

Revision ID: 4b08a4caf9e0
Revises: cdc9116b307a
Create Date: 2021-12-21 15:00:13.417059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b08a4caf9e0'
down_revision = 'cdc9116b307a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mtest', sa.Column('password', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mtest', 'password')
    # ### end Alembic commands ###