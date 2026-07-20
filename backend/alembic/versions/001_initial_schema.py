"""Initial schema with users, crew, shifts, assignments, availability

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-07-20 01:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('Admin', 'Controller', 'Supervisor', 'LobbyOperator', 'Viewer', name='userrole'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Crew table
    op.create_table(
        'crew',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('crew_id', sa.String(length=50), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('department', sa.Enum('Driver', 'Conductor', 'PlatformStaff', 'Security', 'Maintenance', 'AdminStaff', name='department'), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('crew_id'),
        sa.UniqueConstraint('email'),
    )
    op.create_index(op.f('ix_crew_id'), 'crew', ['id'], unique=False)

    # Shifts table
    op.create_table(
        'shifts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('shift_date', sa.Date(), nullable=False),
        sa.Column('shift_type', sa.Enum('Morning', 'Afternoon', 'Night', 'Extended', name='shifttype'), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('crew_required', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('location', sa.String(length=100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_shifts_id'), 'shifts', ['id'], unique=False)
    op.create_index(op.f('ix_shifts_shift_date'), 'shifts', ['shift_date'], unique=False)

    # Assignments table
    op.create_table(
        'assignments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('shift_id', sa.Integer(), nullable=False),
        sa.Column('crew_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('Assigned', 'Confirmed', 'Completed', 'Cancelled', 'NoShow', name='assignmentstatus'), nullable=False, server_default='Assigned'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['crew_id'], ['crew.id'], ),
        sa.ForeignKeyConstraint(['shift_id'], ['shifts.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_assignments_id'), 'assignments', ['id'], unique=False)

    # Availabilities table
    op.create_table(
        'availabilities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('crew_id', sa.Integer(), nullable=False),
        sa.Column('available_date', sa.Date(), nullable=False),
        sa.Column('status', sa.Enum('Available', 'OnLeave', 'SickLeave', 'Unavailable', name='availabilitystatus'), nullable=False),
        sa.Column('reason', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['crew_id'], ['crew.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_availabilities_id'), 'availabilities', ['id'], unique=False)
    op.create_index(op.f('ix_availabilities_available_date'), 'availabilities', ['available_date'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_availabilities_available_date'), table_name='availabilities')
    op.drop_index(op.f('ix_availabilities_id'), table_name='availabilities')
    op.drop_table('availabilities')
    op.drop_index(op.f('ix_assignments_id'), table_name='assignments')
    op.drop_table('assignments')
    op.drop_index(op.f('ix_shifts_shift_date'), table_name='shifts')
    op.drop_index(op.f('ix_shifts_id'), table_name='shifts')
    op.drop_table('shifts')
    op.drop_index(op.f('ix_crew_id'), table_name='crew')
    op.drop_table('crew')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
