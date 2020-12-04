"""first migration

Revision ID: 6cf261402911
Revises: 
Create Date: 2020-12-02 21:59:45.054007

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6cf261402911'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('palette',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('primary', sa.String(length=6), nullable=True),
                    sa.Column('secondary', sa.String(length=6), nullable=True),
                    sa.Column('accent', sa.String(length=6), nullable=True),
                    sa.Column('text', sa.String(length=6), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('project',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('codename', sa.String(length=4), nullable=False),
                    sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.Column('created', sa.DateTime(), nullable=True),
                    sa.Column('title', sa.String(length=80), nullable=True),
                    sa.Column('image_id', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.Column('palette_id', postgresql.UUID(as_uuid=True), nullable=True)
                    ,
                    sa.ForeignKeyConstraint(['palette_id'], ['palette.id'], ),
                    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_index(op.f('ix_project_created'), 'project', ['created'], unique=False)
    op.create_index('uix_project_codename', 'project', ['codename'], unique=True,
                    postgresql_where=sa.text('project_id IS NULL'))
    op.create_index('uix_project_codename_project_id', 'project', ['codename', 'project_id'], unique=True,
                    postgresql_where=sa.text('project_id IS NOT NULL'))
    op.create_table('content',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('codename', sa.String(length=4), nullable=False),
                    sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('created', sa.DateTime(), nullable=False),
                    sa.Column('uploaded', sa.DateTime(), nullable=True),
                    sa.Column('media_type', sa.Enum('video', 'audio', 'image', 'text', name='mediatype'),
                              nullable=False),
                    sa.Column('extension', sa.String(length=10), nullable=False),
                    sa.Column('title', sa.String(length=80), nullable=True),
                    sa.Column('palette_id', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.ForeignKeyConstraint(['palette_id'], ['palette.id'], ),
                    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('codename', 'project_id')
                    )
    op.create_index(op.f('ix_content_created'), 'content', ['created'], unique=False)
    op.create_index(op.f('ix_content_media_type'), 'content', ['media_type'], unique=False)
    op.create_index(op.f('ix_content_uploaded'), 'content', ['uploaded'], unique=False)
    sa.ForeignKeyConstraint(['image_id'], ['content.id'], )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('uix_project_codename_project_id', table_name='project')
    op.drop_index('uix_project_codename', table_name='project')
    op.drop_index(op.f('ix_project_created'), table_name='project')
    op.drop_table('project')
    op.drop_table('palette')
    op.drop_index(op.f('ix_content_uploaded'), table_name='content')
    op.drop_index(op.f('ix_content_media_type'), table_name='content')
    op.drop_index(op.f('ix_content_created'), table_name='content')
    op.drop_table('content')
    # ### end Alembic commands ###
