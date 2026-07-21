"""Add MVP module tables

Revision ID: c3f4a5b6d7e8
Revises: b2c6b8c7c1d2
Create Date: 2026-07-21
"""

from alembic import op
import sqlalchemy as sa


revision = "c3f4a5b6d7e8"
down_revision = "b2c6b8c7c1d2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "lobbies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_lobbies_id"), "lobbies", ["id"], unique=False)

    op.create_table(
        "trains",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("train_number", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("train_number"),
    )
    op.create_index(op.f("ix_trains_id"), "trains", ["id"], unique=False)

    op.create_table(
        "duties",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("duty_code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("duty_code"),
    )
    op.create_index(op.f("ix_duties_id"), "duties", ["id"], unique=False)

    op.create_table(
        "import_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_import_logs_id"), "import_logs", ["id"], unique=False)

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("actor_username", sa.String(length=100), nullable=True),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("entity", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_logs_id"), "audit_logs", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_audit_logs_id"), table_name="audit_logs")
    op.drop_table("audit_logs")

    op.drop_index(op.f("ix_import_logs_id"), table_name="import_logs")
    op.drop_table("import_logs")

    op.drop_index(op.f("ix_duties_id"), table_name="duties")
    op.drop_table("duties")

    op.drop_index(op.f("ix_trains_id"), table_name="trains")
    op.drop_table("trains")

    op.drop_index(op.f("ix_lobbies_id"), table_name="lobbies")
    op.drop_table("lobbies")
