import mysql.connector
from datetime import datetime, timedelta


id = [
    101,
    102,
    103,
    104,
    105
]

user_id = [
    101,
    102,
    103,
    104,
    105
]

email = [
    "test1",
    "test2",
    "test3",
    "test4",
    "test5"
]

item_id = [
    101,
    102,
    103,
    104,
    105
]

item_name = [
    'Vintage Timepiece',
    'Elegant Chronograph',
    'Diver’s Watch',
    'Pilot’s Watch',
    'Classic Dress Watch'
]

start_time = [
    '2023-12-02 00:00:00',
    '2023-12-02 00:00:00',
    '2023-12-02 00:00:00',
    '2023-12-02 00:00:00',
    '2023-12-02 00:00:00'
]

now = datetime.now()
# gen end_time
end_time = [
    now + timedelta(minutes=2),
    now + timedelta(minutes=4),
    now + timedelta(minutes=4),
    now + timedelta(minutes=62),
    now + timedelta(minutes=65)
]

# 將時間轉換為字串格式
end_time = [time.strftime('%Y-%m-%d %H:%M:%S') for time in end_time]

status = [
    'pending',
    'pending',
    'pending',
    'pending',
    'pending'
]

db = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="mysql",
    port=4099
)

cursor = db.cursor()


for i in range(5):
    sql = """
    INSERT INTO Auctions (id, user_id, email, item_id, item_name, start_time, end_time, status) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        id[i],
        user_id[i],
        email[i],
        item_id[i],
        item_name[i],
        start_time[i],
        end_time[i],
        status[i]
    )
    cursor.execute(sql, values)
    db.commit()

print("Inserted 5 records into the auctions database.")
