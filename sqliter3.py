import sqlite3
from threading import RLock

LOCK = RLock()


class Sqliter3:

	def __init__(self, db_filename):
		"""
		:param str db_filename: The name of the db file to open / create.
		"""
		self.db_filename = db_filename
		self.conn = None

	def __del__(self):
		"""
		Close connection to the DB when program ends without saving uncommitted changes.
		"""
		if self.conn:
			self.conn.close()

	def get_db(self):
		"""
		Connect to the DB or return an existing connection.
		:return:
		"""
		if self.conn is None:
			self.conn = sqlite3.connect(self.db_filename)
		return self.conn

	def run_query(self, query, args=None):
		"""
		:param str query: The query to run.
		:param list|tuple args: Arguments to safely inject to the query.
		:return dict: Success=True and the resulting rows if successful; success=False and and error message otherwise.
		"""
		result = {
			"success": False
		}
		try:
			conn = self.get_db()
			cur = conn.cursor()
			with LOCK:
				result["rows"] = cur.execute(query, args or [])
				conn.commit()
				result["success"] = True
		except Exception as exp:
			result["error"] = f"{exp}"
		return result
