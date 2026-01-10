"""orders flow v1

Revision ID: 8d969f733b22
Revises: 9910221764a8
Create Date: 2026-01-09 11:51:40.894033
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '8d969f733b22'
down_revision = '9910221764a8'
branch_labels = None
depends_on = None


def upgrade():
    """
    Create order_items table
    """
    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('image', sa.String(length=500), nullable=True),
    )


def downgrade():
    """
    Drop order_items table
    """
    op.drop_table('order_items')
