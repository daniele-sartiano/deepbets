
import sys
import time
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import *

import numpy as np

class Extractor(object):
    def __init__(self, name):
        self.engine = create_engine('sqlite:///%s' % name, echo=False)
        Base.metadata.bind = self.engine
        self.session = Session(self.engine)

    @staticmethod
    def get_labels(home, away):
        return 1 if home>away else 2 if home<away else 0

        
    def extract(self):
        league_obj = None
        for league in self.session.query(League).filter(League.name.ilike('%italy%')):
            league_obj = league
        
        for match in self.session.query(Match).filter(Match.league == league_obj):
            home_players = []
            away_players = []
            home_attributes = []
            away_attributes = []
            for i in xrange(1, 12):
                for ii in xrange(2):
                    if ii == 0:
                        key = 'home'
                        l = home_players
                        attributes_list = home_attributes
                    else:
                        key = 'away'
                        l = away_players
                        attributes_list = away_attributes
                    player = self.session.query(Player).filter(Player.player_api_id == getattr(match, '%s_player_%s' % (key, i))).first()

                    if player is not None:
                        player_attributes = self.session.query(PlayerAttribute).filter(PlayerAttribute.player_api_id == player.player_api_id).first().get_array()
                    else:
                        player_attributes = PlayerAttribute.get_fake_data()
                    
                    player = player.get_array() if player else Player.get_fake_data()
                    l.extend(player)
                    l.extend(player_attributes)
                    attributes_list.extend(player_attributes)
                    
            
            assert(len(away_players) == len(home_players))

            example = [match.home_team_api_id, match.away_team_api_id]
            example.append(sum(home_attributes))
            example.append(sum(away_attributes))
            example.append(sum(home_attributes) - sum(away_attributes))
            example.extend(home_players)
            example.extend(away_players)
            

            # print match.home_team_api.team_api_id, match.away_team_api.team_api_id
            # print match.goal

            # result = match.get_goals_by_xml()
            # if not match.home_team_api.team_api_id in result:
            #     result[match.home_team_api.team_api_id] = 0
            # if not match.away_team_api.team_api_id in result:
            #     result[match.away_team_api.team_api_id] = 0
            print >> sys.stderr, match.date, match.home_team_api.team_long_name, 'vs', match.away_team_api.team_long_name#, result[match.home_team_api.team_api_id], ':', result[match.away_team_api.team_api_id]
            # print self.get_labels(result[match.home_team_api.team_api_id], result[match.away_team_api.team_api_id])
            # print match.home_team_goal, ':', match.away_team_goal
            # print self.get_labels(*match.get_goals())


            timestamp = time.mktime(datetime.datetime.strptime(match.date.split(' ')[0], "%Y-%m-%d").timetuple())
            example.append(timestamp)
            print >> sys.stdout, '%s\t%s\t%s' % (match.date, ','.join(map(str, example)), self.get_labels(*match.get_goals()))
            
            

def main():
    db = sys.argv[1]
    extractor = Extractor(db)
    extractor.extract()
            
if __name__ == '__main__':
    main()
