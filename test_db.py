import sqlite3
import os

# ========== 1. 创建数据库和连接 ==========
db_path = "test_database.db"

# 如果之前练习建过库，先删掉保证每次运行环境干净
if os.path.exists(db_path):
    os.remove(db_path)

# 创建连接（文件不存在会自动创建）
conn = sqlite3.connect(db_path)
# 获取游标，用来执行SQL语句
cursor = conn.cursor()

print("数据库已创建:", db_path)

# ========== 2. 建表 ==========
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# 再建一张订单表，用来练多表查询
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        amount REAL NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")

print("表已创建: users, orders")

# ========== 3. 插入数据（增） ==========
# 插入用户
users_data = [
    ("admin", "123456", "admin@test.com"),
    ("testuser", "test123", "test@test.com"),
    ("zhangsan", "zs123456", "zhangsan@test.com"),
    ("lisi", "ls123456", "lisi@test.com"),
]

cursor.executemany(
    "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
    users_data
)

# 插入订单
orders_data = [
    (1, "笔记本电脑", 5999.00, "completed"),
    (1, "鼠标", 129.00, "completed"),
    (2, "键盘", 299.00, "pending"),
    (3, "显示器", 1999.00, "completed"),
    (3, "耳机", 399.00, "cancelled"),
    (4, "数据线", 29.90, "pending"),
]

cursor.executemany(
    "INSERT INTO orders (user_id, product_name, amount, status) VALUES (?, ?, ?, ?)",
    orders_data
)

conn.commit()
print("测试数据已插入")

# ========== 4. 查询数据（查） ==========
print("\n" + "="*50)
print("【练习1】查询所有用户：")
print("="*50)
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(f"ID:{row[0]}, 用户名:{row[1]}, 邮箱:{row[3]}, 创建时间:{row[4]}")

print("\n" + "="*50)
print("【练习2】查询状态为 'completed' 的订单：")
print("="*50)
cursor.execute("SELECT * FROM orders WHERE status = 'completed'")
rows = cursor.fetchall()
for row in rows:
    print(f"订单ID:{row[0]}, 商品:{row[2]}, 金额:{row[3]}, 状态:{row[4]}")

print("\n" + "="*50)
print("【练习3】多表联查：显示每个订单的用户名和商品：")
print("="*50)
cursor.execute("""
    SELECT u.username, o.product_name, o.amount, o.status
    FROM orders o
    JOIN users u ON o.user_id = u.id
""")
rows = cursor.fetchall()
for row in rows:
    print(f"用户:{row[0]}, 商品:{row[1]}, 金额:{row[2]}, 状态:{row[3]}")

print("\n" + "="*50)
print("【练习4】聚合查询：每个用户的订单总金额：")
print("="*50)
cursor.execute("""
    SELECT u.username, COUNT(o.id) as order_count, SUM(o.amount) as total_amount
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.username
""")
rows = cursor.fetchall()
for row in rows:
    print(f"用户:{row[0]}, 订单数:{row[1]}, 总金额:{row[2]}")

# ========== 5. 更新数据（改） ==========
print("\n" + "="*50)
print("【练习5】更新订单状态：")
print("="*50)
cursor.execute("UPDATE orders SET status = 'completed' WHERE id = 2")
conn.commit()
print("订单ID=2 的状态已更新为 'completed'")
# 验证
cursor.execute("SELECT * FROM orders WHERE id = 2")
row = cursor.fetchone()
print(f"验证 → 订单ID:{row[0]}, 状态:{row[4]}")

# ========== 6. 删除数据（删） ==========
print("\n" + "="*50)
print("【练习6】删除已取消的订单：")
print("="*50)
cursor.execute("DELETE FROM orders WHERE status = 'cancelled'")
conn.commit()
print("已删除状态为 'cancelled' 的订单")
# 验证
cursor.execute("SELECT COUNT(*) FROM orders")
count = cursor.fetchone()[0]
print(f"验证 → 剩余订单总数: {count}")

# ========== 7. 关闭连接 ==========
cursor.close()
conn.close()
print("\n数据库连接已关闭")