"""Initial migrations

Revision ID: 47917f7b80dd
Revises: 
Create Date: 2021-09-06 18:47:32.648135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47917f7b80dd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('isbn', sa.String(length=10), nullable=True),
    sa.Column('isbn13', sa.String(length=13), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('authors', sa.Text(), nullable=True),
    sa.Column('average_rating', sa.Float(), nullable=True),
    sa.Column('language_code', sa.String(length=7), nullable=True),
    sa.Column('num_pages', sa.Integer(), nullable=True),
    sa.Column('ratings_count', sa.Integer(), nullable=True),
    sa.Column('text_reviews_count', sa.Integer(), nullable=True),
    sa.Column('publication_date', sa.DateTime(), nullable=True),
    sa.Column('publisher_name', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_books_isbn'), 'books', ['isbn'], unique=False)
    op.create_index(op.f('ix_books_isbn13'), 'books', ['isbn13'], unique=False)
    op.create_index(op.f('ix_books_language_code'), 'books', ['language_code'], unique=False)
    op.create_table('member',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('member')
    op.drop_index(op.f('ix_books_language_code'), table_name='books')
    op.drop_index(op.f('ix_books_isbn13'), table_name='books')
    op.drop_index(op.f('ix_books_isbn'), table_name='books')
    op.drop_table('books')
    # ### end Alembic commands ###
