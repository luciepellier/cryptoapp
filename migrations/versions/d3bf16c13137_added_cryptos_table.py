"""Added Cryptos table

Revision ID: d3bf16c13137
Revises: 
Create Date: 2022-10-11 10:46:34.168988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3bf16c13137'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cryptos',
    sa.Column('name', sa.String(length=55), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('cost', sa.Float(), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cryptos')
    # ### end Alembic commands ###
