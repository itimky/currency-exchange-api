"""empty message

Revision ID: 11254fd769d3
Revises:
Create Date: 2022-04-22 05:25:20.026864

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "11254fd769d3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "currency",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_currency_id"), "currency", ["id"], unique=False)
    op.create_table(
        "currencypairrate",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("base_id", sa.Integer(), nullable=False),
        sa.Column("quote_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("rate", sa.Numeric(precision=18, scale=6), nullable=False),
        sa.ForeignKeyConstraint(
            ["base_id"],
            ["currency.id"],
        ),
        sa.ForeignKeyConstraint(
            ["quote_id"],
            ["currency.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_currencypairrate_id"), "currencypairrate", ["id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_currencypairrate_id"), table_name="currencypairrate")
    op.drop_table("currencypairrate")
    op.drop_index(op.f("ix_currency_id"), table_name="currency")
    op.drop_table("currency")
    # ### end Alembic commands ###
