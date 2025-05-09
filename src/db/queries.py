from db.connection import connect_db


connection = connect_db()
cursor = connection.cursor()

"""
TABLE FOR WE WORK REMOTELY
"""

# if connection:
#     cursor.execute(
#         """
#             CREATE TABLE WWR(
#             id SERIAL PRIMARY KEY,
#             title VARCHAR(100),
#             company VARCHAR(100)
#             )
#             """
#     )
#
#     cursor.execute(
#         """
#             CREATE TABLE DESCRIPTIONS(
#             description VARCHAR(255),
#             description_id INT,
#             FOREIGN KEY (description_id) REFERENCES WWR(id) ON DELETE CASCADE
#
#             )
#             """
#     )
#     connection.commit()
#     connection.close()
#     cursor.close()
#     print('TABLE CREATED SUCCESSFULLY!!!')


"""
TABLE FOR REMOTE OK
"""

# if connection:
#     cursor.execute(
#             """
#             CREATE TABLE REMOTEOK(
#             id SERIAL PRIMARY KEY,
#             company VARCHAR(100),
#             position VARCHAR(200),
#             location VARCHAR(100),
#             max_salary INT,
#             min_salary INT
#
#             )
#             """
#             )
#     cursor.execute(
#             """
#             CREATE TABLE TAGS(
#             tag VARCHAR(100),
#             tag_id INT,
#             FOREIGN KEY (tag_id) REFERENCES REMOTEOK(id) ON DELETE CASCADE
#             )
#             """
#             )
#     connection.commit()
#     connection.close()
#     cursor.close()
#     print("TABLE CREATED FOR REMOTE OK")

"""
TABLE FOR REMOTECO
"""
# if connection:
#     cursor.execute(
#         """
#         CREATE TABLE REMOTECO(
#             id SERIAL PRIMARY KEY,
#             title VARCHAR(100),
#             company VARCHAR(100),
#             apply_link VARCHAR(250)
#         )
#         """
#     )
#     cursor.execute(
#         """
#         CREATE TABLE COTAGS(
#             tag VARCHAR(100),
#             tag_id INT,
#             FOREIGN KEY (tag_id) REFERENCES REMOTECO(id) ON DELETE CASCADE
#         )
#         """
#     )
#     connection.commit()
#     cursor.close()
#     connection.close()
#     print("TABLE CREATED FOR REMOTE CO")


def add_to_remote_co(job_lists):
    for job in job_lists:
        title = job.get("role", "")
        company = job.get("company", "")
        apply_link = job.get("apply_link", "")
        tags = job.get("tags", [])
        cursor.execute(
            """
            INSERT INTO REMOTECO (title, company, apply_link) VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (title, company, apply_link),
        )
        tag_id = cursor.fetchone()[0]
        for tag in tags:
            cursor.execute(
                """
                INSERT INTO COTAGS (tag_id, tag) VALUES (%s, %s)
                """,
                (tag_id, tag),
            )
    print("SUCCESSFULLY ADDED TO THE TABLE REMOTECO")
    connection.commit()


def add_to_wwr(job_lists):
    """
    format of job_lists: [
    {
    'description': [],
    'title' : val,
    'company: val'
    }
    ]
    """

    for job in job_lists:
        title = job.get("title")
        company = job.get("company")
        description = job.get("DESCRIPTION", [])
        cursor.execute(
            """
                INSERT INTO WWR (title, company) VALUES (%s, %s)
                RETURNING id;
                """,
            (title, company),
        )
        description_id = cursor.fetchone()[0]
        for des in description:
            cursor.execute(
                """
                    INSERT INTO DESCRIPTIONS (description_id, description) VALUES (%s, %s)
                    """,
                (description_id, des),
            )

    connection.commit()


def add_to_remoteok(job_lists):
    for job in job_lists:
        location = job.get("location")
        company = job.get("company")
        position = job.get("position")
        max_salary = job.get("salary_max")
        min_salary = job.get("salary_min")
        tags = job.get("tags", [])
        cursor.execute(
            """
                INSERT INTO  REMOTEOK (company, position,location, max_salary, min_salary) VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
            (company, position, location, max_salary, min_salary),
        )
        tag_id = cursor.fetchone()[0]
        for tag in tags:
            cursor.execute(
                """
                    INSERT INTO TAGS(tag_id, tag) VALUES (%s, %s)
                    """,
                (tag_id, tag),
            )

    print("DATA ADDED SUCCESSFULLY!!!")
    connection.commit()
