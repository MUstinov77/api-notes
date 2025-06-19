from sqlalchemy import create_engine, text


engine = create_engine(
    'sqlite+pysqlite:///:memory',
    echo=False
)

with engine.connect() as conn:
    result = conn.execute(text('select "hello world"'))
    print(type(result))
    print(type(result.all()))
    for row in result:
        print(row)


