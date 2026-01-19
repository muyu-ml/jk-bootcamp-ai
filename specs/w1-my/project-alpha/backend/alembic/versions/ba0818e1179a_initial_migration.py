"""Initial migration

Revision ID: ba0818e1179a
Revises: 
Create Date: 2026-01-15 16:42:07.359542

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ba0818e1179a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create tickets table
    op.create_table(
        'tickets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('pending', 'completed', name='ticketstatus'), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("status IN ('pending', 'completed')", name='check_status')
    )
    op.create_index(op.f('ix_tickets_id'), 'tickets', ['id'], unique=False)
    op.create_index('idx_tickets_status', 'tickets', ['status'], unique=False)
    op.create_index('idx_tickets_created_at', 'tickets', ['created_at'], unique=False, postgresql_ops={'created_at': 'DESC'})
    # Full-text search index on title
    op.execute("CREATE INDEX idx_tickets_title ON tickets USING gin(to_tsvector('english', title))")

    # Create tags table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('color', sa.String(length=7), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_tags_id'), 'tags', ['id'], unique=False)
    op.create_index(op.f('ix_tags_name'), 'tags', ['name'], unique=True)

    # Create ticket_tags association table
    op.create_table(
        'ticket_tags',
        sa.Column('ticket_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('ticket_id', 'tag_id')
    )
    op.create_index('idx_ticket_tags_ticket_id', 'ticket_tags', ['ticket_id'], unique=False)
    op.create_index('idx_ticket_tags_tag_id', 'ticket_tags', ['tag_id'], unique=False)

    # Create trigger function for updating updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create trigger for tickets.updated_at
    op.execute("""
        CREATE TRIGGER update_tickets_updated_at
            BEFORE UPDATE ON tickets
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
    """)

    # Create trigger function for setting completed_at
    op.execute("""
        CREATE OR REPLACE FUNCTION set_completed_at()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.status = 'completed' AND (OLD.status IS NULL OR OLD.status != 'completed') THEN
                NEW.completed_at = CURRENT_TIMESTAMP;
            ELSIF NEW.status = 'pending' AND OLD.status = 'completed' THEN
                NEW.completed_at = NULL;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create trigger for tickets.completed_at
    op.execute("""
        CREATE TRIGGER trigger_set_completed_at
            BEFORE UPDATE ON tickets
            FOR EACH ROW
            EXECUTE FUNCTION set_completed_at();
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop triggers
    op.execute("DROP TRIGGER IF EXISTS trigger_set_completed_at ON tickets;")
    op.execute("DROP TRIGGER IF EXISTS update_tickets_updated_at ON tickets;")
    
    # Drop functions
    op.execute("DROP FUNCTION IF EXISTS set_completed_at();")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();")
    
    # Drop tables (order matters due to foreign keys)
    op.drop_index('idx_ticket_tags_tag_id', table_name='ticket_tags')
    op.drop_index('idx_ticket_tags_ticket_id', table_name='ticket_tags')
    op.drop_table('ticket_tags')
    
    op.drop_index(op.f('ix_tags_name'), table_name='tags')
    op.drop_index(op.f('ix_tags_id'), table_name='tags')
    op.drop_table('tags')
    
    op.execute("DROP INDEX IF EXISTS idx_tickets_title;")
    op.drop_index('idx_tickets_created_at', table_name='tickets')
    op.drop_index('idx_tickets_status', table_name='tickets')
    op.drop_index(op.f('ix_tickets_id'), table_name='tickets')
    op.drop_table('tickets')
    
    # Drop enum type
    op.execute("DROP TYPE IF EXISTS ticketstatus;")
