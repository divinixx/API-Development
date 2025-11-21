"""add content column to post table

Revision ID: ea6881cf7633
Revises: fddfdee57c4d
Create Date: 2025-11-19 16:22:58.429691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea6881cf7633'
down_revision: Union[str, Sequence[str], None] = 'fddfdee57c4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
