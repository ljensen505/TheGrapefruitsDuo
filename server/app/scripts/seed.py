from datetime import datetime

from dotenv import load_dotenv

from app.db.conn import connect_db
from app.models.event import EVENT_TABLE, SERIES_TABLE, Event, EventSeries
from app.models.group import GROUP_TABLE, Group
from app.models.musician import MUSICIAN_TABLE, NewMusician
from app.models.user import USER_TABLE, User

margarite: NewMusician = NewMusician(
    name="Margarite Waddell",
    bio="French hornist Margarite Waddell holds positions with the Eugene Symphony, Sarasota Opera, Boise Philharmonic, Rogue Valley Symphony, and Newport Symphony. As a freelancer, Margarite has played with ensembles throughout the West Coast including the Oregon Symphony, Portland Opera, Santa Rosa Symphony, Marin Symphony, and Symphony San Jose. She has performed with popular artists such as The Who, Josh Groban, and Sarah Brightman. Margarite can be heard on Kamyar Mohajer’s album “Pictures of the Hidden” on Navona Records. She appeared as a soloist with the Silicon Valley Philharmonic in 2016. Margarite cares deeply about music education and has taught private lessons, sectionals, and masterclasses throughout the Bay Area, Southwestern Oregon, Eugene, and Corvallis since 2013. She also performed in the San Francisco Symphony's Adventures in Music program for the 2016-2017 season. Margarite received her bachelor’s degree from the University of Oregon, and her master’s degree from the San Francisco Conservatory of Music.",
    headshot_id="zlpkcrvbdsicgj7qtslx",
)

coco: NewMusician = NewMusician(
    name="Coco Bender",
    bio="Coco Bender is a pianist residing in the Pacific Northwest. She recently performed with Cascadia Composers, recorded original film scores by Portland composer Christina Rusnak for the Pioneers: First Woman Filmmakers Project, and during the pandemic presented a series of outdoor recitals featuring music by H. Leslie Adams, William Grant Still, Bartok, and others. Coco is a founding member of the Eugene based horn and piano duo, The Grapefruits, as well as a co-artistic director and musical director of an all-women circus, Girl Circus. She has taken master classes with Inna Faliks, Tamara Stefanovich, and Dr. William Chapman Nyaho. Coco currently studies with Dr. Thomas Otten. In addition to performing regularly, she teaches a large studio of students in the Pacific Northwest, from Seattle WA to Eugene OR. Coco was the accompanist for Portland treble choir Aurora Chorus, during their 2021-2022, season under the conductorship of Kathleen Hollingsworth, Margaret Green, Betty Busch, and Joan Szymko.",
    headshot_id="coco_copy_jywbxm",
)

coco_user: User = User(
    name="Coco Bender",
    email="cocobender.piano@gmail.com",
)

margarite_user: User = User(
    name="Margarite Waddell",
    email="mgwaddell@gmail.com",
)

lucas_user: User = User(name="Lucas Jensen", email="lucas.p.jensen10@gmail.com")

tgd_user: User = User(
    name="The Grapefruits Duo",
    email="thegrapefruitsduo@gmail.com",
)

tgd_website: User = User(
    name="The Grapefruits Duo Website", email="grapefruitswebsite@gmail.com"
)


tgd: Group = Group(
    bio="The Grapefruits, comprising of Coco Bender, piano, and Margarite Waddell, french horn, are a contemporary classical music duo. They perform frequently through out the PNW with the goal presenting traditional classical french horn repertoire, new 20th century works, and commissioned works by PNW composers.",
    name="The Grapefruits Duo",
)


series1 = EventSeries(
    name="The Grapefruits Duo Presents: Works for Horn and Piano",
    description="Pieces by Danzi, Gomez, Gounod, Grant, and Rusnak!",
    poster_id="The_Grapefruits_Present_qhng6y",
    events=[
        Event(
            location="Medford, OR",
            time=datetime(2024, 5, 31, 19),
            event_id=0,
        ),
        Event(
            location="First Presbyterian Church Newport",
            time=datetime(2024, 6, 16, 16),
            event_id=0,
            map_url="https://maps.app.goo.gl/hNfN8X5FBZLg8LDF8",  # type: ignore
        ),
        Event(
            location="First Church of Christ, Scientist, Eugene",
            time=datetime(2024, 6, 23, 15),
            event_id=0,
        ),
    ],
    series_id=0,
)

# series2 = EventSeries(
#     name="The Grapefruits Duo Features: Solos for Bass Trombone",
#     description="Pieces by Ewazen, Bozza, and more!",
#     events=[
#         Event(
#             location="Eugene Family YMCA",
#             time=datetime(2024, 7, 1, 17, 30),
#             event_id=0,
#         ),
#         Event(
#             location="Tobi's Crate",
#             time=datetime(2024, 7, 2, 20),
#             event_id=0,
#             ticket_url="http://www.example.com",  # type: ignore
#         ),
#     ],
#     id=0,
# )


def seed():
    confirmation = input(
        "Are you sure you want to seed the database? Data will be lost. [Y/n]: "
    )
    if confirmation.lower() not in ["y", "yes", ""]:
        print("Exiting")
        return
    print("Seeding database")
    add_musicians()
    add_users()
    add_group()
    add_events()


def add_group():
    print("Adding group")
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        f"DROP TABLE IF EXISTS {GROUP_TABLE};",
    )
    cursor.execute(
        f"""
        CREATE TABLE {GROUP_TABLE} (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            bio TEXT NOT NULL,
            PRIMARY KEY (id)
        );
        """
    )
    cursor.execute(
        f"INSERT INTO {GROUP_TABLE} (name, bio) VALUES (%s, %s);",
        (tgd.name, tgd.bio),
    )
    db.commit()
    cursor.close()


def add_users():
    print("Adding users")
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        f"DROP TABLE IF EXISTS {USER_TABLE};",
    )
    cursor.execute(
        f"""
        CREATE TABLE {USER_TABLE} (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            sub VARCHAR(255),
            PRIMARY KEY (id)
        );
        """
    )
    for u in [coco_user, margarite_user, lucas_user, tgd_user, tgd_website]:
        cursor.execute(
            f"INSERT INTO {USER_TABLE} (name, email, sub) VALUES (%s, %s, %s);",
            (u.name, u.email, u.sub),
        )

    db.commit()
    cursor.close()


def add_musicians():
    print("Adding musicians")

    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        f"DROP TABLE IF EXISTS {MUSICIAN_TABLE};",
    )
    cursor.execute(
        f"""
        CREATE TABLE {MUSICIAN_TABLE} (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            bio TEXT NOT NULL,
            headshot_id VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        );
        """
    )
    for m in [margarite, coco]:
        cursor.execute(
            f"INSERT INTO {MUSICIAN_TABLE} (name, bio, headshot_id) VALUES (%s, %s, %s);",
            (m.name, m.bio, m.headshot_id),
        )

    db.commit()
    cursor.close()


def add_events():
    print("Adding events")

    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        f"DROP TABLE IF EXISTS {EVENT_TABLE};",
    )
    cursor.execute(
        f"DROP TABLE IF EXISTS {SERIES_TABLE};",
    )
    cursor.execute(
        f"""
        CREATE TABLE {SERIES_TABLE} (
            series_id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL UNIQUE,
            description TEXT NOT NULL,
            poster_id VARCHAR(255),
            PRIMARY KEY (series_id)
        );
        """
    )
    cursor.execute(
        f"""
        CREATE TABLE {EVENT_TABLE} (
            event_id INT NOT NULL AUTO_INCREMENT,
            series_id INT NOT NULL,
            location VARCHAR(255) NOT NULL,
            time DATETIME NOT NULL,
            ticket_url VARCHAR(255),
            map_url VARCHAR(255),
            PRIMARY KEY (event_id),
            FOREIGN KEY (series_id) REFERENCES {SERIES_TABLE}(series_id) ON DELETE CASCADE
        );
        """
    )

    for series in [series1]:
        cursor.execute(
            f"INSERT INTO {SERIES_TABLE} (name, description, poster_id) VALUES (%s, %s, %s);",
            (
                series.name,
                series.description,
                series.poster_id,
            ),
        )
        series_id = cursor.lastrowid
        if series_id is None:
            raise Exception("Error inserting series: could not get last row id.")
        series.series_id = series_id
        for event in series.events:
            ticket_url = str(event.ticket_url) if event.ticket_url else None
            map_url = str(event.map_url) if event.map_url else None
            cursor.execute(
                f"INSERT INTO {EVENT_TABLE} (series_id, location, time, ticket_url, map_url) VALUES (%s, %s, %s, %s, %s);",
                (
                    series.series_id,
                    event.location,
                    event.time,
                    ticket_url,
                    map_url,
                ),
            )

    db.commit()
    cursor.close()


def main():
    load_dotenv()
    seed()


if __name__ == "__main__":
    main()
