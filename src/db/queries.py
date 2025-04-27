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
        title = job.get('title')
        company = job.get('company')
        description = job.get('DESCRIPTION', [])
        cursor.execute(
            """
                INSERT INTO WWR (title, company) VALUES (%s, %s)
                RETURNING id;
                """,
            (title, company)
        )
        description_id = cursor.fetchone()[0]
        for des in description:
            cursor.execute(
                """
                    INSERT INTO DESCRIPTIONS (description_id, description) VALUES (%s, %s)
                    """,

                (description_id, des)
            )

    connection.commit()
