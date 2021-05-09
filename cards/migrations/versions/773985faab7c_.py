"""empty message

Revision ID: 773985faab7c
Revises: 
Create Date: 2021-05-09 08:01:41.747005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '773985faab7c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('camp_cards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=80), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.Column('user_card', sa.Boolean(), nullable=False),
    sa.Column('role', sa.String(length=120), nullable=False),
    sa.Column('organization', sa.String(length=120), nullable=True),
    sa.Column('user_image', sa.String(length=120), nullable=False),
    sa.Column('brand_image', sa.String(length=120), nullable=False),
    sa.Column('card_type', sa.String(length=120), nullable=False),
    sa.Column('primary_color', sa.String(length=20), nullable=False),
    sa.Column('text_color', sa.String(length=20), nullable=False),
    sa.Column('review', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('camp_cards')
    # ### end Alembic commands ###
