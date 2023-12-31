"""police station altered

Revision ID: 1c9181f8f17f
Revises: 4877cc7f1eaf
Create Date: 2023-07-19 00:51:03.760989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c9181f8f17f'
down_revision = '4877cc7f1eaf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('police_stations', sa.Column('state_code', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('police_stations', 'state_code')
    # ### end Alembic commands ###
