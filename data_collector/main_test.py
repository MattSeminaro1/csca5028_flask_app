import unittest
from unittest.mock import patch, MagicMock
from main import find_endpoints, get_stat_data, clean_csv
import pandas as pd

class TestBaseballScript(unittest.TestCase):

    @patch('requests.get')
    def test_find_endpoints(self, mock_get):
        # Mocking the response of requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'<a href="/boxes/DET/DET202404180.shtml">Box Score</a>'
        mock_get.return_value = mock_response

        test_url = "https://www.baseball-reference.com/boxes/?month=4&day=18&year=2024"
        endpoints = find_endpoints(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertIsInstance(endpoints, list)
        self.assertEqual(len(endpoints), 1)
        self.assertIn("https://www.baseball-reference.com/boxes/DET/DET202404180.shtml", endpoints)


    def test_get_stat_data(self):
        # Mocking get_stat_data behavior directly
        test_link_list = ["https://www.baseball-reference.com/boxes/DET/DET202404180.shtml"]
        batting_data = [['--- When using SR data, please cite us and provide a link and/or a mention.', '', '', ' ', 'Batting,AB,R,H,RBI,BB,SO,PA,BA,OBP,SLG,OPS,Pit,Str,WPA,aLI,WPA+,WPA-,cWPA,acLI,RE24,PO,A,Details,Batting-additional', 'Luis Arráez 2B,4,0,0,0,0,0,4,.263,.337,.325,.662,15,11,-0.023,0.33,0.008,-0.031,-0.01%,0.13,-0.3,3,2,,arraelu01', 'Vidal Bruján 2B,0,0,0,0,0,0,0,.100,.182,.150,.332,,,,,,,,,,0,0,,brujavi01', 'Bryan De La Cruz DH,4,1,1,1,0,2,4,.286,.294,.476,.770,19,12,-0.007,0.27,0.018,-0.024,-0.00%,0.11,0.3,,,HR,delacbr01', 'Jazz Chisholm Jr. CF,4,0,2,0,0,2,4,.246,.342,.391,.733,16,10,0.000,0.22,0.016,-0.016,0%,0.09,0.4,2,0,2B,chishja01', 'Josh Bell 1B,3,1,0,0,1,0,4,.192,.298,.315,.613,17,10,-0.035,0.32,0.004,-0.039,-0.01%,0.13,-0.6,5,0,,belljo02', 'Jesús Sánchez RF,4,0,0,0,0,2,4,.167,.222,.167,.389,14,11,-0.036,0.33,0.000,-0.036,-0.01%,0.13,-1.3,2,0,,sanchje02', 'Tim Anderson SS,3,0,0,0,0,1,3,.254,.299,.270,.568,8,7,-0.023,0.29,0.000,-0.023,-0.01%,0.11,-0.6,0,3,,anderti01', 'Otto Lopez SS,1,1,1,0,0,0,1,.286,.286,.286,.571,5,3,0.000,0.01,0.000,0.000,0%,0.00,0.2,0,0,,lopezot01', 'Nick Gordon LF,4,0,1,2,0,0,4,.211,.262,.474,.736,19,13,-0.029,0.29,0.001,-0.030,-0.01%,0.12,1.0,2,0,,gordoni01', 'Emmanuel Rivera 3B,4,0,1,0,0,2,4,.214,.290,.214,.505,13,11,-0.013,0.20,0.004,-0.017,-0.00%,0.08,-0.4,1,3,,riverem01', 'Nick Fortes C,3,0,0,0,0,0,3,.088,.162,.118,.280,16,12,-0.019,0.22,0.000,-0.019,-0.00%,0.09,-0.6,9,0,,forteni01', ',,,,,,,,,,,,,,,,,,,,,,,,-9999', 'A.J. Puk P,,,,,,,,,,,,,,,,,,,,,0,0,,pukaj01', 'Declan Cronin P,,,,,,,,,,,,,,,,,,,,,0,0,,cronide01', 'Burch Smith P,,,,,,,,,,,,,,,,,,,,,0,0,,smithbu03', 'Andrew Nardi P,,,,,,,,,,,,,,,,,,,,,0,1,,nardian01', 'Team Totals,34,3,6,3,1,9,35,.176,.200,.294,.494,142,100,-0.185,0.27,0.051,-0.235,-0.04%,0.11,-1.9,24,9,,-9999'], ['--- When using SR data, please cite us and provide a link and/or a mention.', '', '', ' ', 'Batting,AB,R,H,RBI,BB,SO,PA,BA,OBP,SLG,OPS,Pit,Str,WPA,aLI,WPA+,WPA-,cWPA,acLI,RE24,PO,A,Details,Batting-additional', 'Nico Hoerner 2B,5,1,2,1,0,0,5,.258,.382,.355,.736,14,10,0.136,0.33,0.141,-0.005,0.09%,0.35,0.2,2,3,2·2B,hoernni01', 'Patrick Wisdom RF-3B,4,1,0,0,1,2,5,.000,.200,.000,.200,21,11,0.006,0.39,0.029,-0.023,0.00%,0.42,-0.9,2,3,,wisdopa01', 'Cody Bellinger CF,4,1,2,1,0,0,4,.216,.306,.378,.684,18,11,0.098,0.58,0.100,-0.003,0.06%,0.62,1.1,2,0,,bellico01', 'Christopher Morel DH,3,1,0,0,1,0,4,.208,.266,.375,.641,18,11,-0.062,0.57,0.026,-0.088,-0.04%,0.61,-0.9,,,GDP,morelch01', 'Dansby Swanson SS,3,2,2,1,1,1,4,.254,.325,.408,.733,17,10,0.118,0.52,0.119,0.000,0.08%,0.56,2.0,2,1,2B,swansda01', 'Ian Happ LF,2,0,0,0,1,2,3,.240,.352,.360,.712,13,8,-0.049,0.61,0.005,-0.054,-0.03%,0.65,-0.5,0,0,,happia01', 'Alexander Canario LF,1,0,0,0,0,1,1,.333,.333,.667,1.000,4,3,0.000,0.01,0.000,0.000,0%,0.01,-0.1,0,0,,canaral01', 'Garrett Cooper 1B,3,0,1,1,1,1,4,.346,.414,.577,.991,18,10,0.020,0.51,0.041,-0.021,0.01%,0.54,0.5,7,1,,coopega03', 'Nick Madrigal 3B,1,2,0,1,0,0,2,.250,.286,.350,.636,2,1,0.024,0.65,0.024,0.000,0.01%,0.69,0.2,0,0,HBP,madrini01', 'Mike Tauchman PH-RF,2,0,2,1,0,0,2,.256,.396,.359,.755,4,3,0.012,0.14,0.012,0.000,0.01%,0.14,2.4,1,0,2B,tauchmi01', 'Miguel Amaya C,4,0,1,2,0,2,4,.278,.308,.472,.780,14,11,0.015,0.39,0.043,-0.028,0.01%,0.41,-0.3,10,0,2BGDP,amayami01', ',,,,,,,,,,,,,,,,,,,,,,,,-9999', 'Jameson Taillon P,,,,,,,,,,,,,,,,,,,,,0,0,,taillja01', 'Keegan Thompson P,,,,,,,,,,,,,,,,,,,,,0,0,,thompke02', 'Colten Brewer P,,,,,,,,,,,,,,,,,,,,,1,0,,breweco01', 'Team Totals,32,8,10,8,5,9,38,.312,.421,.469,.890,143,89,0.318,0.45,0.540,-0.222,0.20%,0.49,3.6,27,8,,-9999']]

        pitching_data = [['--- When using SR data, please cite us and provide a link and/or a mention.', '', '', ' ',
                          'Pitching,IP,H,R,ER,BB,SO,HR,ERA,BF,Pit,Str,Ctct,StS,StL,GB,FB,LD,Unk,GSc,IR,IS,WPA,aLI,cWPA,acLI,RE24,Pitching-additional',
                          'A.J. Puk L (0-4),3,7,7,7,3,4,0,9.22,19,70,40,21,6,13,4,7,3,0,18,,,-0.319,0.84,-0.07%,0.33,-5.4,pukaj01',
                          'Declan Cronin,2,2,1,1,1,1,0,2.45,8,28,18,10,3,5,2,4,2,0,,0,0,-0.001,0.15,0.00%,0.06,0.1,cronide01',
                          'Burch Smith,2,0,0,0,0,2,0,4.82,6,26,19,10,3,6,1,3,0,0,,0,0,0.003,0.01,0.00%,0.00,1.1,smithbu03',
                          'Andrew Nardi,1,1,0,0,1,2,0,10.38,5,19,12,7,2,3,1,1,1,0,,0,0,0.000,0.01,0.00%,0.00,0.5,nardian01', 'Team Totals,8,10,8,8,5,9,0,9.00,38,143,89,48,14,27,8,15,6,0,18,0,0,-0.317,0.45,-0.07%,0.18,-3.6,-9999'], ['--- When using SR data, please cite us and provide a link and/or a mention.', '', '', ' ', 'Pitching,IP,H,R,ER,BB,SO,HR,ERA,BF,Pit,Str,Ctct,StS,StL,GB,FB,LD,Unk,GSc,IR,IS,WPA,aLI,cWPA,acLI,RE24,Pitching-additional', 'Jameson Taillon W (1-0),5,3,1,1,0,4,1,1.80,18,73,54,30,12,12,4,10,3,0,61,,,0.164,0.45,0.10%,0.48,1.7,taillja01', 'Keegan Thompson,2,0,0,0,1,4,0,0.00,8,36,22,10,8,4,3,0,0,0,,0,0,0.015,0.16,0.01%,0.17,1.1,thompke02', 'Colten Brewer,2,3,2,1,0,1,0,4.50,9,33,24,14,5,5,5,3,2,0,,0,0,0.005,0.04,0.00%,0.04,-0.9,breweco01', 'Team Totals,9,6,3,2,1,9,1,2.00,35,142,100,54,25,21,12,13,5,0,61,0,0,0.184,0.27,0.12%,0.29,1.9,-9999']]


        # Patching get_stat_data inside the module under test
        with patch('main.get_stat_data') as mock_get_stat_data:
            # Setting the side effect
            mock_get_stat_data.side_effect = [batting_data, pitching_data]

            # Calling the function under test
            batting_data_result = get_stat_data(test_link_list, 'batting')
            pitching_data_result = get_stat_data(test_link_list, 'pitching')

            # Assertions
            self.assertIsInstance(batting_data_result, list)
            self.assertIsInstance(pitching_data_result, list)

            # Check if the elements in the list are also lists
            for data in batting_data_result:
                self.assertIsInstance(data, list)
            for data in pitching_data_result:
                self.assertIsInstance(data, list)

    def test_clean_csv(self):
        # Sample data
        test_batting_csv = [['--- When using SR data, please cite us and provide a link and/or a mention.', '', '', ' ',
                         'Batting,AB,R,H,RBI,BB,SO,PA,BA,OBP,SLG,OPS,Pit,Str,WPA,aLI,WPA+,WPA-,cWPA,acLI,RE24,PO,A,Details,Batting-additional',
                         'Luis Arráez 2B,4,0,0,0,0,0,4,.263,.337,.325,.662,15,11,-0.023,0.33,0.008,-0.031,-0.01%,0.13,-0.3,3,2,,arraelu01',
                         'Vidal Bruján 2B,0,0,0,0,0,0,0,.100,.182,.150,.332,,,,,,,,,,0,0,,brujavi01',
                         'Bryan De La Cruz DH,4,1,1,1,0,2,4,.286,.294,.476,.770,19,12,-0.007,0.27,0.018,-0.024,-0.00%,0.11,0.3,,,HR,delacbr01',
                         'Jazz Chisholm Jr. CF,4,0,2,0,0,2,4,.246,.342,.391,.733,16,10,0.000,0.22,0.016,-0.016,0%,0.09,0.4,2,0,2B,chishja01',
                         'Josh Bell 1B,3,1,0,0,1,0,4,.192,.298,.315,.613,17,10,-0.035,0.32,0.004,-0.039,-0.01%,0.13,-0.6,5,0,,belljo02',
                         'Jesús Sánchez RF,4,0,0,0,0,2,4,.167,.222,.167,.389,14,11,-0.036,0.33,0.000,-0.036,-0.01%,0.13,-1.3,2,0,,sanchje02',
                         'Tim Anderson SS,3,0,0,0,0,1,3,.254,.299,.270,.568,8,7,-0.023,0.29,0.000,-0.023,-0.01%,0.11,-0.6,0,3,,anderti01',
                         'Otto Lopez SS,1,1,1,0,0,0,1,.286,.286,.286,.571,5,3,0.000,0.01,0.000,0.000,0%,0.00,0.2,0,0,,lopezot01',
                         'Nick Gordon LF,4,0,1,2,0,0,4,.211,.262,.474,.736,19,13,-0.029,0.29,0.001,-0.030,-0.01%,0.12,1.0,2,0,,gordoni01',
                         'Emmanuel Rivera 3B,4,0,1,0,0,2,4,.214,.290,.214,.505,13,11,-0.013,0.20,0.004,-0.017,-0.00%,0.08,-0.4,1,3,,riverem01',
                         'Nick Fortes C,3,0,0,0,0,0,3,.088,.162,.118,.280,16,12,-0.019,0.22,0.000,-0.019,-0.00%,0.09,-0.6,9,0,,forteni01',
                         ',,,,,,,,,,,,,,,,,,,,,,,,-9999', 'A.J. Puk P,,,,,,,,,,,,,,,,,,,,,0,0,,pukaj01',
                         'Declan Cronin P,,,,,,,,,,,,,,,,,,,,,0,0,,cronide01',
                         'Burch Smith P,,,,,,,,,,,,,,,,,,,,,0,0,,smithbu03',
                         'Andrew Nardi P,,,,,,,,,,,,,,,,,,,,,0,1,,nardian01',
                         'Team Totals,34,3,6,3,1,9,35,.176,.200,.294,.494,142,100,-0.185,0.27,0.051,-0.235,-0.04%,0.11,-1.9,24,9,,-9999'],
                        ['--- When using SR data, please cite us and provide a link and/or a mention.', '', '', ' ',
                         'Batting,AB,R,H,RBI,BB,SO,PA,BA,OBP,SLG,OPS,Pit,Str,WPA,aLI,WPA+,WPA-,cWPA,acLI,RE24,PO,A,Details,Batting-additional',
                         'Nico Hoerner 2B,5,1,2,1,0,0,5,.258,.382,.355,.736,14,10,0.136,0.33,0.141,-0.005,0.09%,0.35,0.2,2,3,2·2B,hoernni01',
                         'Patrick Wisdom RF-3B,4,1,0,0,1,2,5,.000,.200,.000,.200,21,11,0.006,0.39,0.029,-0.023,0.00%,0.42,-0.9,2,3,,wisdopa01',
                         'Cody Bellinger CF,4,1,2,1,0,0,4,.216,.306,.378,.684,18,11,0.098,0.58,0.100,-0.003,0.06%,0.62,1.1,2,0,,bellico01',
                         'Christopher Morel DH,3,1,0,0,1,0,4,.208,.266,.375,.641,18,11,-0.062,0.57,0.026,-0.088,-0.04%,0.61,-0.9,,,GDP,morelch01',
                         'Dansby Swanson SS,3,2,2,1,1,1,4,.254,.325,.408,.733,17,10,0.118,0.52,0.119,0.000,0.08%,0.56,2.0,2,1,2B,swansda01',
                         'Ian Happ LF,2,0,0,0,1,2,3,.240,.352,.360,.712,13,8,-0.049,0.61,0.005,-0.054,-0.03%,0.65,-0.5,0,0,,happia01',
                         'Alexander Canario LF,1,0,0,0,0,1,1,.333,.333,.667,1.000,4,3,0.000,0.01,0.000,0.000,0%,0.01,-0.1,0,0,,canaral01',
                         'Garrett Cooper 1B,3,0,1,1,1,1,4,.346,.414,.577,.991,18,10,0.020,0.51,0.041,-0.021,0.01%,0.54,0.5,7,1,,coopega03',
                         'Nick Madrigal 3B,1,2,0,1,0,0,2,.250,.286,.350,.636,2,1,0.024,0.65,0.024,0.000,0.01%,0.69,0.2,0,0,HBP,madrini01',
                         'Mike Tauchman PH-RF,2,0,2,1,0,0,2,.256,.396,.359,.755,4,3,0.012,0.14,0.012,0.000,0.01%,0.14,2.4,1,0,2B,tauchmi01',
                         'Miguel Amaya C,4,0,1,2,0,2,4,.278,.308,.472,.780,14,11,0.015,0.39,0.043,-0.028,0.01%,0.41,-0.3,10,0,2BGDP,amayami01',
                         ',,,,,,,,,,,,,,,,,,,,,,,,-9999', 'Jameson Taillon P,,,,,,,,,,,,,,,,,,,,,0,0,,taillja01',
                         'Keegan Thompson P,,,,,,,,,,,,,,,,,,,,,0,0,,thompke02',
                         'Colten Brewer P,,,,,,,,,,,,,,,,,,,,,1,0,,breweco01',
                         'Team Totals,32,8,10,8,5,9,38,.312,.421,.469,.890,143,89,0.318,0.45,0.540,-0.222,0.20%,0.49,3.6,27,8,,-9999']]

        test_pitching_csv = [['--- When using SR data, please cite us and provide a link and/or a mention.', '', '', ' ',
                          'Pitching,IP,H,R,ER,BB,SO,HR,ERA,BF,Pit,Str,Ctct,StS,StL,GB,FB,LD,Unk,GSc,IR,IS,WPA,aLI,cWPA,acLI,RE24,Pitching-additional',
                          'A.J. Puk L (0-4),3,7,7,7,3,4,0,9.22,19,70,40,21,6,13,4,7,3,0,18,,,-0.319,0.84,-0.07%,0.33,-5.4,pukaj01',
                          'Declan Cronin,2,2,1,1,1,1,0,2.45,8,28,18,10,3,5,2,4,2,0,,0,0,-0.001,0.15,0.00%,0.06,0.1,cronide01',
                          'Burch Smith,2,0,0,0,0,2,0,4.82,6,26,19,10,3,6,1,3,0,0,,0,0,0.003,0.01,0.00%,0.00,1.1,smithbu03',
                          'Andrew Nardi,1,1,0,0,1,2,0,10.38,5,19,12,7,2,3,1,1,1,0,,0,0,0.000,0.01,0.00%,0.00,0.5,nardian01',
                          'Team Totals,8,10,8,8,5,9,0,9.00,38,143,89,48,14,27,8,15,6,0,18,0,0,-0.317,0.45,-0.07%,0.18,-3.6,-9999'],
                         ['--- When using SR data, please cite us and provide a link and/or a mention.', '', '', ' ',
                          'Pitching,IP,H,R,ER,BB,SO,HR,ERA,BF,Pit,Str,Ctct,StS,StL,GB,FB,LD,Unk,GSc,IR,IS,WPA,aLI,cWPA,acLI,RE24,Pitching-additional',
                          'Jameson Taillon W (1-0),5,3,1,1,0,4,1,1.80,18,73,54,30,12,12,4,10,3,0,61,,,0.164,0.45,0.10%,0.48,1.7,taillja01',
                          'Keegan Thompson,2,0,0,0,1,4,0,0.00,8,36,22,10,8,4,3,0,0,0,,0,0,0.015,0.16,0.01%,0.17,1.1,thompke02',
                          'Colten Brewer,2,3,2,1,0,1,0,4.50,9,33,24,14,5,5,5,3,2,0,,0,0,0.005,0.04,0.00%,0.04,-0.9,breweco01',
                          'Team Totals,9,6,3,2,1,9,1,2.00,35,142,100,54,25,21,12,13,5,0,61,0,0,0.184,0.27,0.12%,0.29,1.9,-9999']]

        cleaned_batting_data = clean_csv(test_batting_csv, 'batting')
        cleaned_pitching_data = clean_csv(test_pitching_csv, 'pitching')

        self.assertIsInstance(cleaned_batting_data, pd.DataFrame)
        self.assertIsInstance(cleaned_pitching_data, pd.DataFrame)



if __name__ == '__main__':
    unittest.main()