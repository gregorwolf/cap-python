# Generated using ChatGPT with the following prompt:
# Create a Python script that uses the HANA Client hdbcli but instead of using a single connection 
# it uses a connection pool which re-uses an already established connection. 
import queue
import threading
from hdbcli import dbapi

class hdb_pool:
    def __init__(self, pool_size, host, port, user, password):
        self.pool_size = pool_size
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.pool = queue.Queue(maxsize=pool_size)
        self.lock = threading.Lock()

        # Initialize the connection pool with the specified number of connections
        for _ in range(pool_size):
            conn = self.create_connection()
            self.pool.put(conn)

    def create_connection(self):
        """Create a new connection to the HANA database."""
        conn = dbapi.connect(
            address=self.host,
            port=self.port,
            user=self.user,
            password=self.password
        )
        return conn

    def get_connection(self):
        """Retrieve a connection from the pool."""
        with self.lock:
            if self.pool.empty():
                conn = self.create_connection()
            else:
                conn = self.pool.get()
        return conn

    def return_connection(self, conn):
        """Return a connection back to the pool."""
        with self.lock:
            if self.pool.full():
                conn.close()
            else:
                self.pool.put(conn)

    def close_all_connections(self):
        """Close all connections in the pool."""
        while not self.pool.empty():
            conn = self.pool.get()
            conn.close()
