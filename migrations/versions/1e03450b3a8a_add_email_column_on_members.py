"""Add email column on members

Revision ID: 1e03450b3a8a
Revises: 3f8d54a758a2
Create Date: 2021-09-09 10:51:16.723926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e03450b3a8a'
down_revision = '3f8d54a758a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('members', sa.Column('email', sa.String(length=255), nullable=True))
    op.create_unique_constraint(None, 'members', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'members', type_='unique')
    op.drop_column('members', 'email')
    # ### end Alembic commands ###