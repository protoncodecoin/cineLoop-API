"""create playlist database

Revision ID: dc226b3d86d9
Revises:
Create Date: 2024-11-26 15:31:07.601916

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dc226b3d86d9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("playlist", sa.Column("user", sa.Integer()))


def downgrade() -> None:
    op.drop_column("playlist", "user")
