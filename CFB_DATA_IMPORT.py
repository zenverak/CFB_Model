import cfbd
import CFBDB as cbd
import math
import globals


config = cfbd.Configuration()
config.api_key['Authorization'] = globals.KEY
config.api_key_prefix['Authorization'] = 'Bearer'
apic = cfbd.ApiClient(config)

bet_api = cfbd.BettingApi(apic)
game_api = cfbd.GamesApi(apic)
team_api = cfbd.TeamsApi(apic)
rank_api = cfbd.RankingsApi(apic)


####BETTING########
def get_line(game):
        try:
            team1 = game.away_team
            team2 = game.home_team
        except:
            return 'NOPE','',''
        if len(game.lines) > 0:
            line = game.lines[0]
        else:
            return "NOPE", '',''
        f_spread = line['formattedSpread']
        try:
            ou = float(line['overUnder'])
        except:
            ou = 0
        if f_spread.find(team1) > -1 and f_spread.find(team2) > -1:
            spread = f_spread.replace(team1,'').lstrip()
            try:
                float(spread)
                fav_team = team1
            except ValueError:
                spread = f_spread.replace(team2,'').lstrip()
                fav_team = team2
        elif f_spread.find(team1) > -1:
            fav_team = team1
            spread = f_spread.replace(team1,'').lstrip()
        else:
            fav_team = team2
            spread = f_spread.replace(team2,'').lstrip()
        return fav_team, spread, ou


def insert_betting_data(api,only=False):
    lines = api.get_lines(year=globals.YEAR)
    bet_list = []
    for game in lines:
        if not only and game.week <= globals.WEEK:
            fav_team, spread, ou = get_line(game)        
            data = [game.id, game.home_team, game.home_conference, game.away_team, game.away_conference, fav_team, spread, ou, game.week, globals.YEAR]
            bet_list.append(data)
        elif only and game.week == globals.WEEK:
            fav_team, spread, ou = get_line(game)
            data = [game.id, game.home_team, game.home_conference, game.away_team, game.away_conference, fav_team, spread, ou, game.week, globals.YEAR]
            bet_list.append(data)
    cbd.insert_lines(bet_list)


####STATS########

def _split_numbers(number):
    mid = number.find('-')
    return [int(number[0:mid]),int(number[mid+1::])]

def append_stat(stat_name, dict_stats,stat):
    if stat_name in dict_stats:
        stat.append(int(math.floor(float(dict_stats[stat_name]))))
    else:
        stat.append(0)
    return stat
    
def format_stat_list(stat,dict_stats):
    pass_stat = _split_numbers(dict_stats['completionAttempts'])
    pen_stat = _split_numbers(dict_stats['totalPenaltiesYards'])
    
    stat = append_stat('rushingYards',dict_stats,stat)
    stat = append_stat('rushingAttempts',dict_stats,stat)
    stat = append_stat('netPassingYards',dict_stats,stat)
    stat.append(pass_stat[1])
    stat.append(pass_stat[0])
    stat = append_stat('defensiveTDs',dict_stats,stat)
    stat = append_stat('passingTDs',dict_stats,stat)
    stat = append_stat('rushingTDs',dict_stats,stat)
    stat = append_stat('kickingPoints',dict_stats,stat)
    stat = append_stat('sacks',dict_stats,stat)
    stat = append_stat('tacklesForLoss',dict_stats,stat)
    stat = append_stat('qbHurries',dict_stats,stat)
    stat.append(int(pen_stat[0]))
    stat.append(int(pen_stat[1]))
    stat = append_stat('fumblesLost',dict_stats,stat)
    stat = append_stat('totalFumbles',dict_stats,stat)
    stat = append_stat('fumblesRecovered',dict_stats,stat)
    stat = append_stat('interceptions',dict_stats,stat)
    stat = append_stat('passesIntercepted',dict_stats,stat)
    stat = append_stat('puntReturnYards',dict_stats,stat)
    stat = append_stat('puntReturns',dict_stats,stat)
    stat = append_stat('puntReturnTDs',dict_stats,stat)

    
    return stat
                

def insert_team_stats_data(api, WEEK=1, year=globals.YEAR):
    stat_list = []
    for week in range(WEEK, globals.WEEK+1):
        week_stats = api.get_team_game_stats(year=year, week=week)
        for game_stats in week_stats:
            for team in game_stats.teams:
                team_stats = team['stats']
                all_stats = {}
                for stat in team_stats:
                    all_stats[stat['category']] = stat['stat']
                try:
                    stat = format_stat_list([game_stats.id, team['school']],all_stats)
                except Exception as e:
                    print(f"{game_stats.id  - team['school']}")
                    raise e
                stat.append(year)
                stat.append(week)
                stat_list.append(stat)
    cbd.insert_game_stats(stat_list)
        
####TEAMS#####
def insert_teams(api):
    teams = api.get_fbs_teams()
    team_list = []
    for team in teams:
        capacity = team.location['capacity']
        city = team.location['city']
        elevation = team.location['elevation']
        year_constructed = team.location['year_constructed']
        lat = str(team.location['latitude'])
        long = str(team.location['longitude'])
        grass = str(team.location['grass'])
        dome = str(team.location['dome'])
        stad_id = team.location['venue_id']
        stad_name = team.location['name']
        state = team.location['state']
        data = [team.id, team.school, team.conference, team.mascot, stad_name,
                year_constructed, lat, long, stad_id, capacity, grass, dome, state, city]
        team_list.append(data)
    cbd.insert_teams(team_list)


        
###GAMES####

def insert_games(api,WEEK=1):
    game_list = []
    for week in range(WEEK, globals.WEEK+1):
        week_games = api.get_games(year=2022, week=week)
        for game in week_games:
            hl = game.home_line_scores
            if hl is None or len(hl) != 4:
                hq1 = 0
                hq2 = 0
                hq3 = 0
                hq4 = 0
            else:
                hq1 = hl[0]
                hq2 = hl[1]
                hq3 = hl[2]
                hq4 = hl[3]
            al = game.away_line_scores
            if al is None or len(al) != 4:
                aq1 = 0
                aq2 = 0
                aq3 = 0
                aq4 = 0
            else:
                aq1 = al[0]
                aq2 = al[1]
                aq3 = al[2]
                aq4 = al[3] 
            gl = [game.id, game.home_team, game.home_id, game.away_team, game.away_id, game.week, game.season,
                  game.home_points, game.away_points, game.neutral_site, hq1,hq2,hq3,hq4,aq1,aq2,aq3,aq4
                  ,game.venue_id, game.conference_game,game.season_type]
            game_list.append(gl)
    cbd.insert_games(game_list)
            

###RANKINGS##############

def insert_rankings_data(api,WEEK=1,year=1936):
    rankings_list = []
    for y in range(year,globals.YEAR+1):
        print(y)
        rankings = api.get_rankings(year=y)
        for week in rankings:
            for poll in week.polls:
                for rank in poll['ranks']:
                    data = [rank['school'],rank['conference'],rank['rank'],rank['firstPlaceVotes'],
                            rank['points'],poll['poll'],week.season_type,week.week, week.season]
                    rankings_list.append(data)
    cbd.insert_into_polls(rankings_list)
                    
        

    


###ALL####
def load_all():
    insert_games(game_api)
    insert_teams(team_api)
    insert_team_stats_data(game_api)


if __name__ == '__main__':
    insert_rankings_data(rank_api)


