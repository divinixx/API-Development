"""add user table

Revision ID: cf236f850121
Revises: ea6881cf7633
Create Date: 2025-11-19 18:01:19.224188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf236f850121'
down_revision: Union[str, Sequence[str], None] = 'ea6881cf7633'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('email', sa.String(), nullable=False),    
                sa.Column('password', sa.String(), nullable=False),
                sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'), nullable=False),
                sa.PrimaryKeyConstraint('id'),
                sa.UniqueConstraint('email')
                )
pass


def downgrade():
    op.drop_table('user')
    pass
