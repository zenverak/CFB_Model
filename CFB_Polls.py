import CFBDB as cbd
import globals

REPLACES = globals.REPLACES

def get_flair(name):
    if name in REPLACES:
        f_name = REPLACES[name]['flair']
        n = REPLACES[name]['name']
        return "[{}](#f/{})".format(n, f_name)
    else:
        f_name = name.replace(' ','').replace('&','').replace('(','').replace(')','').replace("'",'').lower()
        return "[{}](#f/{})".format(name, f_name)


class School():

    def __init__(self, name):
        self.name = name
        self.weeks1 = []
        self.weeks5 = []
        self.conf = ''
        self.years_end5 = []
        self.total_points = 0
        self.decades_points = {x:0 for x in range(1930,2030,10)}
        self.rankings_rank = {x:[] for x in range(1,26)}
        self.rankings_years = {}
        self.rankings = []


    def add_total_rank_score(self,rank,year,week=0):
        if week == 0:
            total_points = 25 - int(rank) + 1
        else:
            points = 25 - int(rank) + 1
            total_points = points*week
        self.total_points +=  total_points
        self.add_score_decades(year, total_points)


    def add_total_rank_score_add(self,rank,year,week=0):
        if week == 0:
            total_points = 25 - int(rank) + 1
        else:
            points = 25 - int(rank) + 1
            week_point = week/17.0
            total_points = points + week_point
        self.total_points +=  total_points
        self.add_score_decades(year, total_points)



    def add_score_decades(self,year, points):
        dec = int(str(year)[0:3]+ '0')
        self.decades_points[dec] += points
        
            
        
    def count_per_week(self):
        print("***{}***".format(self.name))
        for rank in range(1,26):
            print("{}: {}".format(rank, len(self.rankings_rank[rank])))


    def __repr__(self):
        return str(self.total_points)



class Poll():

    def __init__(self):
        self.schools = {}
        self.data = cbd.get_all_rankings_poll('AP Top 25')
        self.create_schools()
        self.decades = {x:[] for x in range(1930,2030,10)}
        self.total_ranks = []


    def create_schools(self):
        for ranking in self.data:
            team = ranking[0]
            rank = ranking[2]
            season_type = ranking[6]
            week = ranking[7]
            year = ranking[8]
            if week == 1 and season_type != 'regular':
                week = 17
            if team not in self.schools:
                self.schools[team] = School(team)
            self.schools[team].rankings_rank[rank].append({"week":week, "year":year})
            self.schools[team].add_total_rank_score(rank,year,week)
            self.schools[team].rankings.append(ranking)
            if rank == 1:
                self.schools[team].weeks5.append(ranking)
                self.schools[team].weeks1.append(ranking)
            elif rank < 6:
                self.schools[team].weeks5.append(ranking)

    def rank_all(self):
        for s in self.schools:
            school = self.schools[s]
            self.total_ranks.append([school.name,round(school.total_points,2)])
            for dec in school.decades_points:
                dec_points = round(school.decades_points[dec],2)
                self.decades[dec].append([school.name,dec_points])
        self.total_ranks.sort(key=lambda x: -x[1])
        for dec in self.decades:
            self.decades[dec].sort(key=lambda x: -x[1])

    def show_ranking(self):
        print("ranking|team|ranking")
        print("----|----|----")
        for i  in range(0,25):
            team = self.total_ranks[i]
            print(f"{i+1}|{get_flair(team[0])}  {team[0]}|{team[1]}")

    def show_decades(self):
        for dec in self.decades:
            print(f"DECADE: {dec}")
            print("ranking|team|ranking")
            print("----|----|----")
            for i  in range(0,25):
                team = self.decades[dec][i]
                print(f"{i+1}|{get_flair(team[0])} {team[0]}|{team[1]}")
            print("------------------")
            print("------------------")

            
        
            
            
        

if __name__ == '__main__':
    poll = Poll()
    poll.rank_all()
    poll.show_ranking()
            
