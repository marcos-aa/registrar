"""convert_existing_datetimes_to_utc

Revision ID: 262829d3c4c0
Revises: 2219ddbca669
Create Date: 2025-03-30 15:58:12.431251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '262829d3c4c0'
down_revision: Union[str, None] = '2219ddbca669'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


"""convert_existing_datetimes_to_utc"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

def upgrade():
    conn = op.get_bind()
    
    # For SQLite, we'll treat existing datetimes as UTC
    # Since SQLite doesn't natively support timezones, we'll just ensure consistency
    conn.execute(text("""
        UPDATE user_codes 
        SET expires_at = datetime(expires_at, 'utc')
    """))
    conn.execute(text("""
        UPDATE user_token 
        SET expires_at = datetime(expires_at, 'utc')
    """))

def downgrade():
    # No action needed since we're just ensuring UTC interpretation
    pass
