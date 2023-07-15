"""applications table altered

Revision ID: 7c3926013d64
Revises: b68faa99196a
Create Date: 2023-07-13 19:46:30.747113

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7c3926013d64'
down_revision = 'b68faa99196a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('applicant_addresses', sa.Column('house_street', sa.String(length=50), nullable=True))
    op.add_column('applicant_addresses', sa.Column('city_name', sa.String(length=50), nullable=True))
    op.drop_column('applicant_addresses', 'city_ame')
    op.drop_column('applicant_addresses', 'house_treet')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('applicant_addresses', sa.Column('house_treet', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('applicant_addresses', sa.Column('city_ame', mysql.VARCHAR(length=50), nullable=True))
    op.drop_column('applicant_addresses', 'city_name')
    op.drop_column('applicant_addresses', 'house_street')
    # ### end Alembic commands ###