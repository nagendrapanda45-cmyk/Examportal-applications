# # import os
# # import time
# # import logging
# # from django.db import connection
# # from django.conf import settings
# # from home.users.models import Users  # your custom table


# # class UserRequestLoggingMiddleware:
# #     """
# #     Middleware to log request duration, latency, and query time per user.
# #     Logs are stored per custom user_id from your `users` table.
# #     """

# #     def __init__(self, get_response):
# #         self.get_response = get_response
# #         self.logs_dir = os.path.join(settings.BASE_DIR, "users_logs")
# #         os.makedirs(self.logs_dir, exist_ok=True)
# #         print(f"[Middleware Init] Logs directory created at: {self.logs_dir}")

# #     def __call__(self, request):
# #         print(f"\n[Middleware] Incoming request: {request.path} ({request.method})")

# #         start_time = time.time()
# #         connection.queries.clear()

# #         response = self.get_response(request)

# #         end_time = time.time()
# #         duration = end_time - start_time
# #         total_query_time = sum(float(q.get("time", 0)) for q in connection.queries)

# #         print(f"[Middleware] Request processed in {duration:.3f}s")
# #         print(f"[Middleware] Total DB Query Time: {total_query_time:.3f}s, Queries Executed: {len(connection.queries)}")

# #         if hasattr(request, "user") and request.user.is_authenticated:
# #             print(f"[Middleware] Authenticated user detected: auth_user.id={request.user.id}")
# #             try:
# #                 # Map auth_user → your custom users table
# #                 custom_user = Users.objects.get(user=request.user)
# #                 user_id = custom_user.user_id
# #                 print(f"[Middleware] Found custom user mapping: users.user_id={user_id}")
# #                 log_file = os.path.join(self.logs_dir, f"user_{user_id}.log")
# #             except Users.DoesNotExist:
# #                 print(f"[Middleware] No mapping found in users table for auth_user.id={request.user.id}")
# #                 log_file = os.path.join(self.logs_dir, f"authuser_{request.user.id}.log")
# #         else:
# #             print("[Middleware] Anonymous user (not logged in)")
# #             log_file = os.path.join(self.logs_dir, "anonymous.log")

# #         logger = logging.getLogger(f"user_logger_{log_file}")
# #         logger.setLevel(logging.INFO)
# #         if not logger.handlers:
# #             handler = logging.FileHandler(log_file)
# #             formatter = logging.Formatter("%(asctime)s - %(message)s")
# #             handler.setFormatter(formatter)
# #             logger.addHandler(handler)
# #             print(f"[Middleware] Logger initialized for file: {log_file}")

# #         logger.info(
# #             f"Path: {request.path}, Method: {request.method}, "
# #             f"Duration: {duration:.3f}s, Query Time: {total_query_time:.3f}s, "
# #             f"Queries: {len(connection.queries)}"
# #         )
# #         print(f"[Middleware] Log entry written to {log_file}")

# #         return response


# import os
# import time
# import logging
# import sqlparse
# from django.db import connection
# from django.conf import settings
# from home.users.models import Users  # your custom table


# class UserRequestLoggingMiddleware:
#     """
#     Middleware to log request duration, latency, and query time per user.
#     Logs are stored per custom user_id from your `users` table.
#     """

#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.logs_dir = os.path.join(settings.BASE_DIR, "users_logs")
#         os.makedirs(self.logs_dir, exist_ok=True)
#         print(f"[Middleware Init] Logs directory created at: {self.logs_dir}")

#     def __call__(self, request):
#         print(f"\n[Middleware] Incoming request: {request.path} ({request.method})")

#         start_time = time.time()
#         connection.queries.clear()

#         response = self.get_response(request)

#         end_time = time.time()
#         duration = end_time - start_time
#         total_query_time = sum(float(q.get("time", 0)) for q in connection.queries)

#         print(f"[Middleware] Request processed in {duration:.3f}s")
#         print(f"[Middleware] Total DB Query Time: {total_query_time:.3f}s, Queries Executed: {len(connection.queries)}")

#         # 🔎 Print each formatted query
#         for i, query in enumerate(connection.queries, start=1):
#             formatted_sql = sqlparse.format(query.get("sql"), reindent=True, keyword_case="upper")
#             print(f"[Query {i}] (time: {query.get('time')}s)\n{formatted_sql}\n")

#         if hasattr(request, "user") and request.user.is_authenticated:
#             print(f"[Middleware] Authenticated user detected: auth_user.id={request.user.id}")
#             try:
#                 # Map auth_user → your custom users table
#                 custom_user = Users.objects.get(user=request.user)
#                 user_id = custom_user.user_id
#                 print(f"[Middleware] Found custom user mapping: users.user_id={user_id}")
#                 log_file = os.path.join(self.logs_dir, f"user_{user_id}.log")
#             except Users.DoesNotExist:
#                 print(f"[Middleware] No mapping found in users table for auth_user.id={request.user.id}")
#                 log_file = os.path.join(self.logs_dir, f"authuser_{request.user.id}.log")
#         else:
#             print("[Middleware] Anonymous user (not logged in)")
#             log_file = os.path.join(self.logs_dir, "anonymous.log")

#         logger = logging.getLogger(f"user_logger_{log_file}")
#         logger.setLevel(logging.INFO)
#         if not logger.handlers:
#             handler = logging.FileHandler(log_file)
#             formatter = logging.Formatter("%(asctime)s - %(message)s")
#             handler.setFormatter(formatter)
#             logger.addHandler(handler)
#             print(f"[Middleware] Logger initialized for file: {log_file}")

#         logger.info(
#             f"Path: {request.path}, Method: {request.method}, "
#             f"Duration: {duration:.3f}s, Query Time: {total_query_time:.3f}s, "
#             f"Queries: {len(connection.queries)}"
#         )

#         # 🔎 Save formatted queries into the log file
#         for i, query in enumerate(connection.queries, start=1):
#             formatted_sql = sqlparse.format(query.get("sql"), reindent=True, keyword_case="upper")
#             logger.info(f"[Query {i}] (time: {query.get('time')}s)\n{formatted_sql}\n")

#         print(f"[Middleware] Log entry written to {log_file}")

#         return response

# import os
# import time
# import logging
# import sqlparse
# from django.db import connection
# from django.conf import settings
# from home.users.models import Users


# class UserRequestLoggingMiddleware:
#     """
#     Middleware to log request duration, latency, and query time per user.
#     Also appends a summary at the end of the user's log file.
#     """

#     # 🔹 Keep stats in memory for each user
#     user_stats = {}

#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.logs_dir = os.path.join(settings.BASE_DIR, "users_logs")
#         os.makedirs(self.logs_dir, exist_ok=True)
#         print(f"[Middleware Init] Logs directory created at: {self.logs_dir}")

#     def __call__(self, request):
#         start_time = time.time()
#         connection.queries.clear()

#         response = self.get_response(request)

#         duration = time.time() - start_time
#         total_query_time = sum(float(q.get("time", 0)) for q in connection.queries)

#         # 🔹 Detect user
#         if hasattr(request, "user") and request.user.is_authenticated:
#             try:
#                 custom_user = Users.objects.get(user=request.user)
#                 user_id = custom_user.user_id
#                 log_file = os.path.join(self.logs_dir, f"user_{user_id}.log")
#             except Users.DoesNotExist:
#                 user_id = f"auth_{request.user.id}"
#                 log_file = os.path.join(self.logs_dir, f"authuser_{request.user.id}.log")
#         else:
#             user_id = "anonymous"
#             log_file = os.path.join(self.logs_dir, "anonymous.log")

#         # 🔹 Logger setup
#         logger = logging.getLogger(f"user_logger_{log_file}")
#         logger.setLevel(logging.INFO)
#         if not logger.handlers:
#             handler = logging.FileHandler(log_file)
#             formatter = logging.Formatter("%(asctime)s - %(message)s")
#             handler.setFormatter(formatter)
#             logger.addHandler(handler)

#         # 🔹 Log request + queries
#         logger.info(
#             f"Path: {request.path}, Method: {request.method}, "
#             f"Duration: {duration:.3f}s, Query Time: {total_query_time:.3f}s, "
#             f"Queries: {len(connection.queries)}"
#         )

#         for i, query in enumerate(connection.queries, start=1):
#             formatted_sql = sqlparse.format(query.get("sql"), reindent=True, keyword_case="upper")
#             logger.info(f"[Query {i}] (time: {query.get('time')}s)\n{formatted_sql}\n")

#         # 🔹 Update summary stats in memory
#         stats = self.user_stats.setdefault(user_id, {
#             "total_requests": 0,
#             "total_duration": 0,
#             "total_queries": 0,
#             "total_query_time": 0,
#             "slowest_request": 0,
#             "slowest_query_time": 0,
#             "slowest_query_sql": None,
#         })

#         stats["total_requests"] += 1
#         stats["total_duration"] += duration
#         stats["total_queries"] += len(connection.queries)
#         stats["total_query_time"] += total_query_time
#         stats["slowest_request"] = max(stats["slowest_request"], duration)

#         for q in connection.queries:
#             q_time = float(q.get("time", 0))
#             if q_time > stats["slowest_query_time"]:
#                 stats["slowest_query_time"] = q_time
#                 stats["slowest_query_sql"] = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")

#         # 🔹 Write summary block at the end of the file
#         avg_duration = stats["total_duration"] / stats["total_requests"]
#         logger.info("\n====== USER SUMMARY ======")
#         logger.info(f"Total Requests: {stats['total_requests']}")
#         logger.info(f"Total Queries: {stats['total_queries']}")
#         logger.info(f"Total Query Time: {stats['total_query_time']:.3f}s")
#         logger.info(f"Avg Request Duration: {avg_duration:.3f}s")
#         logger.info(f"Slowest Request Duration: {stats['slowest_request']:.3f}s")
#         logger.info(f"Slowest Query Time: {stats['slowest_query_time']:.3f}s")
#         if stats["slowest_query_sql"]:
#             logger.info("Slowest Query SQL:\n" + stats["slowest_query_sql"])
#         logger.info("==========================\n")

#         return response


# import os
# import time
# import logging
# import sqlparse
# from django.db import connection
# from django.conf import settings
# from home.users.models import Users


# class UserRequestLoggingMiddleware:
#     """
#     Middleware to log request duration, latency, query time,
#     and maintain per-user summaries including longest query.
#     """

#     user_stats = {}  # in-memory stats per user

#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.logs_dir = os.path.join(settings.BASE_DIR, "users_logs")
#         os.makedirs(self.logs_dir, exist_ok=True)
#         print(f"[Middleware Init] Logs directory created at: {self.logs_dir}")

#     def __call__(self, request):
#         start_time = time.time()
#         connection.queries.clear()

#         response = self.get_response(request)

#         duration = time.time() - start_time
#         total_query_time = sum(float(q.get("time", 0)) for q in connection.queries)

#         # 🔹 Detect user
#         if hasattr(request, "user") and request.user.is_authenticated:
#             try:
#                 custom_user = Users.objects.get(user=request.user)
#                 user_id = custom_user.user_id
#                 log_file = os.path.join(self.logs_dir, f"user_{user_id}.log")
#             except Users.DoesNotExist:
#                 user_id = f"auth_{request.user.id}"
#                 log_file = os.path.join(self.logs_dir, f"authuser_{request.user.id}.log")
#         else:
#             user_id = "anonymous"
#             log_file = os.path.join(self.logs_dir, "anonymous.log")

#         # 🔹 Logger setup
#         logger = logging.getLogger(f"user_logger_{log_file}")
#         logger.setLevel(logging.INFO)
#         if not logger.handlers:
#             handler = logging.FileHandler(log_file)
#             formatter = logging.Formatter("%(asctime)s - %(message)s")
#             handler.setFormatter(formatter)
#             logger.addHandler(handler)

#         # 🔹 Log per-request
#         logger.info(
#             f"Path: {request.path}, Method: {request.method}, "
#             f"Duration: {duration:.3f}s, Query Time: {total_query_time:.3f}s, "
#             f"Queries: {len(connection.queries)}"
#         )

#         for i, query in enumerate(connection.queries, start=1):
#             formatted_sql = sqlparse.format(query.get("sql"), reindent=True, keyword_case="upper")
#             logger.info(f"[Query {i}] (time: {query.get('time')}s)\n{formatted_sql}\n")

#         # 🔹 Update in-memory stats
#         stats = self.user_stats.setdefault(user_id, {
#             "total_requests": 0,
#             "total_duration": 0,
#             "total_queries": 0,
#             "total_query_time": 0,
#             "slowest_request": 0,
#             "longest_query_time": 0,
#             "longest_query_sql": None,
#         })

#         stats["total_requests"] += 1
#         stats["total_duration"] += duration
#         stats["total_queries"] += len(connection.queries)
#         stats["total_query_time"] += total_query_time
#         stats["slowest_request"] = max(stats["slowest_request"], duration)

#         # track longest query
#         for q in connection.queries:
#             q_time = float(q.get("time", 0))
#             if q_time > stats["longest_query_time"]:
#                 stats["longest_query_time"] = q_time
#                 stats["longest_query_sql"] = sqlparse.format(
#                     q.get("sql"), reindent=True, keyword_case="upper"
#                 )

#         # 🔹 Append summary (after each request)
#         avg_duration = stats["total_duration"] / stats["total_requests"]
#         logger.info("\n====== USER SUMMARY ======")
#         logger.info(f"Total Requests: {stats['total_requests']}")
#         logger.info(f"Total Queries: {stats['total_queries']}")
#         logger.info(f"Total Query Time: {stats['total_query_time']:.3f}s")
#         logger.info(f"Avg Request Duration: {avg_duration:.3f}s")
#         logger.info(f"Slowest Request Duration: {stats['slowest_request']:.3f}s")
#         logger.info(f"Longest Query Duration: {stats['longest_query_time']:.3f}s")
#         if stats["longest_query_sql"]:
#             logger.info("Longest Query SQL:\n" + stats["longest_query_sql"])
#         logger.info("==========================\n")

#         return response


# import os
# import time
# import logging
# import sqlparse
# from django.db import connection
# from django.conf import settings
# from home.users.models import Users

# # Dictionary to keep per-user stats in-memory during server runtime
# USER_STATS = {}

# class UserRequestLoggingMiddleware:
#     """
#     Middleware to log request duration, all SQL queries, 
#     total query time, longest query, and maintain per-user statistics.
#     """

#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.logs_dir = os.path.join(settings.BASE_DIR, "users_logs")
#         os.makedirs(self.logs_dir, exist_ok=True)
#         print(f"[Middleware Init] Logs directory created at: {self.logs_dir}")

#     def __call__(self, request):
#         start_time = time.time()
#         connection.queries.clear()

#         response = self.get_response(request)

#         end_time = time.time()
#         duration = end_time - start_time
#         total_query_time = sum(float(q.get("time", 0)) for q in connection.queries)

#         # Determine user-specific log file
#         log_file = os.path.join(self.logs_dir, "anonymous.log")
#         user_key = "anonymous"
#         if hasattr(request, "user") and request.user.is_authenticated:
#             try:
#                 custom_user = Users.objects.get(email=request.user.email)  # or map properly
#                 user_id = custom_user.user_id
#                 log_file = os.path.join(self.logs_dir, f"user_{user_id}.log")
#                 user_key = str(user_id)
#             except Users.DoesNotExist:
#                 pass

#         # Setup logger
#         logger = logging.getLogger(f"user_logger_{log_file}")
#         logger.setLevel(logging.INFO)
#         if not logger.handlers:
#             handler = logging.FileHandler(log_file)
#             formatter = logging.Formatter("%(asctime)s - %(message)s")
#             handler.setFormatter(formatter)
#             logger.addHandler(handler)

#         # Initialize per-user stats if first request
#         if user_key not in USER_STATS:
#             USER_STATS[user_key] = {
#                 "total_requests": 0,
#                 "total_queries": 0,
#                 "total_query_time": 0.0,
#                 "total_request_duration": 0.0,
#                 "slowest_request": 0.0,
#                 "longest_query_time": 0.0,
#                 "longest_query_sql": ""
#             }

#         stats = USER_STATS[user_key]
#         stats["total_requests"] += 1
#         stats["total_queries"] += len(connection.queries)
#         stats["total_query_time"] += total_query_time
#         stats["total_request_duration"] += duration
#         stats["slowest_request"] = max(stats["slowest_request"], duration)

#         # Track longest query
#         for query in connection.queries:
#             time_taken = float(query.get("time", 0))
#             sql = sqlparse.format(query.get("sql"), reindent=True, keyword_case="upper")
#             if time_taken > stats["longest_query_time"]:
#                 stats["longest_query_time"] = time_taken
#                 stats["longest_query_sql"] = sql

#             # Log each query
#             logger.info(f"[Query] (time: {time_taken}s)\n{sql}\n")

#         logger.info(f"Path: {request.path}, Method: {request.method}, Duration: {duration:.3f}s, "
#                     f"Total Query Time: {total_query_time:.3f}s, Queries Executed: {len(connection.queries)}")

#         # Log user summary at end of this request
#         avg_duration = stats["total_request_duration"] / stats["total_requests"] if stats["total_requests"] else 0.0

#         logger.info("\n====== USER SUMMARY ======")
#         logger.info(f"Total Requests: {stats['total_requests']}")
#         logger.info(f"Total Queries: {stats['total_queries']}")
#         logger.info(f"Total Query Time: {stats['total_query_time']:.3f}s")
#         logger.info(f"Avg Request Duration: {avg_duration:.3f}s")
#         logger.info(f"Slowest Request Duration: {stats['slowest_request']:.3f}s")
#         logger.info(f"Longest Query Duration: {stats['longest_query_time']:.3f}s")
#         if stats["longest_query_sql"]:
#             logger.info("Longest Query SQL:\n" + stats["longest_query_sql"])
#         logger.info("==========================\n")

#         print(f"[Middleware] Request logged and summary updated for user: {user_key}")

#         return response


# import os
# import time
# import logging
# import sqlparse
# from django.db import connection
# from django.conf import settings
# from home.users.models import Users

# # In-memory per-user stats
# USER_STATS = {}

# class UserRequestLoggingMiddleware:

#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.logs_dir = os.path.join(settings.BASE_DIR, "users_logs")
#         os.makedirs(self.logs_dir, exist_ok=True)
#         print(f"[Middleware Init] Logs directory created at: {self.logs_dir}")

#     def __call__(self, request):
#         start_time = time.time()
#         connection.queries.clear()

#         response = self.get_response(request)

#         end_time = time.time()
#         duration = end_time - start_time
#         total_query_time = sum(float(q.get("time", 0)) for q in connection.queries)

#         # Map user
#         user_key = "anonymous"
#         log_file = os.path.join(self.logs_dir, "anonymous.log")

#         if hasattr(request, "user") and request.user.is_authenticated:
#             try:
#                 # Map by email or any unique field in Users
#                 custom_user = Users.objects.get(email=request.user.email)
#                 user_id = custom_user.user_id
#                 log_file = os.path.join(self.logs_dir, f"user_{user_id}.log")
#                 user_key = str(user_id)
#             except Users.DoesNotExist:
#                 pass

#         # Logger setup
#         logger = logging.getLogger(f"user_logger_{log_file}")
#         logger.setLevel(logging.INFO)
#         if not logger.handlers:
#             handler = logging.FileHandler(log_file)
#             formatter = logging.Formatter("%(asctime)s - %(message)s")
#             handler.setFormatter(formatter)
#             logger.addHandler(handler)

#         # Initialize stats
#         if user_key not in USER_STATS:
#             USER_STATS[user_key] = {
#                 "total_requests": 0,
#                 "total_queries": 0,
#                 "total_query_time": 0.0,
#                 "total_request_duration": 0.0,
#                 "slowest_request": 0.0,
#                 "longest_request": 0.0,
#                 "longest_query_time": 0.0,
#                 "longest_query_sql": "",
#             }

#         stats = USER_STATS[user_key]
#         stats["total_requests"] += 1
#         stats["total_queries"] += len(connection.queries)
#         stats["total_query_time"] += total_query_time
#         stats["total_request_duration"] += duration
#         stats["slowest_request"] = max(stats["slowest_request"], duration)
#         stats["longest_request"] = max(stats.get("longest_request", 0), duration)

#         # Track longest and slowest query per request
#         slowest_query_time = 0.0
#         slowest_query_sql = ""
#         for query in connection.queries:
#             time_taken = float(query.get("time", 0))
#             sql = sqlparse.format(query.get("sql"), reindent=True, keyword_case="upper")
#             if time_taken > stats["longest_query_time"]:
#                 stats["longest_query_time"] = time_taken
#                 stats["longest_query_sql"] = sql
#             if time_taken > slowest_query_time:
#                 slowest_query_time = time_taken
#                 slowest_query_sql = sql
#             # Log each query
#             logger.info(f"[Query] (time: {time_taken}s)\n{sql}\n")

#         # Log request info
#         logger.info(
#             f"Path: {request.path}, Method: {request.method}, Duration: {duration:.3f}s, "
#             f"Total Query Time: {total_query_time:.3f}s, Queries Executed: {len(connection.queries)}"
#         )

#         # User summary
#         avg_duration = stats["total_request_duration"] / stats["total_requests"] if stats["total_requests"] else 0.0
#         logger.info("\n====== USER SUMMARY ======")
#         logger.info(f"Total Requests: {stats['total_requests']}")
#         logger.info(f"Total Queries: {stats['total_queries']}")
#         logger.info(f"Total Query Time: {stats['total_query_time']:.3f}s")
#         logger.info(f"Avg Request Duration: {avg_duration:.3f}s")
#         logger.info(f"Slowest Request Duration: {stats['slowest_request']:.3f}s")
#         logger.info(f"Longest Request Duration: {stats['longest_request']:.3f}s")
#         logger.info(f"Longest Query Duration: {stats['longest_query_time']:.3f}s")
#         if stats["longest_query_sql"]:
#             logger.info("Longest Query SQL:\n" + stats["longest_query_sql"])
#         # Slowest query for this request
#         if slowest_query_sql:
#             logger.info(f"Slowest Query Duration for this request: {slowest_query_time:.3f}s")
#             logger.info("Slowest Query SQL:\n" + slowest_query_sql)
#         logger.info("==========================\n")

#         print(f"[Middleware] Request logged and summary updated for user: {user_key}")
#         return response


# import os
# import time
# import logging
# import sqlparse
# from django.db import connection
# from django.conf import settings
# from home.users.models import Users

# # Per-user stats dictionary
# user_stats = {}

# class UserRequestLoggingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.logs_dir = os.path.join(settings.BASE_DIR, "users_logs")
#         os.makedirs(self.logs_dir, exist_ok=True)
#         print(f"[Middleware Init] Logs directory created at: {self.logs_dir}")

#     def __call__(self, request):
#         start_time = time.time()
#         connection.queries.clear()

#         response = self.get_response(request)

#         end_time = time.time()
#         duration = end_time - start_time
#         total_query_time = sum(float(q.get("time", 0)) for q in connection.queries)

#         # Determine user identity
#         if hasattr(request, "user") and request.user.is_authenticated:
#             try:
#                 custom_user = Users.objects.get(email=request.user.email)
#                 user_id = custom_user.user_id
#                 log_file = os.path.join(self.logs_dir, f"user_{user_id}.log")
#                 user_key = str(user_id)
#             except Users.DoesNotExist:
#                 log_file = os.path.join(self.logs_dir, f"authuser_{request.user.id}.log")
#                 user_key = f"authuser_{request.user.id}"
#         else:
#             log_file = os.path.join(self.logs_dir, "anonymous.log")
#             user_key = "anonymous"

#         # Logger setup
#         logger = logging.getLogger(f"user_logger_{user_key}")
#         logger.setLevel(logging.INFO)
#         if not logger.handlers:
#             handler = logging.FileHandler(log_file)
#             formatter = logging.Formatter("%(asctime)s - %(message)s")
#             handler.setFormatter(formatter)
#             logger.addHandler(handler)

#         # Log request info
#         logger.info(
#             f"\n[REQUEST] Path: {request.path}, Method: {request.method}, "
#             f"Duration: {duration:.3f}s, Query Time: {total_query_time:.3f}s, "
#             f"Queries: {len(connection.queries)}"
#         )

#         # Log individual queries
#         for i, q in enumerate(connection.queries, start=1):
#             sql = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")
#             q_time = float(q.get("time", 0))
#             logger.info(f"[QUERY {i}] Time: {q_time:.5f}s\n{sql}\n")

#         # Update user stats
#         if user_key not in user_stats:
#             user_stats[user_key] = {
#                 "total_requests": 0,
#                 "total_queries": 0,
#                 "total_query_time": 0.0,
#                 "slowest_request": 0.0,
#                 "longest_request": 0.0,
#                 "slowest_query_time": 0.0,
#                 "slowest_query_sql": "",
#                 "longest_query_time": 0.0,
#                 "longest_query_sql": ""
#             }

#         stats = user_stats[user_key]
#         stats["total_requests"] += 1
#         stats["total_queries"] += len(connection.queries)
#         stats["total_query_time"] += total_query_time
#         stats["slowest_request"] = max(stats["slowest_request"], duration)
#         stats["longest_request"] = max(stats["longest_request"], duration)

#         # Track slowest/longest queries
#         for q in connection.queries:
#             q_time = float(q.get("time", 0))
#             sql = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")
#             if q_time > stats["longest_query_time"]:
#                 stats["longest_query_time"] = q_time
#                 stats["longest_query_sql"] = sql
#             if q_time > stats["slowest_query_time"]:
#                 stats["slowest_query_time"] = q_time
#                 stats["slowest_query_sql"] = sql

#         # Log summary per request
#         avg_duration = stats["total_query_time"] / stats["total_requests"] if stats["total_requests"] > 0 else 0
#         logger.info("\n====== USER SUMMARY ======")
#         logger.info(f"Total Requests: {stats['total_requests']}")
#         logger.info(f"Total Queries: {stats['total_queries']}")
#         logger.info(f"Total Query Time: {stats['total_query_time']:.3f}s")
#         logger.info(f"Avg Request Duration: {avg_duration:.3f}s")
#         logger.info(f"Slowest Request Duration: {stats['slowest_request']:.3f}s")
#         logger.info(f"Longest Request Duration: {stats['longest_request']:.3f}s")
#         logger.info(f"Longest Query Duration: {stats['longest_query_time']:.5f}s")
#         if stats["longest_query_sql"]:
#             logger.info("Longest Query SQL:\n" + stats["longest_query_sql"])
#         logger.info(f"Slowest Query Duration: {stats['slowest_query_time']:.5f}s")
#         if stats["slowest_query_sql"]:
#             logger.info("Slowest Query SQL:\n" + stats["slowest_query_sql"])
#         logger.info("==========================\n")

#         return response




# import os
# import time
# import logging
# import sqlparse
# from django.db import connection
# from django.conf import settings
# from home.users.models import Users

# # Global per-user stats dictionary
# user_stats = {}

# class UserRequestLoggingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.logs_dir = os.path.join(settings.BASE_DIR, "users_logs")
#         os.makedirs(self.logs_dir, exist_ok=True)
#         print(f"--------------start------------------\n")
#         print(f"[Middleware Init] Logs directory created at: {self.logs_dir}")

#     def __call__(self, request):
#         start_time = time.time()
#         connection.queries.clear()

#         response = self.get_response(request)

#         end_time = time.time()
#         duration = end_time - start_time
#         total_query_time = sum(float(q.get("time", 0)) for q in connection.queries)

#         # Determine user identity
#         if hasattr(request, "user") and request.user.is_authenticated:
#             try:
#                 custom_user = Users.objects.get(email=request.user.email)
#                 user_id = custom_user.user_id
#                 log_file = os.path.join(self.logs_dir, f"user_{user_id}.log")
#                 user_key = str(user_id)
#             except Users.DoesNotExist:
#                 log_file = os.path.join(self.logs_dir, f"authuser_{request.user.id}.log")
#                 user_key = f"authuser_{request.user.id}"
#         else:
#             log_file = os.path.join(self.logs_dir, "anonymous.log")
#             user_key = "anonymous"

#         # Setup logger
#         logger = logging.getLogger(f"user_logger_{user_key}")
#         logger.setLevel(logging.INFO)
#         if not logger.handlers:
#             handler = logging.FileHandler(log_file)
#             formatter = logging.Formatter("%(asctime)s - %(message)s")
#             handler.setFormatter(formatter)
#             logger.addHandler(handler)

#         # Log request info
#         logger.info(
#             f"\n[REQUEST] Path: {request.path}, Method: {request.method}, "
#             f"Duration: {duration:.3f}s, Query Time: {total_query_time:.3f}s, "
#             f"Queries: {len(connection.queries)}"
#         )

#         # Log individual queries
#         for i, q in enumerate(connection.queries, start=1):
#             sql = q.get("sql", "").strip()
#             if sql.upper() in ["COMMIT", "BEGIN", "ROLLBACK"]:
#                 continue  # skip trivial transaction queries
#             q_time = float(q.get("time", 0))
#             sql_formatted = sqlparse.format(sql, reindent=True, keyword_case="upper")
#             logger.info(f"[QUERY {i}] Time: {q_time:.5f}s\n{sql_formatted}\n")

#         # Initialize stats if first request for this user
#         if user_key not in user_stats:
#             user_stats[user_key] = {
#                 "total_requests": 0,
#                 "total_queries": 0,
#                 "total_query_time": 0.0,
#                 "slowest_request": 0.0,
#                 "longest_request": 0.0,
#                 "slowest_query_time": 0.0,
#                 "slowest_query_sql": "",
#                 "longest_query_time": 0.0,
#                 "longest_query_sql": ""
#             }

#         stats = user_stats[user_key]
#         stats["total_requests"] += 1
#         stats["total_queries"] += len(connection.queries)
#         stats["total_query_time"] += total_query_time
#         stats["slowest_request"] = max(stats["slowest_request"], duration)
#         stats["longest_request"] = max(stats["longest_request"], duration)

#         # Track slowest/longest queries
#         for q in connection.queries:
#             sql = q.get("sql", "").strip()
#             if not sql or sql.upper() in ["COMMIT", "BEGIN", "ROLLBACK"]:
#                 continue
#             q_time = float(q.get("time", 0))
#             sql_formatted = sqlparse.format(sql, reindent=True, keyword_case="upper")

#             if q_time > stats["longest_query_time"]:
#                 stats["longest_query_time"] = q_time
#                 stats["longest_query_sql"] = sql_formatted

#             if stats["slowest_query_time"] == 0.0 or q_time < stats["slowest_query_time"]:
#                 stats["slowest_query_time"] = q_time
#                 stats["slowest_query_sql"] = sql_formatted

#         # Log summary per request
#         avg_duration = stats["total_query_time"] / stats["total_requests"] if stats["total_requests"] > 0 else 0
#         logger.info("\n====== USER SUMMARY ======")
#         logger.info(f"Total Requests: {stats['total_requests']}")
#         logger.info(f"Total Queries: {stats['total_queries']}")
#         logger.info(f"Total Query Time: {stats['total_query_time']:.5f}s")
#         logger.info(f"Avg Request Duration: {avg_duration:.5f}s")
#         logger.info(f"Slowest Request Duration: {stats['slowest_request']:.5f}s")
#         logger.info(f"Longest Request Duration: {stats['longest_request']:.5f}s")
#         logger.info(f"Longest Query Duration: {stats['longest_query_time']:.5f}s")
#         if stats["longest_query_sql"]:
#             logger.info("Longest Query SQL:\n" + stats["longest_query_sql"])
#         logger.info(f"Slowest Query Duration: {stats['slowest_query_time']:.5f}s")
#         if stats["slowest_query_sql"]:
#             logger.info("Slowest Query SQL:\n" + stats["slowest_query_sql"])
#         logger.info("================End==========\n")

#         return response





# import os
# import time
# import logging
# import sqlparse
# from django.db import connection
# from django.conf import settings

# # Per-user stats dictionary (in-memory)
# user_stats = {}

# class UserRequestLoggingMiddleware:
#     """
#     Middleware to log request duration, query times, and per-user stats.
#     Stores logs per user in `users_logs/user_{user_id}.log`.
#     Tracks:
#         - Slowest/Longest Request Duration
#         - Slowest/Longest Query Duration
#         - Total Requests & Queries
#         - Average Request Duration
#     """

#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.logs_dir = os.path.join(settings.BASE_DIR, "users_logs")
#         os.makedirs(self.logs_dir, exist_ok=True)
#         print(f"[Middleware Init] Logs directory created at: {self.logs_dir}")

#     def __call__(self, request):
        
#         start_time = time.time()
#         connection.queries.clear()

#         response = self.get_response(request)

#         end_time = time.time()
#         duration = end_time - start_time
#         total_query_time = sum(float(q.get("time", 0)) for q in connection.queries)

#         # ------------------------------
#         # Determine user identity
#         # ------------------------------
#         user_id = request.session.get("user_id")  # store at login
#         if user_id:
#             log_file = os.path.join(self.logs_dir, f"user_{user_id}.log")
#             user_key = str(user_id)
#         elif hasattr(request, "user") and request.user.is_authenticated:
#             log_file = os.path.join(self.logs_dir, f"authuser_{request.user.id}.log")
#             user_key = f"authuser_{request.user.id}"
#         else:
#             log_file = os.path.join(self.logs_dir, "anonymous.log")
#             user_key = "anonymous"

#         # ------------------------------
#         # Logger setup
#         # ------------------------------
#         logger = logging.getLogger(f"user_logger_{user_key}")
#         logger.setLevel(logging.INFO)
#         if not logger.handlers:
#             handler = logging.FileHandler(log_file)
#             formatter = logging.Formatter("%(asctime)s - %(message)s")
#             handler.setFormatter(formatter)
#             logger.addHandler(handler)

#         # ------------------------------
#         # Log request info
#         # ------------------------------
#         logger.info("=============Start=============\n")
#         logger.info(
#             f"\n[REQUEST] Path: {request.path}, Method: {request.method}, "
#             f"Duration: {duration:.5f}s, Query Time: {total_query_time:.5f}s, "
#             f"Queries: {len(connection.queries)}"
#         )

#         # ------------------------------
#         # Log individual queries
#         # ------------------------------
#         for i, q in enumerate(connection.queries, start=1):
#             sql = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")
#             q_time = float(q.get("time", 0))
#             logger.info(f"[QUERY {i}] Time: {q_time:.5f}s\n{sql}\n")

#         # ------------------------------
#         # Update per-user stats
#         # ------------------------------
#         if user_key not in user_stats:
#             user_stats[user_key] = {
#                 "total_requests": 0,
#                 "total_queries": 0,
#                 "total_query_time": 0.0,
#                 "slowest_request": 0.0,
#                 "longest_request": 0.0,
#                 "slowest_query_time": 0.0,
#                 "slowest_query_sql": "",
#                 "longest_query_time": 0.0,
#                 "longest_query_sql": ""
#             }

#         stats = user_stats[user_key]
#         stats["total_requests"] += 1
#         stats["total_queries"] += len(connection.queries)
#         stats["total_query_time"] += total_query_time
#         stats["slowest_request"] = max(stats["slowest_request"], duration)
#         stats["longest_request"] = max(stats["longest_request"], duration)

#         for q in connection.queries:
#             q_time = float(q.get("time", 0))
#             sql = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")

#             # Track longest query
#             if q_time > stats["longest_query_time"]:
#                 stats["longest_query_time"] = q_time
#                 stats["longest_query_sql"] = sql

#             # Track slowest query (if needed separately from longest)
#             if q_time > stats["slowest_query_time"]:
#                 stats["slowest_query_time"] = q_time
#                 stats["slowest_query_sql"] = sql

#         avg_request_duration = stats["total_query_time"] / stats["total_requests"] if stats["total_requests"] > 0 else 0

#         # ------------------------------
#         # Log summary per user
#         # ------------------------------
#         logger.info("\n====== USER SUMMARY ======")
#         logger.info(f"Total Requests: {stats['total_requests']}")
#         logger.info(f"Total Queries: {stats['total_queries']}")
#         logger.info(f"Total Query Time: {stats['total_query_time']:.5f}s")
#         logger.info(f"Avg Request Duration: {avg_request_duration:.5f}s")
#         logger.info(f"Slowest Request Duration: {stats['slowest_request']:.5f}s")
#         logger.info(f"Longest Request Duration: {stats['longest_request']:.5f}s")
#         logger.info(f"Longest Query Duration: {stats['longest_query_time']:.5f}s")
#         if stats["longest_query_sql"]:
#             logger.info("Longest Query SQL:\n" + stats["longest_query_sql"])
#         logger.info(f"Slowest Query Duration: {stats['slowest_query_time']:.5f}s")
#         if stats["slowest_query_sql"]:
#             logger.info("Slowest Query SQL:\n" + stats["slowest_query_sql"])
#         logger.info("=============End=============\n")

#         return response


# import os
# import time
# import logging
# import sqlparse
# from django.db import connection
# from django.conf import settings

# # In-memory per-user stats
# user_stats = {}

# class UserRequestLoggingMiddleware:
#     """
#     Middleware to log request duration, query times, and per-user stats.
#     Stores logs per user in `users_logs/user_{user_id}.log`.
#     Tracks:
#         - Slowest/Longest Request Duration
#         - Slowest/Longest Query Duration
#         - Total Requests & Queries (executed only)
#         - Average Request Duration
#     """

#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.logs_dir = os.path.join(settings.BASE_DIR, "users_logs")
#         os.makedirs(self.logs_dir, exist_ok=True)
#         print(f"[Middleware Init] Logs directory created at: {self.logs_dir}")

#     def __call__(self, request):
#         start_time = time.time()
#         connection.queries.clear()

#         response = self.get_response(request)

#         end_time = time.time()
#         duration = end_time - start_time

#         # Only include queries that actually took time
#         executed_queries = [q for q in connection.queries if float(q.get("time", 0)) > 0]
#         total_query_time = sum(float(q.get("time", 0)) for q in executed_queries)

#         # ------------------------------
#         # Determine user identity
#         # ------------------------------
#         user_id = request.session.get("user_id")  # store at login
#         if user_id:
#             log_file = os.path.join(self.logs_dir, f"user_{user_id}.log")
#             user_key = str(user_id)
#         elif hasattr(request, "user") and request.user.is_authenticated:
#             log_file = os.path.join(self.logs_dir, f"authuser_{request.user.id}.log")
#             user_key = f"authuser_{request.user.id}"
#         else:
#             log_file = os.path.join(self.logs_dir, "anonymous.log")
#             user_key = "anonymous"

#         # ------------------------------
#         # Logger setup
#         # ------------------------------
#         logger = logging.getLogger(f"user_logger_{user_key}")
#         logger.setLevel(logging.INFO)
#         if not logger.handlers:
#             handler = logging.FileHandler(log_file)
#             formatter = logging.Formatter("%(asctime)s - %(message)s")
#             handler.setFormatter(formatter)
#             logger.addHandler(handler)

#         # ------------------------------
#         # Log request info
#         # ------------------------------
#         logger.info("=============Start=============\n")
#         logger.info(
#             f"[REQUEST] Path: {request.path}, Method: {request.method}, "
#             f"Duration: {duration:.5f}s, Query Time: {total_query_time:.5f}s, "
#             f"Executed Queries: {len(executed_queries)}"
#         )

#         # ------------------------------
#         # Log individual executed queries
#         # ------------------------------
#         for i, q in enumerate(executed_queries, start=1):
#             sql = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")
#             q_time = float(q.get("time", 0))
#             logger.info(f"[QUERY {i}] Time: {q_time:.5f}s\n{sql}\n")

#         # ------------------------------
#         # Update per-user stats
#         # ------------------------------
#         if user_key not in user_stats:
#             user_stats[user_key] = {
#                 "total_requests": 0,
#                 "total_queries": 0,
#                 "total_query_time": 0.0,
#                 "slowest_request": 0.0,
#                 "longest_request": 0.0,
#                 "slowest_query_time": 0.0,
#                 "slowest_query_sql": "",
#                 "longest_query_time": 0.0,
#                 "longest_query_sql": ""
#             }

#         stats = user_stats[user_key]
#         stats["total_requests"] += 1
#         stats["total_queries"] += len(executed_queries)
#         stats["total_query_time"] += total_query_time
#         stats["slowest_request"] = max(stats["slowest_request"], duration)
#         stats["longest_request"] = max(stats["longest_request"], duration)

#         # Track longest/slowest executed queries
#         for q in executed_queries:
#             q_time = float(q.get("time", 0))
#             sql = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")

#             if q_time > stats["longest_query_time"]:
#                 stats["longest_query_time"] = q_time
#                 stats["longest_query_sql"] = sql

#             if q_time > stats["slowest_query_time"]:
#                 stats["slowest_query_time"] = q_time
#                 stats["slowest_query_sql"] = sql

#         avg_request_duration = stats["total_query_time"] / stats["total_requests"] if stats["total_requests"] > 0 else 0

#         # ------------------------------
#         # Log summary per user
#         # ------------------------------
#         logger.info("\n====== USER SUMMARY ======")
#         logger.info(f"Total Requests: {stats['total_requests']}")
#         logger.info(f"Executed Queries: {stats['total_queries']}")
#         logger.info(f"Total Query Time: {stats['total_query_time']:.5f}s")
#         logger.info(f"Avg Request Duration: {avg_request_duration:.5f}s")
#         logger.info(f"Slowest Request Duration: {stats['slowest_request']:.5f}s")
#         logger.info(f"Longest Request Duration: {stats['longest_request']:.5f}s")
#         logger.info(f"Longest Query Duration: {stats['longest_query_time']:.5f}s")
#         if stats["longest_query_sql"]:
#             logger.info("Longest Query SQL:\n" + stats["longest_query_sql"])
#         logger.info(f"Slowest Query Duration: {stats['slowest_query_time']:.5f}s")
#         if stats["slowest_query_sql"]:
#             logger.info("Slowest Query SQL:\n" + stats["slowest_query_sql"])
#         logger.info("=============End=============\n")

#         return response



# import os
# import time
# import logging
# import sqlparse
# from django.db import connection
# from django.conf import settings

# # In-memory per-user stats
# user_stats = {}

# class UserRequestLoggingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.logs_dir = os.path.join(settings.BASE_DIR, "users_logs")
#         os.makedirs(self.logs_dir, exist_ok=True)
#         print(f"[Middleware Init] Logs directory created at: {self.logs_dir}")

#     def __call__(self, request):
#         start_time = time.time()
#         connection.queries.clear()

#         response = self.get_response(request)

#         end_time = time.time()
#         duration = end_time - start_time

#         # Queries executed only for this request
#         executed_queries = [q for q in connection.queries if float(q.get("time", 0)) > 0]
#         request_query_count = len(executed_queries)
#         total_query_time = sum(float(q.get("time", 0)) for q in executed_queries)

#         # ------------------------------
#         # Determine user identity
#         # ------------------------------
#         user_id = request.session.get("user_id")
#         if user_id:
#             log_file = os.path.join(self.logs_dir, f"user_{user_id}.log")
#             user_key = str(user_id)
#         elif hasattr(request, "user") and request.user.is_authenticated:
#             log_file = os.path.join(self.logs_dir, f"authuser_{request.user.id}.log")
#             user_key = f"authuser_{request.user.id}"
#         else:
#             log_file = os.path.join(self.logs_dir, "anonymous.log")
#             user_key = "anonymous"

#         # ------------------------------
#         # Logger setup
#         # ------------------------------
#         logger = logging.getLogger(f"user_logger_{user_key}")
#         logger.setLevel(logging.INFO)
#         if not logger.handlers:
#             handler = logging.FileHandler(log_file)
#             formatter = logging.Formatter("%(asctime)s - %(message)s")
#             handler.setFormatter(formatter)
#             logger.addHandler(handler)

#         # ------------------------------
#         # Log request info
#         # ------------------------------
#         logger.info("=============Start=============\n")
#         logger.info(
#             f"[REQUEST] Path: {request.path}, Method: {request.method}, "
#             f"Duration: {duration:.5f}s, Query Time: {total_query_time:.5f}s, "
#             f"Executed Queries: {request_query_count}"
#         )

#         # ------------------------------
#         # Log individual executed queries
#         # ------------------------------
#         for i, q in enumerate(executed_queries, start=1):
#             sql = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")
#             q_time = float(q.get("time", 0))
#             logger.info(f"[QUERY {i}] Time: {q_time:.5f}s\n{sql}\n")

#         # ------------------------------
#         # Update cumulative per-user stats
#         # ------------------------------
#         if user_key not in user_stats:
#             user_stats[user_key] = {
#                 "total_requests": 0,
#                 "total_query_time": 0.0,
#                 "slowest_request": 0.0,
#                 "longest_request": 0.0,
#                 "slowest_query_time": 0.0,
#                 "slowest_query_sql": "",
#                 "longest_query_time": 0.0,
#                 "longest_query_sql": ""
#             }

#         stats = user_stats[user_key]
#         stats["total_requests"] += 1
#         stats["total_query_time"] += total_query_time
#         stats["slowest_request"] = max(stats["slowest_request"], duration)
#         stats["longest_request"] = max(stats["longest_request"], duration)

#         # Track longest/slowest queries across all requests
#         for q in executed_queries:
#             q_time = float(q.get("time", 0))
#             sql = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")
#             if q_time > stats["longest_query_time"]:
#                 stats["longest_query_time"] = q_time
#                 stats["longest_query_sql"] = sql
#             if q_time > stats["slowest_query_time"]:
#                 stats["slowest_query_time"] = q_time
#                 stats["slowest_query_sql"] = sql

#         avg_request_duration = stats["total_query_time"] / stats["total_requests"]

#         # ------------------------------
#         # Log summary per request
#         # ------------------------------
#         logger.info("\n====== REQUEST SUMMARY ======")
#         logger.info(f"Executed Queries (this request): {request_query_count}")
#         logger.info(f"Request Duration: {duration:.5f}s")
#         logger.info(f"Total Query Time: {total_query_time:.5f}s")
#         # if executed_queries:
#         #     logger.info(f"Longest Query Duration (this request): {max(float(q.get('time',0)) for q in executed_queries):.5f}s")
#         #     # logger.info(f"Slowest Query Duration (this request): {min(float(q.get('time',0)) for q in executed_queries):.5f}s")
#         # if stats["longest_query_sql"]:
#         #     logger.info("Longest Query SQL:\n" + stats["longest_query_sql"])
#         #     logger.info(f"Slowest Query Duration (this request): {min(float(q.get('time',0)) for q in executed_queries):.5f}s")
#         #     # logger.info(f"Slowest Query Duration: {stats['slowest_query_time']:.5f}s")
#         # if stats["slowest_query_sql"]:
#         #     logger.info("Slowest Query SQL:\n" + stats["slowest_query_sql"])

#         if executed_queries:
#             longest_query_time = max(float(q.get('time', 0)) for q in executed_queries)
#             slowest_query_time = min(float(q.get('time', 0)) for q in executed_queries)

#             logger.info(f"Longest Query Duration (this request): {longest_query_time:.5f}s")
#             logger.info("Longest Query SQL:\n" + stats["longest_query_sql"])

#             logger.info(f"Slowest Query Duration (this request): {slowest_query_time:.5f}s")
#             logger.info("Slowest Query SQL:\n" + stats["slowest_query_sql"])

#         logger.info("=============End=============\n")

#         return response




# import os
# import time
# import logging
# import sqlparse
# from logging.handlers import RotatingFileHandler
# from django.db import connection
# from django.conf import settings

# # In-memory per-user stats
# user_stats = {}

# class UserRequestLoggingMiddleware:
#     """
#     Logs request duration, executed queries, and per-user stats.
#     Stores logs per user in users_logs/ folder.
#     """

#     def __init__(self, get_response):
#         self.get_response = get_response

#         # Absolute path outside project recommended for server
#         self.logs_dir = os.path.join(settings.BASE_DIR, "users_logs")
#         os.makedirs(self.logs_dir, exist_ok=True)
#         print(f"[Middleware Init] Logs directory: {self.logs_dir}")

#     def __call__(self, request):
#         start_time = time.time()
#         connection.queries.clear()

#         response = self.get_response(request)

#         end_time = time.time()
#         duration = end_time - start_time

#         # Only executed queries (time > 0)
#         executed_queries = [q for q in connection.queries if float(q.get("time", 0)) > 0]
#         request_query_count = len(executed_queries)
#         total_query_time = sum(float(q.get("time", 0)) for q in executed_queries)

#         # -------------------
#         # Identify user
#         # -------------------
#         user_id = getattr(request.user, "id", None)
#         if hasattr(request, "session") and request.session.get("user_id"):
#             user_id = request.session.get("user_id")

#         if user_id:
#             log_file = os.path.join(self.logs_dir, f"user_{user_id}.log")
#             user_key = str(user_id)
#         elif hasattr(request, "user") and request.user.is_authenticated:
#             log_file = os.path.join(self.logs_dir, f"authuser_{request.user.id}.log")
#             user_key = f"authuser_{request.user.id}"
#         else:
#             log_file = os.path.join(self.logs_dir, "anonymous.log")
#             user_key = "anonymous"

#         # -------------------
#         # Logger setup
#         # -------------------
#         logger = logging.getLogger(f"user_logger_{user_key}")
#         logger.setLevel(logging.INFO)

#         if not any(isinstance(h, RotatingFileHandler) and h.baseFilename == log_file
#                    for h in logger.handlers):
#             handler = RotatingFileHandler(
#                 log_file, maxBytes=10*1024*1024, backupCount=3, encoding='utf-8'
#             )
#             formatter = logging.Formatter("%(asctime)s - %(message)s")
#             handler.setFormatter(formatter)
#             logger.addHandler(handler)

#         # -------------------
#         # Log request start
#         # -------------------
#         logger.info("=============Start=============")
#         logger.info(f"[REQUEST START] Path: {request.path}, Method: {request.method}")
#         logger.info(f"Duration: {duration:.5f}s, Query Time: {total_query_time:.5f}s, Executed Queries: {request_query_count}")

#         # -------------------
#         # Log executed queries
#         # -------------------
#         for i, q in enumerate(executed_queries, start=1):
#             sql = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")
#             q_time = float(q.get("time", 0))
#             logger.info(f"[QUERY {i}] Time: {q_time:.5f}s\n{sql}\n")

#         # -------------------
#         # Update per-user stats
#         # -------------------
#         if user_key not in user_stats:
#             user_stats[user_key] = {
#                 "total_requests": 0,
#                 "total_query_time": 0.0,
#                 "slowest_request": 0.0,
#                 "longest_request": 0.0,
#                 "slowest_query_time": 0.0,
#                 "slowest_query_sql": "",
#                 "longest_query_time": 0.0,
#                 "longest_query_sql": ""
#             }

#         stats = user_stats[user_key]
#         stats["total_requests"] += 1
#         stats["total_query_time"] += total_query_time
#         stats["slowest_request"] = max(stats["slowest_request"], duration)
#         stats["longest_request"] = max(stats["longest_request"], duration)

#         for q in executed_queries:
#             q_time = float(q.get("time", 0))
#             sql = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")

#             # Track longest query
#             if q_time > stats["longest_query_time"]:
#                 stats["longest_query_time"] = q_time
#                 stats["longest_query_sql"] = sql

#             # Track slowest query
#             if q_time > stats["slowest_query_time"]:
#                 stats["slowest_query_time"] = q_time
#                 stats["slowest_query_sql"] = sql

#         avg_request_duration = stats["total_query_time"] / stats["total_requests"]

#         # -------------------
#         # Log request summary
#         # -------------------
#         logger.info("====== REQUEST SUMMARY ======")
#         logger.info(f"Executed Queries (this request): {request_query_count}")
#         logger.info(f"Request Duration: {duration:.5f}s")
#         logger.info(f"Total Query Time: {total_query_time:.5f}s")

#         if executed_queries:
#             longest_query_time = max(float(q.get('time', 0)) for q in executed_queries)
#             slowest_query_time = min(float(q.get('time', 0)) for q in executed_queries)

#             logger.info(f"Longest Query Duration (this request): {longest_query_time:.5f}s")
#             logger.info("Longest Query SQL:\n" + stats["longest_query_sql"])

#             logger.info(f"Slowest Query Duration (this request): {slowest_query_time:.5f}s")
#             logger.info("Slowest Query SQL:\n" + stats["slowest_query_sql"])

#         logger.info("=============End=============\n")

#         return response

# import os
# import time
# import logging
# import sqlparse
# import re
# from django.db import connection
# from django.conf import settings

# # In-memory per-user stats
# user_stats = {}

# class UserRequestLoggingMiddleware:
#     """
#     Middleware to log per-request and cumulative per-user SQL execution details.
#     Filters out trivial SQL statements (BEGIN, COMMIT, ROLLBACK, SAVEPOINT, RELEASE).
#     """

#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.logs_dir = os.path.join(settings.BASE_DIR, "users_logs")
#         os.makedirs(self.logs_dir, exist_ok=True)
#         print(f"[Middleware Init] Logs directory created at: {self.logs_dir}")

#         # Pattern to ignore trivial SQL queries
#         self.skip_pattern = re.compile(r"^(BEGIN|COMMIT|ROLLBACK|SAVEPOINT|RELEASE)", re.I)

#     def __call__(self, request):
#         start_time = time.time()
#         connection.queries.clear()

#         response = self.get_response(request)

#         end_time = time.time()
#         duration = end_time - start_time

#         # ------------------------------
#         # Filter executed queries (ignore trivial ones)
#         # ------------------------------
#         executed_queries = [
#             q for q in connection.queries
#             if float(q.get("time", 0)) > 0 and not self.skip_pattern.match(q.get("sql", ""))
#         ]
#         request_query_count = len(executed_queries)
#         total_query_time = sum(float(q.get("time", 0)) for q in executed_queries)

#         # ------------------------------
#         # Determine user identity
#         # ------------------------------
#         user_id = request.session.get("user_id")
#         if user_id:
#             log_file = os.path.join(self.logs_dir, f"user_{user_id}.log")
#             user_key = str(user_id)
#         elif hasattr(request, "user") and request.user.is_authenticated:
#             log_file = os.path.join(self.logs_dir, f"authuser_{request.user.id}.log")
#             user_key = f"authuser_{request.user.id}"
#         else:
#             log_file = os.path.join(self.logs_dir, "anonymous.log")
#             user_key = "anonymous"

#         # ------------------------------
#         # Logger setup
#         # ------------------------------
#         logger = logging.getLogger(f"user_logger_{user_key}")
#         logger.setLevel(logging.INFO)
#         if not logger.handlers:
#             handler = logging.FileHandler(log_file)
#             formatter = logging.Formatter("%(asctime)s - %(message)s")
#             handler.setFormatter(formatter)
#             logger.addHandler(handler)

#         # ------------------------------
#         # Log request info
#         # ------------------------------
#         logger.info("=============Start=============\n")
#         logger.info(
#             f"[REQUEST] Path: {request.path}, Method: {request.method}, "
#             f"Duration: {duration:.5f}s, Query Time: {total_query_time:.5f}s, "
#             f"Executed Queries: {request_query_count}"
#         )

#         # ------------------------------
#         # Log individual executed queries
#         # ------------------------------
#         for i, q in enumerate(executed_queries, start=1):
#             sql = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")
#             q_time = float(q.get("time", 0))
#             logger.info(f"[QUERY {i}] Time: {q_time:.5f}s\n{sql}\n")

#         # ------------------------------
#         # Update cumulative per-user stats
#         # ------------------------------
#         if user_key not in user_stats:
#             user_stats[user_key] = {
#                 "total_requests": 0,
#                 "total_query_time": 0.0,
#                 "slowest_request": 0.0,
#                 "longest_request": 0.0,
#                 "slowest_query_time": 0.0,
#                 "slowest_query_sql": "",
#                 "longest_query_time": 0.0,
#                 "longest_query_sql": ""
#             }

#         stats = user_stats[user_key]
#         stats["total_requests"] += 1
#         stats["total_query_time"] += total_query_time
#         stats["slowest_request"] = max(stats["slowest_request"], duration)
#         stats["longest_request"] = max(stats["longest_request"], duration)

#         # Track longest/slowest queries across all requests
#         for q in executed_queries:
#             q_time = float(q.get("time", 0))
#             sql = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")
#             if q_time > stats["longest_query_time"]:
#                 stats["longest_query_time"] = q_time
#                 stats["longest_query_sql"] = sql
#             if q_time > stats["slowest_query_time"]:
#                 stats["slowest_query_time"] = q_time
#                 stats["slowest_query_sql"] = sql

#         avg_request_duration = stats["total_query_time"] / stats["total_requests"]

#         # ------------------------------
#         # Log summary per request
#         # ------------------------------
#         logger.info("\n====== REQUEST SUMMARY ======")
#         logger.info(f"Executed Queries (this request): {request_query_count}")
#         logger.info(f"Request Duration: {duration:.5f}s")
#         logger.info(f"Total Query Time: {total_query_time:.5f}s")

#         if executed_queries:
#             longest_query_time = max(float(q.get('time', 0)) for q in executed_queries)
#             slowest_query_time = min(float(q.get('time', 0)) for q in executed_queries)

#             logger.info(f"Longest Query Duration (this request): {longest_query_time:.5f}s")
#             logger.info("Longest Query SQL:\n" + stats["longest_query_sql"])

#             logger.info(f"Slowest Query Duration (this request): {slowest_query_time:.5f}s")
#             logger.info("Slowest Query SQL:\n" + stats["slowest_query_sql"])

#         logger.info("=============End=============\n")

#         return response


import os
import time
import logging
import sqlparse
from logging.handlers import RotatingFileHandler
from django.db import connection
from django.conf import settings

# In-memory per-user stats
user_stats = {}

class UserRequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logs_dir = os.path.join(settings.BASE_DIR, "users_logs")
        os.makedirs(self.logs_dir, exist_ok=True)
        print(f"[Middleware Init] Logs directory created at: {self.logs_dir}")

    def __call__(self, request):
        start_time = time.time()
        connection.queries.clear()

        response = self.get_response(request)

        end_time = time.time()
        duration = end_time - start_time

        # Queries executed only for this request
        executed_queries = [q for q in connection.queries if float(q.get("time", 0)) > 0]
        request_query_count = len(executed_queries)
        total_query_time = sum(float(q.get("time", 0)) for q in executed_queries)

        # ------------------------------
        # Determine user identity
        # ------------------------------
        user_id = request.session.get("user_id")
        if user_id:
            log_file = os.path.join(self.logs_dir, f"user_{user_id}.log")
            user_key = str(user_id)
        elif hasattr(request, "user") and request.user.is_authenticated:
            log_file = os.path.join(self.logs_dir, f"authuser_{request.user.id}.log")
            user_key = f"authuser_{request.user.id}"
        else:
            log_file = os.path.join(self.logs_dir, "anonymous.log")
            user_key = "anonymous"

        # ------------------------------
        # Logger setup using RotatingFileHandler
        # ------------------------------
        logger = logging.getLogger(f"user_logger_{user_key}")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = RotatingFileHandler(
                log_file,
                mode='a',
                maxBytes=5 * 1024 * 1024,  # 5 MB
                backupCount=3,  # keep 3 old files
                encoding='utf-8'
            )
            formatter = logging.Formatter("%(asctime)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.propagate = False  # prevent duplicate logs

        # ------------------------------
        # Log request info
        # ------------------------------
        logger.info("=============Start=============\n")
        logger.info(
            f"[REQUEST] Path: {request.path}, Method: {request.method}, "
            f"Duration: {duration:.5f}s, Query Time: {total_query_time:.5f}s, "
            f"Executed Queries: {request_query_count}"
        )

        # ------------------------------
        # Log individual executed queries
        # ------------------------------
        for i, q in enumerate(executed_queries, start=1):
            sql = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")
            q_time = float(q.get("time", 0))
            logger.info(f"[QUERY {i}] Time: {q_time:.5f}s\n{sql}\n")

        # ------------------------------
        # Update cumulative per-user stats
        # ------------------------------
        if user_key not in user_stats:
            user_stats[user_key] = {
                "total_requests": 0,
                "total_query_time": 0.0,
                "slowest_request": 0.0,
                "longest_request": 0.0,
                "slowest_query_time": 0.0,
                "slowest_query_sql": "",
                "longest_query_time": 0.0,
                "longest_query_sql": ""
            }

        stats = user_stats[user_key]
        stats["total_requests"] += 1
        stats["total_query_time"] += total_query_time
        stats["slowest_request"] = max(stats["slowest_request"], duration)
        stats["longest_request"] = max(stats["longest_request"], duration)

        # Track longest/slowest queries across all requests
        for q in executed_queries:
            q_time = float(q.get("time", 0))
            sql = sqlparse.format(q.get("sql"), reindent=True, keyword_case="upper")
            if q_time > stats["longest_query_time"]:
                stats["longest_query_time"] = q_time
                stats["longest_query_sql"] = sql
            if q_time > stats["slowest_query_time"]:
                stats["slowest_query_time"] = q_time
                stats["slowest_query_sql"] = sql

        avg_request_duration = stats["total_query_time"] / stats["total_requests"]

        # ------------------------------
        # Log summary per request
        # ------------------------------
        logger.info("\n====== REQUEST SUMMARY ======")
        logger.info(f"Executed Queries (this request): {request_query_count}")
        logger.info(f"Request Duration: {duration:.5f}s")
        logger.info(f"Total Query Time: {total_query_time:.5f}s")

        if executed_queries:
            longest_query_time = max(float(q.get('time', 0)) for q in executed_queries)
            slowest_query_time = min(float(q.get('time', 0)) for q in executed_queries)

            # Find the actual SQL corresponding to longest and slowest queries in this request
            longest_query_sql = max(executed_queries, key=lambda x: float(x.get('time',0))).get('sql')
            slowest_query_sql = min(executed_queries, key=lambda x: float(x.get('time',0))).get('sql')

            logger.info(f"Longest Query Duration (this request): {longest_query_time:.5f}s")
            logger.info("Longest Query SQL:\n" + sqlparse.format(longest_query_sql, reindent=True, keyword_case="upper"))

            logger.info(f"Slowest Query Duration (this request): {slowest_query_time:.5f}s")
            logger.info("Slowest Query SQL:\n" + sqlparse.format(slowest_query_sql, reindent=True, keyword_case="upper"))

        logger.info("=============End=============\n")

        return response
