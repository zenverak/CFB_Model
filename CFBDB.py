import sqlite3
import globals
import os

if not os.path.exists('./database/'):
    os.mkdir('./database/')

conn = sqlite3.connect(f'database/{globals.DB}')

def dbs():
    global conn
    c = conn.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS lines(
                   game_id integer PRIMARY KEY,
                   home_team char(40),
                   home_conference char(40),
                   away_team char(40),
                   away_conference char (40),
                   favorite_team char(40),
                   spread char(6),
                   ou char(4),
                   week integer,
                   year integer
        )""")

    c.execute("""CREATE INDEX IF NOT EXISTS lines_hteam on lines(home_team)""")
    c.execute("""CREATE INDEX IF NOT EXISTS lines_ateam on lines(away_team)""")

    c.execute("""CREATE TABLE IF NOT EXISTS polls(
              school char(30),
              conference char(30),
              rank integer,
              first_place_votes integer,
              points integer,
              poll char(30),
              season_type char(10),
              week integer,
              year integer
            )""")

    c.execute("""CREATE UNIQUE INDEX IF NOT EXISTS pollsIDX on polls(school,week,year,poll)""")


    c.execute(""" CREATE TABLE IF NOT EXISTS games(
                game_id integer PRIMARY KEY,
                home_team char(40),
                home_id integer,
                away_team char(40),
                away_id integer,
                week integer,
                year integer,
                home_score integer,
                away_score integer,
                neutral_site char(5),
                home_score_1qt int,
                home_score_2qt int,
                home_score_3qt int,
                home_score_4qt int,
                away_score_1qt int,
                away_score_21t int,
                away_score_3qt int,
                away_score_4qt int,
                venue_id int,
                conf_game char(5),
                season_type char(10)
                )""")


    c.execute("""CREATE INDEX IF NOT EXISTS games_hteam on games(home_team)""")
    c.execute("""CREATE INDEX IF NOT EXISTS games_ateam on games(away_team)""")
    
    c.execute(""" CREATE TABLE IF NOT EXISTS game_stats(
                game_id integer,
                team char(25),
                rush_yards integer,
                rush_attempt integer,
                pass_yards integer,
                pass_attempts integer,
                completions integer,
                def_td integer,
                pass_td integer,
                rush_td integer,
                kick_points integer,
                sacks integer,
                tfls integer,
                qb_hurries integer,
                pentalties integer,
                pen_yards integer,
                fumbles_lost integer,
                total_fumbles integer,
                fumbles_recovered integer,
                ints_throw integer,
                passes_inter integer,
                punt_return_yds integer,
                punt_returns integer,
                punt_rtn_td integer,
                year integer,
                week integer
                )""")


    c.execute("""CREATE UNIQUE INDEX IF NOT EXISTS statsIDX on game_stats(game_id,team)""")

    c.execute("""CREATE TABLE IF NOT EXISTS teams(
                 team_id integer PRIMARY KEY,
                 team char(30),
                 conference char(20),
                 mascot char(30),
                 stadium_name char(30),
                 stadium_year integer,
                 stadium_lat char(10),
                 stadium_long char(10),
                 stadium_id integer,
                 stadium_capacity integer,
                 grass char(5),
                 dome char(5),
                 state char(2),
                 city char(30)
                ) """)

    conn.commit()

##CLEAN ALL###

def drop_all():
    global conn
    c = conn.cursor()
    tables = ['teams', 'games','game_stats','lines']
    for table in tables:
        c.execute(f"drop table {table}")
    conn.commit()

##TEAMS TABLE########
def insert_teams(data):
    global conn
    c = conn.cursor()
    c.executemany("INSERT OR IGNORE INTO teams values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",data)
    conn.commit()


def get_team_names():
    global conn
    c = conn.cursor()
    c.execute("select team from teams")
    return c.fetchall()


def get_team_data(team):
    global conn
    c = conn.cursor()
    c.execute(f"select * from teams where team = {team}")
    return c.fetchall()[0]


def get_all_teams():
    global conn
    c = conn.cursor()
    c.execute("select * from teams")
    return c.fetchall()


##LINES TABLE###########

def insert_lines(lines):
    global conn
    c = conn.cursor()
    c.executemany('INSERT OR IGNORE INTO lines VALUES(?,?,?,?,?,?,?,?,?,?);',lines)
    conn.commit()


def week_in_lines(week):
    global conn
    c = conn.cursor()
    c.execute(f"select count(*) from lines where week={week} and year={globals.YEAR}")
    rows = c.fetchall()[0][0]
    return rows

def get_line(id_):
    global conn
    c = conn.cursor()
    c.execute(f"select * from lines where id={id_}")
    data = c.fetchall()[0]
    return data


###GAME STATS TABLE######
def insert_game_stats(data):
    global conn
    c = conn.cursor()
    c.executemany("""INSERT or ignore INTO game_stats VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(data))
    conn.commit()


def get_game_stats_ids():
    global conn
    c = conn.cursor()
    c.execute(""" select id from game_stats """)
    return c.fetchall()


def is_id_in_game_stats(id_):
    global conn
    c = conn.cursor()
    c.execute(f"select count(*) from game_stats where id={id_}")
    return c.fetchall()[0][0]


def count_game_stats():
    global conn
    c = conn.cursor()
    c.execute("select count(*) from game_stats")
    return c.fetchall()[0][0]


def get_stats_by_team_in_year(team, year):
    global conn
    c = conn.cursor()
    c.execute(f"select * from game_stats where team='{team}' and year={year}")
    return c.fetchall()


def get_stats_by_team_year_week(team, year, week):
    global conn
    c = conn.cursor()
    c.execute(f"select * from game_stats where team='{team}' and year={year} and week={week}")
    return c.fetchall()


def get_defensive_scores_team_year(team,year):
    pass
    


##games Table#######
def insert_games(data):
    global conn
    c = conn.cursor()
    c.executemany("INSERT OR IGNORE INTO games values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",data)
    conn.commit()


def get_games_for_team_in_year(team, year):
    global conn
    c = conn.cursor()
    c.execute(f"select * from games where (home_team='{team}' or away_team='{team}') and year={year}")
    return c.fetchall()


def get_game_for_team_alltime(team):
    global conn
    c = conn.cursor()
    c.execute(f"select * from games where home_team='{team}' or away_team='{team}'")
    return c.fetchall()


def get_games_for_week_and_year(week, year):
    global conn
    c = conn.cursor()
    c.execute(f"select * from games where week={week} and year={year}")
    return c.fetchall()


def get_mov(team,year):
    global conn
    c = conn.cursor()
    c.execute(f"select sum(case home_team when '{team}' then home_score - away_score else  \
                away_score - home_score END) from games where year={year} and (home_team='{team}' or away_team='{team}')")
    return c.fetchall()[0][0]

def get_points_scored(team, year):
    global conn
    c = conn.cursor()
    c.execute(f"select sum(case home_team when '{team}' then home_score else away_score END) \
                from games where year={year} and (home_team='{team}' or away_team='{team}')")
    return c.fetchall()[0][0]

def get_points_given_up(team, year):
    global conn
    c = conn.cursor()
    c.execute(f"select sum(case home_team when '{team}' then away_score else home_score END) \
                    from games where year={year} and (home_team='{team}' or away_team='{team}')")
    return c.fetchall()[0][0]

####POLLS######

def insert_into_polls(data):
    global conn
    c = conn.cursor()
    c.executemany("INSERT OR IGNORE INTO polls VALUES(?,?,?,?,?,?,?,?,?)",data)
    conn.commit()


def get_all_rankings_for_team(team):
    global conn
    c = conn.cursor()
    c.execute(f"select * from polls where school='{team}'" )
    return c.fetchall()

def get_all_rankings_for_team_with_poll(team,poll):
    global conn
    c = conn.cursor()
    c.execute(f"select * from polls where school='{team}' and poll='{poll}'" )
    return c.fetchall()

def get_all_rankings_poll(poll):
    global conn
    c = conn.cursor()
    c.execute(f"select * from polls where poll='{poll}'" )
    return c.fetchall()    

def get_poll_year(year, poll):
    global conn
    c = conn.cursor()
    c.execute(f"select * from poll whre year={year} and poll='{poll}'")
    return c.fetchall()

def get_all_poll():
    global conn
    c = conn.cursor()
    c.execute("select count(*) as total, school, rank, poll from polls group by poll, rank, school")
    return c.fetchall()


if __name__ == "__main__":
    t = get_all_rankings_for_team_with_poll('Tulane','AP Top 25')
    
