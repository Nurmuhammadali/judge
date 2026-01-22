"""add foreign keys

Revision ID: 060503ae549a
Revises: ebf41cd0bb81
Create Date: 2026-01-05 04:34:35.146450

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '060503ae549a'
down_revision: Union[str, Sequence[str], None] = 'ebf41cd0bb81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key(
        "fk_submissions_problem_id_problems",
        source_table="submissions",
        referent_table="problems",
        local_cols=["problem_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "fk_test_cases_problem_id_problems",
        source_table="test_cases",
        referent_table="problems",
        local_cols=["problem_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_test_cases_problem_id_problems",
        "test_cases",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_submissions_problem_id_problems",
        "submissions",
        type_="foreignkey",
    )
