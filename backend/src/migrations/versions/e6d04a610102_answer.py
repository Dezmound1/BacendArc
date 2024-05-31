"""answer

Revision ID: e6d04a610102
Revises: 7a90203192f1
Create Date: 2024-05-21 08:24:31.744954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6d04a610102'
down_revision: Union[str, None] = '7a90203192f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('answer',
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.Column('stud_answer', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('answer_id')
    )
    op.create_table('user_answer',
    sa.Column('user_answer_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['answer_id'], ['answer.answer_id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['question.question_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_answer_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_answer')
    op.drop_table('answer')
    # ### end Alembic commands ###
