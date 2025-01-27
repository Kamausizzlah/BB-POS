"""update

Revision ID: 9617f5d5036a
Revises: 17f6e5123a37
Create Date: 2024-08-27 18:57:51.337053

"""
from alembic import op
import sqlalchemy as sa


from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9617f5d5036a'
down_revision = '17f6e5123a37'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(), nullable=True))
        # Provide a name for the unique constraint
        batch_op.create_unique_constraint('uq_users_email', ['email'])
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        # Drop the unique constraint by its name
        batch_op.drop_constraint('uq_users_email', type_='unique')
        batch_op.drop_column('email')
    # ### end Alembic commands ###
