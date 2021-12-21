## Alembic Cheatsheet
### 1. Create alembic migration environment
```bash
alembic init alembic
```

### 2. Configure the migration environment
-> SQLAlchemy url
-> SQLAlchemy declarative base

### 3. Create a migration script
#### Method 1: Manual
```bash
alembic revision -m "migrations test"
```
This generates the migration script, the file contains some header information, identifiers for the current revision 
and a “downgrade” revision, an import of basic Alembic directives, and empty upgrade() and downgrade() functions. 
Then manually populate the upgrade() and downgrade() functions with directives that will apply a set of changes to our database. 
Typically, upgrade() is required while downgrade() is only needed if down-revision capability is desired, though it’s probably a good idea.

Example: 
```python
def upgrade():
    op.create_table(
        'test',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

def downgrade():
    op.drop_table('test')
```
#### Method 2: Autogenerate
Populate revision script with candidate migration operations, based on comparison of database to model.
```bash
$ alembic revision --autogenerate -m "change made to models"
```
### 4. Run the migration
```bash
$ alembic upgrade head
```
### Relative Migration Identifiers
Relative upgrades/downgrades are also supported. To move two versions from the current, a decimal value “+N” can be supplied:
```bash
$ alembic upgrade +2
```
Negative values are accepted for downgrades:
```bash
$ alembic downgrade -1
```
Relative identifiers may also be in terms of a specific revision. For example, to upgrade to revision ae1027a6acf plus two additional steps:
```bash
$ alembic upgrade ae10+2
```
### Downgrading
Downgrade to last revision
```bash
$ alembic downgrade -1
```
Downgrade to the start
```bash
$ alembic downgrade base
```
