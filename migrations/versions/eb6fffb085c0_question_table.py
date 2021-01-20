"""question table

Revision ID: eb6fffb085c0
Revises: 6cf261402911
Create Date: 2020-12-12 18:07:26.686639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb6fffb085c0'
down_revision = '6cf261402911'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'project', 'content', ['image_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'project', type_='foreignkey')
    # ### end Alembic commands ###
