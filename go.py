import os
import sys

DIR=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DIR, 'deps'))

import djangogo

parser=djangogo.make_parser()
args=parser.parse_args()
djangogo.main(args,
	project='SocialTennis_proj',
	app='SocialTennis',
	database='socialtennis_database',
	user='socialtennis_user',
	heroku_url='https://rocky-beach-86807.herokuapp.com/',
)
