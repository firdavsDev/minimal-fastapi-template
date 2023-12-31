"""migration_name

Revision ID: c5895fc1f40f
Revises: 07c71f4389b6
Create Date: 2023-06-14 03:57:12.173234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5895fc1f40f'
down_revision = '07c71f4389b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_model', sa.Column('is_active', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_model', 'is_active')
    # ### end Alembic commands ###
