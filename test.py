import os
import unittest
import json
from datetime import datetime
 
from serveren import app, db
 
 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['MONGODB_SETTINGS'] = {
                                        'db': 'audio_metadata',
                                        'host': 'localhost',
                                        'port': 27017
                                      }
        self.app = app.test_client()

 
    # executed after each test
    def tearDown(self):
        pass
 
 
###############
#### tests ####
###############

#################################################################
################       CREATE          ##########################

    def test_create_success1(self):
        Datetime=datetime.now()
        da={"audioFileType": "Song", "audioFileMetadata": {"Id":"12123232000",
                                                        "songName":"I wanna grow old with you.",
                                                        "songDuration":"220"
                                                                                                    }
            }

        response = self.app.post('/audiometa',data=json.dumps(da),content_type='application/json')
        self.assertEqual(response.status_code, 200)   

    def test_create_fail1(self):
        Datetime=datetime.now()
        da={"audioFileType": "Song", "audioFileMetadata": {"Id":"12123232000new", ###### String in Id, (Required only integers.) #######
                                                        "songName":"I wanna grow old with you 1.",
                                                        "songDuration":"220"
                                                            }
            }

        response = self.app.post('/audiometa',data=json.dumps(da),content_type='application/json')
        self.assertEqual(response.status_code, 400) 

    def test_create_fail2(self):
        Datetime=datetime.now()
        da={"audioFileType": "Song", "audioFileMetadata": {"Id":"12123232001", ###### Duplicate Id #######
                                                        "songName":"I wanna grow old with you 2.", 
                                                        "songDuration":"220"
                                                        }
            }

        response = self.app.post('/audiometa',data=json.dumps(da),content_type='application/json')
        self.assertEqual(response.status_code, 400)                                             

    def test_create_fail3(self):
        Datetime=datetime.now()
        da={"audioFileType": "Song", "audioFileMetadata": {"Id":"12123232002", ###### Song name larger than 100 character #######
                                                        "songName":"ABCD EFGH IJKL MNOP QRST UVWX YZ, ABCD EFGH IJKL MNOP QRST UVWX YZ, ABCD EFGH IJKL MNOP QRST UVWX YZ, ABCD EFGH IJKL MNOP QRST UVWX YZ",
                                                        "songDuration":"220"
                                                            }
            }

        response = self.app.post('/audiometa',data=json.dumps(da),content_type='application/json')
        self.assertEqual(response.status_code, 400) 

    def test_create_fail4(self):
        Datetime=datetime.now()
        da={"audioFileType": "Song", "audioFileMetadata": {"Id":"12123232003", 
                                                        "songName":"I wanna grow old with you 3.", 
                                                        "songDuration":"-220" ###### Negative duration #######
                                                        }
            }
        response = self.app.post('/audiometa',data=json.dumps(da),content_type='application/json')
        self.assertEqual(response.status_code, 400) 

    def test_create_success2(self):
        Datetime=datetime.now()
        da={"audioFileType": "Podcast", "audioFileMetadata": {"Id":"12123232000", 
                                                        "podcastName":"Ummid", 
                                                        "podcastDuration":"220" ,
                                                        "podcastHost" : "Zakir khan",
                                                        "podcastParticipants" : ["Yash", "Raj", "DK", "DC"]
                                                        }
            }
        response = self.app.post('/audiometa',data=json.dumps(da),content_type='application/json')
        self.assertEqual(response.status_code, 200) 

    def test_create_success3(self):
        Datetime=datetime.now()
        da={"audioFileType": "Audiobook", "audioFileMetadata": {"Id":"12123232000", 
                                                        "audiobookName":"The alchemist", 
                                                        "audiobookAuthor" : "Polo cohelo",
                                                        "audiobookNarrator": "Yash viroja",
                                                        "audiobookDuration":"220" 
                                                        }
            }
        response = self.app.post('/audiometa',data=json.dumps(da),content_type='application/json')
        self.assertEqual(response.status_code, 200) 

    def test_create_fail5(self):
        Datetime=datetime.now()
        da={"audioFileType": "Podcast", "audioFileMetadata": {"Id":"12123232000", 
                                                        "podcastName":"Ummid", 
                                                        "podcastDuration":"220",
                                                        "podcastHost" : "Zakir khan", ###### List longer than 10 names #######
                                                        "podcastParticipants" : ["Yash", "Raj", "DK", "DC","Kk","Asha","Twinkle","Landy","Rinku","Krima","Priyanka"]
                                                        }
            }
        response = self.app.post('/audiometa',data=json.dumps(da),content_type='application/json')
        self.assertEqual(response.status_code, 400) 

    def test_create_fail6(self):
        Datetime=datetime.now()
        da={"audioFileType": "Song", "audioFileMetadata": {"Id":"12123232004",
                                                        "songName":"I wanna grow old with you 4."
                                                            }           ######## "songDuration" required field is missing ###########
            }
        response = self.app.post('/audiometa',data=json.dumps(da),content_type='application/json')
        self.assertEqual(response.status_code, 400) 
#################################################################
################       QUERY          ###########################
    def test_query_song_success(self):
        response = self.app.get('/Song/12123232000')
        self.assertEqual(response.status_code, 200)
    def test_query_song_fail(self):
        response = self.app.get('/Song/1212')                 ########### With Id 1212 no file in database#######
        self.assertEqual(response.status_code, 400)

    def test_query_podcast_success(self):
        response = self.app.get('/Podcast/12123232000')
        self.assertEqual(response.status_code, 200)
    def test_query_podcast_fail(self):
        response = self.app.get('/Podcaster/12123232000')      ########### "Podcaster" instead of "Podcast" #########
        self.assertEqual(response.status_code, 400)

    def test_query_audiobook_success(self):
        response = self.app.get('/Audiobook/12123232000')
        self.assertEqual(response.status_code, 200)
    def test_query_audiobook_fail(self):
        response = self.app.get('/Audiobook/1212')        ########### With Id 1212 no file in database#######
        self.assertEqual(response.status_code, 400)

    def test_query_song_success1(self):
        response = self.app.get('/Song')
        self.assertEqual(response.status_code, 200)        ####### Returns all songs from the document.########

    def test_query_song_success1(self):
        response = self.app.get('/Songs')              #### "Songs" instead of "Song" which is not valid.##########
        self.assertEqual(response.status_code, 400)

#################################################################
################       UPDATE          ##########################

    def test_update_success1(self):
        Datetime=datetime.now()
        da={
            "songName":"Wanna shake it up",
            "songDuration":"205"
            }
                                                
        response = self.app.put('/Song/12123232000',data=json.dumps(da),content_type='application/json')
        self.assertEqual(response.status_code, 200)       
    
    def test_update_fail1(self):
        Datetime=datetime.now()
        da={
            "songsName":"Wanna shake it up",   ############ "Songs" instead of "Song" ################3
            "songsDuration":"205"
            }
                                                
        response = self.app.put('/Song/12123232000',data=json.dumps(da),content_type='application/json')
        self.assertEqual(response.status_code, 400)    
 
#################################################################
################       DELETE          ##########################
    def test_zdelete_song_success(self):
        response = self.app.delete('/Song/12123232000')
        self.assertEqual(response.status_code, 200)

    def test_zdelete_song_failed(self):
        response = self.app.delete('/Songs/1212')                    ########### "Songs" instead of "Song" #######
        self.assertEqual(response.status_code, 400)           

    def test_zdelete_podcast_success(self):
        response = self.app.delete('/Podcast/12123232000')
        self.assertEqual(response.status_code, 200)
    def test_zdelete_podcast_failed(self):
        response = self.app.delete('/Podcast/1212')                        ########### With Id 1212 no file in database#######
        self.assertEqual(response.status_code, 400)

    def test_zdelete_audiobook_success(self):
        response = self.app.delete('/Audiobook/12123232000')
        self.assertEqual(response.status_code, 200)
    def test_zdelete_audiobook_failed(self):
        response = self.app.delete('/Audiobook/1212')                         ########### With Id 1212 no file in database#######
        self.assertEqual(response.status_code, 400)



if __name__ == "__main__":
    unittest.main()
