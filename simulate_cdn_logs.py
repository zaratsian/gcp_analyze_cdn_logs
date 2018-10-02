
#####################################################################################
#
#   Simulate CDN Logs
#
#   USAGE: file.py --bucket_name BUCKET_NAME --iteration_count ITERATION_COUNT
#          file.py --bucket_name=cdn_logs_z2018 --iteration_count=100
#
#####################################################################################



import re
import json
import datetime,time
import random
import argparse
from google.cloud.storage import Blob
from google.cloud import storage



def simulate_cdn_logs(iteration_count):
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)'
        ]
    
    usa_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    
    countries = ['US']*80 + ['CN']*70 + ['IN']*50 + ['ZA']*20 + ['AW', 'AF', 'AO', 'AI', 'AX', 'AL', 'AD', 'AE', 'AR', 'AM', 'AS', 'AQ', 'TF', 'AG', 'AU', 'AT', 'AZ', 'BI', 'BE', 'BJ', 'BQ', 'BF', 'BD', 'BG', 'BH', 'BS', 'BA', 'BL', 'BY', 'BZ', 'BM', 'BO', 'BR', 'BB', 'BN', 'BT', 'BV', 'BW', 'CF', 'CA', 'CC', 'CH', 'CL', 'CN', 'CI', 'CM', 'CD', 'CG', 'CK', 'CO', 'KM', 'CV', 'CR', 'CU', 'CW', 'CX', 'KY', 'CY', 'CZ', 'DE', 'DJ', 'DM', 'DK', 'DO', 'DZ', 'EC', 'EG', 'ER', 'EH', 'ES', 'EE', 'ET', 'FI', 'FJ', 'FK', 'FR', 'FO', 'FM', 'GA', 'GB', 'GE', 'GG', 'GH', 'GI', 'GN', 'GP', 'GM', 'GW', 'GQ', 'GR', 'GD', 'GL', 'GT', 'GF', 'GU', 'GY', 'HK', 'HM', 'HN', 'HR', 'HT', 'HU', 'ID', 'IM', 'IN', 'IO', 'IE', 'IR', 'IQ', 'IS', 'IL', 'IT', 'JM', 'JE', 'JO', 'JP', 'KZ', 'KE', 'KG', 'KH', 'KI', 'KN', 'KR', 'KW', 'LA', 'LB', 'LR', 'LY', 'LC', 'LI', 'LK', 'LS', 'LT', 'LU', 'LV', 'MO', 'MF', 'MA', 'MC', 'MD', 'MG', 'MV', 'MX', 'MH', 'MK', 'ML', 'MT', 'MM', 'ME', 'MN', 'MP', 'MZ', 'MR', 'MS', 'MQ', 'MU', 'MW', 'MY', 'YT', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NU', 'NL', 'NO', 'NP', 'NR', 'NZ', 'OM', 'PK', 'PA', 'PN', 'PE', 'PH', 'PW', 'PG', 'PL', 'PR', 'KP', 'PT', 'PY', 'PS', 'PF', 'QA', 'RE', 'RO', 'RU', 'RW', 'SA', 'SD', 'SN', 'SG', 'GS', 'SH', 'SJ', 'SB', 'SL', 'SV', 'SM', 'SO', 'PM', 'RS', 'SS', 'ST', 'SR', 'SK', 'SI', 'SE', 'SZ', 'SX', 'SC', 'SY', 'TC', 'TD', 'TG', 'TH', 'TJ', 'TK', 'TM', 'TL', 'TO', 'TT', 'TN', 'TR', 'TV', 'TW', 'TZ', 'UG', 'UA', 'UM', 'UY', 'US', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU', 'WF', 'WS', 'YE', 'ZA', 'ZM', 'ZW']
    
    urls =  ["/2018/08/08/technology/deepfakes-countermeasures-facebook-twitter-youtube/index.html"]*10 + \
            ["/2018/09/28/technology/tesla-stock-analysts/index.html"]*8 + \
            [
            "/2018/10/01/us/allentown-pennsylvania-explosion-victims/index.html",
            "/2018/10/02/us/allentown-pennsylvania-car-explosion-investigation/index.html",
            "/2018/10/02/us/las-vegas-shooting-anniversary/index.html",
            "/2018/09/30/us/cristiano-ronaldo-rape-allegations-lawsuit/index.html",
            "/2018/09/29/us/shark-attack-san-diego/index.html",
            "/2018/10/01/us/jessica-chambers-mistrial/index.html",
            "/2018/10/01/us/orlando-police-hospital-shooting/index.html",
            "/2018/10/01/us/bear-injures-alaska-hunter-trnd/index.html",
            "/2018/10/01/politics/puerto-rico-governor-endorses-florida-candidates/index.html",
            "/2018/09/30/politics/kellyanne-conway-support-kavanaugh-cnntv/index.html",
            "/2018/09/27/politics/kavanaugh-american-bar-association/index.html",
            "/2018/09/27/world/gallery/week-in-photos-0928/index.html",
            "/2018/09/23/sport/gallery/what-a-shot-sports-0923/index.html",
            "/2018/09/20/world/gallery/week-in-photos-0921/index.html",
            "/2018/09/13/world/gallery/week-in-photos-0913/index.html",
            "/2018/09/06/world/gallery/week-in-photos-0907/index.html",
            "/2018/09/02/sport/gallery/what-a-shot-sports-0902/index.html",
            "/2018/08/30/world/gallery/week-in-photos-0831/index.html",
            "/2018/08/26/sport/gallery/what-a-shot-sports-0826/index.html",
            "/2018/10/02/politics/trump-michael-cohen-stormy-daniels/index.html",
            "/2018/10/02/politics/harvard-kavanaugh-not-teaching/index.html",
            "/2018/10/02/politics/trump-international-image-pew-report-intl/index.html",
            "/2018/10/01/us/prosecuting-sex-crimes/index.html",
            "/2018/10/02/politics/trump-brett-kavanaugh-turning-point-election-educated-white-women-voters/index.html",
            "/2018/10/02/politics/will-hurd-republican-survive-a-blue-wave/index.html",
            "/2018/10/02/us/five-things-october-2-trnd/index.html",
            "/2018/10/01/politics/brett-kavanaugh-yale-drinking/index.html",
            "/2018/10/02/politics/donald-trump-mitch-mcconnell-brett-kavanaugh-chris-coons-jeff-flake/index.html",
            "/2018/10/01/politics/mark-judge-fbi-interview/index.html",
            "/2018/10/01/politics/trump-bump-fire-stocks/index.html",
            "/2018/10/01/politics/beto-orourke-apologizes-college-newspaper/index.html",
            "/2018/10/01/politics/donald-trump-trade-nafta-usmca/index.html",
            "/2018/10/02/us/az-off-duty-border-patrol-agent-wildfire/index.html",
            "/2018/10/01/politics/donald-trump-trade-canada-mexico/index.html",
            "/2018/10/01/world/indonesia-earthquake-tsunami-satellite-trnd/index.html",
            "/2018/10/01/asia/indonesia-earthquake-tsunami-survivor-stories-intl/index.html",
            "/2018/10/01/asia/indonesia-earthquake-tsunami-warning-intl/index.html",
            "/2018/09/30/asia/indonesia-earthquake/index.html",
            "/2018/10/02/world/nobel-physics-prize-2018-intl/index.html",
            "/2018/10/02/africa/nigeria-nollywood-international/index.html",
            "/2018/09/30/world/iyw-aid-indonesia-earthquake-and-tsunami-victims/index.html",
            "/2018/10/02/asia/indonesia-palu-tsunami-earthquake-intl/index.html",
            "/2018/10/02/africa/nigeria-leather-economy/index.html",
            "/2018/10/02/opinions/2018-midterm-campaign-watch-roundup-opinion/index.html",
            "/2018/10/02/opinions/trumps-dc-distracting-the-world-opinion-intl/index.html",
            "/2018/10/01/opinions/trump-trade-deals-nafta-china-iran-andelman-opinion/index.html",
            "/2018/10/02/africa/victoire-ingabire-freed-asequals-africa-intl/index.html",
            "/2018/09/28/americas/hurricane-rosa-mexico-california-wxc/index.html",
            "/2018/09/28/americas/aung-san-suu-kyi-canada-intl/index.html",
            "/2018/10/01/middleeast/iran-syria-missiles/index.html",
            "/2018/10/01/europe/macron-photograph-intl/index.html",
            "/2018/10/01/europe/charles-aznavour-intl/index.html",
            "/2018/10/01/europe/jean-claude-arnault-nobel-rape-sentence-intl/index.html",
            "/2018/09/29/asia/gallery/indonesia-earthquake-tsunami-intl/index.html",
            "/2018/09/27/us/cnnheroes-susan-munsey-generatehope/index.html",
            "/2018/09/13/world/cnnheroes-abisoye-ajayi-akinfolarin-pearls-africa-foundation/index.html",
            "/2018/10/01/europe/chemnitz-neo-nazi-arrests-intl/index.html",
            "/2018/10/01/europe/macedonia-name-referendum/index.html",
            "/2018/09/30/asia/north-korea-moon-kim-dogs-intl/index.html",
            "/2018/10/01/asia/okinawa-governor-us-intl/index.html",
            "/2018/09/30/asia/indonesia-earthquake-controller-intl/index.html",
            "/2018/09/30/world/five-things-september-30-trnd/index.html",
            "/2018/09/29/europe/macedonia-name-referendum-nato-intl/index.html",
            "/2018/09/30/europe/brexit-festival-intl/index.html",
            "/2018/09/29/asia/earthquakes-indonesia-explainer/index.html",
            "/2018/09/29/asia/indonesia-earthquake/index.html",
            "/2018/09/30/middleeast/trump-israelis-palestinians-analysis/index.html",
            "/2018/09/29/asia/typhoon-trami-japan-wxc/index.html",
            "/2018/09/29/asia/air-niugini-micronesia-intl/index.html",
            "/2018/09/29/middleeast/egypt-amal-fathy-activist-sentenced/index.html",
            "/2018/09/29/world/skull-asteroid-halloween-trnd/index.html",
            "/2018/09/29/europe/medicane-zorba-greece-turkey-intl/index.html",
            "/2018/09/28/middleeast/tara-fares-iraq-killed-intl/index.html",
            "/2018/10/01/politics/ice-arrests-immigrant-child-sponsors-legislation/index.html",
            "/2018/10/01/politics/nafta-usmca-differences/index.html",
            "/2018/10/01/politics/police-report-kavanaugh-bar/index.html",
            "/2018/10/01/politics/china-california-space-smuggling-intl/index.html",
            "/2018/10/01/politics/warren-2020-announcement-question/index.html",
            "/2018/10/01/politics/congress-fbi-kavanaugh-white-house/index.html",
            "/2018/10/01/politics/donald-trump-brett-kavanaugh-drinking/index.html",
            "/2018/10/01/politics/nyt-police-kavanaugh-bar-fight/index.html",
            "/2018/10/01/politics/mark-judge-videos/index.html",
            "/2018/10/01/politics/fbi-investigation-kavanaugh-christine-blasey-ford/index.html",
            "/2018/10/01/politics/fbi-kavanaugh-key-witnesses/index.html",
            "/2018/10/01/politics/cnn-polls-missouri-nevada-senate/index.html",
            "/2018/09/29/politics/kavanaugh-fbi-background-investigation/index.html",
            "/2018/09/27/politics/rod-rosenstein-donald-trump-meeting/index.html",
            "/2018/09/25/politics/trump-con-game-kavanaugh-tv/index.html",
            "/2018/10/01/politics/trump-un-global-push-back/index.html",
            "/2018/10/01/politics/donald-trump-brett-kavanaugh-fbi-investigation/index.html",
            "/2018/10/01/politics/trump-china-trade-war-resume-talks/index.html",
            "/2018/10/01/politics/trump-tariffs-congress-trade/index.html",
            "/2018/10/01/politics/donald-trump-drinking/index.html",
            "/2018/10/01/politics/melania-trump-africa/index.html",
            "/2018/09/26/politics/melania-trump-africa/index.html",
            "/2018/09/15/politics/donald-trump-jr-defender/index.html",
            "/2018/10/01/politics/supreme-court-congress-senators-kavanaugh/index.html",
            "/2018/09/30/politics/flake-fbi-kavanaugh-investigation/index.html",
            "/2018/10/01/politics/jeff-flake-60-minutes/index.html",
            "/2018/09/30/politics/mcconnell-julie-swetnick-defamation-suit/index.html",
            "/2018/09/30/politics/amy-klobuchar-stunned-brett-kavanaugh-cnntv/index.html",
            "/2018/09/28/politics/kavanaugh-judiciary-committee-votes/index.html",
            "/2018/10/01/politics/russia-trump-dossier-buzzfeed-court-lawsuit/index.html",
            "/2018/10/01/politics/james-comey-house-gop-interview/index.html",
            "/2018/10/01/politics/white-house-kavanaugh-confirmation-postponement/index.html",
            "/2018/10/01/politics/obama-endorses-ocasio-cortez-gillum-bryce-eastman-jealous/index.html",
            "/2018/10/01/politics/aclu-new-ad-campaign-against-brett-kavanaugh/index.html",
            "/2018/10/01/politics/amanpour-interview-woman-jeff-flake-elevator-cnntv/index.html",
            "/2018/10/01/politics/rnc-2020-convention-announced/index.html",
            "/2018/09/30/politics/deborah-ramirez-fbi-kavanaugh/index.html",
            "/2018/09/30/politics/us-sails-south-china-sea/index.html",
            "/2018/09/27/politics/hackers-warning-midterm-elections/index.html",
            "/2018/09/25/politics/chinese-agent-us-intl/index.html",
            "/2018/09/20/politics/foreign-hackers-target-senators-gmail/index.html",
            "/2018/10/01/politics/china-us-warship-unsafe-encounter/index.html",
            "/2018/09/28/politics/us-consulate-basra-evacuation/index.html",
            "/2018/09/28/politics/marine-corps-f-35b-fighter-crash/index.html",
            "/2018/09/27/politics/us-iran-proxy-concerns/index.html",
            "/2018/09/27/politics/airstrike-afghanistan-first-f-35b/index.html",
            "/2018/10/01/politics/yale-kavanaugh-drinking/index.html",
            "/2018/10/01/politics/yale-kavanaugh-drinking-ludington/index.html",
            "/2018/10/01/politics/supreme-court-kavanaugh-day-one-john-roberts/index.html",
            "/2018/10/01/politics/kavanaugh-poll-quinnipiac-confirmation/index.html",
            "/2018/09/28/politics/supreme-court-partisanship-kavanaugh/index.html",
            "/2018/09/30/politics/trump-nafta-canada/index.html",
            "/2018/10/01/politics/mattis-us-china-ties-intl/index.html",
            "/2018/09/28/politics/netanyahu-labott-interview-unga/index.html",
            "/2018/09/28/politics/china-unga-speech/index.html",
            "/2018/09/27/politics/us-north-korea-meeting-unga-russia-china/index.html",
            "/2018/10/01/politics/menendez-hugin-new-jersey-senate-poll/index.html",
            "/2018/09/30/politics/adam-laxalt-family-endorsement-steve-sisolak/index.html",
            "/2018/09/29/politics/poll-of-the-week-florida-senate-bill-nelson/index.html",
            "/2018/09/26/politics/key-race-that-is-trending-republican/index.html",
            "/2018/09/30/opinions/fbi-investigation-ford-kavanaugh-facts-matter-honig/index.html",
            "/2018/09/30/opinions/presidential-weekly-briefing-north-korea-vinograd/index.html",
            "/2018/09/30/opinions/saturday-night-live-evolution-gop-same-mindset-obeidallah/index.html",
            "/2018/09/29/opinions/the-world-will-regret-laughing-at-trump-robertson-intl/index.html",
            "/2018/09/28/opinions/kavanaugh-hearing-brought-back-assault-jennifer-taub/index.html",
            "/2018/09/27/opinions/ford-kavanaugh-senate-judiciary-hearing-opinion-pate/index.html",
            "/2018/09/30/politics/trump-immigration-women-victims/index.html",
            "/2018/09/21/politics/family-reunifications-southern-border/index.html",
            "/2018/09/20/politics/hhs-shifting-money-cancer-aids-immigrant-children/index.html",
            "/2018/09/20/politics/ice-arrested-immigrants-sponsor-children/index.html",
            "/2018/09/28/politics/opioids-package-passes-house/index.html",
            "/2018/09/27/politics/obamacare-premiums/index.html",
            "/2018/09/26/politics/republicans-health-care-defensive/index.html",
            "/2018/09/25/politics/kentucky-blue-wave-mcgrath-barr/index.html",
            "/2018/09/19/politics/trump-organization-midterm-democrats-investigations/index.html",
            "/2018/09/12/politics/dc-alcohol-license-trump-hotel/index.html",
            "/2018/08/31/politics/trump-foundation-new-york-attorney-general-lawsuit/index.html",
            "/2018/09/26/politics/nafta-us-canada-deadline/index.html",
            "/2018/09/23/politics/trump-trade-war-china/index.html",
            "/2018/09/15/politics/trump-tariffs-china-trade-war/index.html",
            "/2018/09/30/politics/fbi-brett-kavanaugh-investigation/index.html",
            "/2018/09/30/politics/rachel-mitchell-kavanaugh-ford/index.html",
            "/2018/09/29/politics/trump-west-virginia-rally/index.html",
            "/2018/09/30/politics/james-comey-op-ed-fbi-investigation/index.html",
            "/2018/09/29/politics/ford-friend-cooperate-fbi/index.html",
            "/2018/09/28/politics/kavanaugh-senate-judiciary-vote/index.html",
            "/2018/09/26/politics/brett-kavanaugh-1982-calendar/index.html",
            "/2018/09/27/politics/christine-ford-metoo-movement/index.html",
            "/2018/10/02/technology/amazon-minimum-wage/index.html",
            "/2018/10/01/news/companies/ge-ceo-larry-culp-flannery/index.html",
            "/2018/10/01/news/companies/general-electric-ceo-flannery-culp/index.html",
            "/2018/10/01/news/companies/goldman-sachs-david-solomon-ceo/index.html",
            "/2018/10/01/news/companies/beth-ford-boss-files/index.html",
            "/2018/10/01/technology/paul-allen-non-hodgkins-lymphoma/index.html",
            "/2018/10/01/investing/stock-market-today-usmca-ge-tesla-dow/index.html",
            "/2018/10/01/technology/business/tesla-stock/index.html",
            "/2018/09/28/technology/tesla-production/index.html",
            "/2018/10/01/media/jemele-hill-the-atlantic/index.html",
            "/2018/10/02/media/reliable-sources-10-01-18/index.html",
            "/2018/10/01/media/white-house-press-briefing-september/index.html",
            "/2018/09/30/news/california-requires-women-board-of-directors/index.html",
            "/2018/09/30/media/katie-couric-reliable-sources/index.html",
            "/2018/10/01/media/washington-times-aaron-rich/index.html",
            "/2018/09/30/technology/california-net-neutrality-law/index.html",
            "/2018/09/30/investing/stocks-week-ahead-tesla-elon-musk/index.html",
            "/2018/09/29/technology/business/elon-musk-tesla-sec-settlement/index.html",
            "/2018/10/02/investing/premarket-stocks-trading/index.html",
            "/2018/10/01/technology/facebook-hack-tinder-pinterest/index.html",
            "/2018/09/29/technology/facebook-hack-what-to-do-if-youre-affected/index.html",
            "/2018/10/01/technology/instagram-adam-mosseri/index.html",
            "/2018/09/25/technology/instagram-cofounders-facebook/index.html",
            "/2018/07/31/smallbusiness/girlcrew-app/index.html",
            "/2018/09/28/media/myanmar-reuters-journalists-amal-clooney/index.html",
            "/2018/10/01/investing/ryanair-profit-warning/index.html",
            "/2018/09/27/technology/bitcoin-mining-ipo/index.html",
            "/2018/09/20/smallbusiness/agriprotein-fly-farming/index.html",
            "/video/technology/2018/09/19/iphone-xs-max-apple-first-look-orig.cnnmoney/index.html",
            "/video/technology/2018/09/27/elon-musk-sec-lawsuit.cnnmoney/index.html",
            "/video/technology/business/2018/09/28/dreamforce-orig.cnnmoney/index.html",
            "/video/media/2018/09/28/late-night-kavanaugh-hearing-orig-llr.cnnmoney/index.html",
            "/video/technology/2018/09/20/amazon-alexa-microwave.cnnmoney/index.html",
            "/2018/10/02/health/australia-bhutan-conjoined-twins-intl/index.html",
            "/2018/10/01/health/fasting-longevity-food-drayer/index.html",
            "/2018/09/29/health/sex-education-consent-in-public-schools-trnd/index.html",
            "/2018/09/28/health/world-first-rat-disease-hepatitis-e-intl/index.html",
            "/2018/09/28/health/doctors-rally-against-gun-violence/index.html",
            "/2018/09/26/health/flu-deaths-2017--2018-cdc-bn/index.html",
            "/2018/09/27/health/birth-control-ovarian-cancer-risk/index.html",
            "/2018/09/27/health/trigger-empowerment-trauma-blasey-ford/index.html",
            "/2018/10/02/health/african-swine-fever-europe-china-spread-intl/index.html",
            "/2018/10/01/health/groundcherry-berry-study/index.html",
            "/2018/10/01/health/sexual-assault-hotline-record-bn/index.html",
            "/2018/09/26/health/meth-overdoses-increase-oklahoma-mexico-superlabs/index.html",
            "/2018/09/25/health/crispr-gene-drive-mosquitoes-malaria-study/index.html",
            "/2018/09/25/health/medical-marijuana-california-child-school-ruling/index.html",
            "/2018/09/28/health/china-ai-early-education/index.html",
            "/2018/09/27/health/early-christmas-boy-cancer/index.html",
            "/2018/10/01/health/infection-death-hurricane-florence/index.html",
            "/2018/10/01/health/sleep-risky-behavior-teens-study/index.html",
            "/2018/10/01/health/uti-bladder-infections-water-study/index.html",
            "/2018/10/01/health/georgia-high-school-football-player-dies/index.html",
            "/2018/10/01/health/nobel-prize-medicine-2018-intl/index.html",
            "/2018/10/01/health/health-care-education-united-states-27th-world-trnd/index.html",
            "/2018/09/28/health/kentucky-abortion-law-unconstitutional/index.html",
            "/2018/09/25/health/dog-3d-printed-skull-trnd/index.html",
            "/2018/09/24/health/paralyzed-woman-walks-again/index.html",
            "/2018/09/25/health/syphilis-newborns-cdc-study/index.html",
            "/2018/09/27/health/staying-well-rock-climbing/index.html",
            "/2018/09/28/health/cannabis-teen-use-methods-study/index.html",
            "/2018/09/26/health/malawi-abortion-law-as-equals-africa-intl/index.html",
            "/2018/09/28/health/uk-breast-cancer-deaths-will-rise-intl/index.html",
            "/2018/09/28/health/turning-points-blind-swimmer/index.html",
            "/2018/09/27/health/orca-killer-whale-pollution-intl/index.html",
            "/2018/09/26/health/britain-europe-teenage-drinking-alcohol-intl/index.html",
            "/2018/09/21/health/global-alcohol-deaths-who-intl/index.html",
            "/2018/09/26/health/third-monkeypox-case-uk-intl/index.html",
            "/2018/09/27/health/iyw-sexual-assault-help-blasey-ford/index.html",
            "/2018/09/26/health/sexual-assault-reporting-kavanaugh/index.html",
            "/2018/09/13/health/opioid-recovery-love-story/index.html",
            "/2018/09/03/health/claire-wineland-obit/index.html",
            "/2018/08/29/health/live-longer-qigong-health-benefits-intl/index.html",
            "/2018/08/23/health/cara-pressman-surgery-update-aetna/index.html",
            "/2018/08/13/health/mayo-clinic-escape-1-eprise/index.html",
            "/2018/08/13/health/mayo-clinic-escape-2-eprise/index.html",
            "/2018/08/14/health/face-transplant-suicide-attempt-natgeo-profile/index.html",
            "/2018/07/27/health/essure-bayer-doctor-payments-eprise/index.html",
            "/2018/06/28/health/embryos-egg-donor-surrogate/index.html",
            "/2018/06/12/health/pancreas-transplant-diabetes-eprise/index.html",
            "/2018/05/26/health/barkley-marathons-sport-fit-nation/index.html",
            "/2018/05/25/health/turning-points-shalom-blac-burn-survivor-turns-beauty-inspiration/index.html",
            "/2018/05/13/health/liver-transplant-mom-erika-zak/index.html",
            "/2018/05/23/health/claire-wineland-transplant-evaluation/index.html",
            "/2018/04/13/health/athletes-gene-editing-doping-sport-intl/index.html",
            "/2018/04/09/health/parkinsons-drug-nuplazid-invs/index.html",
            "/2018/03/30/health/kentucky-water-crisis/index.html",
            "/2018/02/27/health/functioning-heroin-addicts/index.html",
            "/2018/03/11/health/prescription-opioid-payments-eprise/index.html",
            "/2018/02/11/health/aetna-california-investigation/index.html",
            "/2018/08/30/health/chocolate-chip-cookies-addictive-food-drayer/index.html",
            "/2018/02/01/health/alcohol-health-weight-diabetes-memory-intl/index.html",
            "/2018/08/21/health/unhealthy-vegetarianism-food/index.html",
            "/2018/03/09/health/vegetarian-fast-food-drayer/index.html",
            "/2018/05/21/health/eggs-heart-disease-study/index.html",
            "/2018/03/22/health/calorie-restriction-longer-life-study/index.html",
            "/2018/04/26/health/salt-detox-food-drayer/index.html",
            "/2018/03/23/health/intermittent-fasting-food-drayer/index.html",
            "/2018/03/12/health/improve-health-sugar-partner/index.html",
            "/2018/02/26/health/best-foods-for-heart/index.html",
            "/2018/09/15/health/pack-burro-donkey-sport-fit-nation/index.html",
            "/2018/04/11/health/improve-emotional-intelligence/index.html",
            "/2018/03/14/health/dementia-risk-fitness-study/index.html",
            "/2018/01/03/health/exercise-trends-survey-2018/index.html",
            "/2018/02/01/health/love-handles-exercise-jampolis/index.html",
            "/2018/03/26/health/lose-weight-where-does-it-go-partner/index.html",
            "/2018/05/22/health/leukemia-clean-childhood-study-intl/index.html",
            "/2018/05/21/health/girls-confidence-code-parenting/index.html",
            "/2018/05/03/health/children-movement-schools-classroom/index.html",
            "/2018/03/02/health/childrens-programming-female-empowerment-role-models/index.html",
            "/2018/01/18/health/nfl-no-tackle-football-kids/index.html",
            "/2018/02/26/health/youth-sexting-prevalence-study/index.html",
            "/2018/01/31/health/meaning-of-life-wisdom-project/index.html",
            "/2018/01/05/health/habits-wisdom-project/index.html",
            "/2018/01/05/health/baby-bedtimes-parenting-without-borders-explainer-intl/index.html",
            "/2018/09/28/technology/tesla-stock-analysts/index.html",
            "/2018/09/10/technology/mit-robot-picks-up-objects/index.html",
            "/2018/09/09/technology/business/jack-ma-alibaba-bio/index.html",
            "/2018/09/08/technology/nfl-national-anthem-russia-trolls/index.html",
            "/2018/08/08/technology/deepfakes-countermeasures-facebook-twitter-youtube/index.html",
            "/video/technology/gadgets/2018/09/12/iphone-xs-unveiled.cnnmoney/index.html",
            "/video/technology/2018/09/12/apple-watch-series-4-announcement.cnnmoney/index.html"
    ]
    
    cdn_logs = []
    
    for i in range(iteration_count):
        
        date_year       = 2018
        date_month      = int(random.triangular(7,9.49,9.49))
        date_day        = random.randint(1,30)
        date_hour       = random.randint(0,23)
        date_minute     = random.randint(0,57)
        date_second     = random.randint(0,59)
        simulated_date  = (date_year, date_month, date_day if date_month!=9 else int(random.triangular(1,30,5)), date_hour, date_minute, date_second, 1,1,1 )
        unix_datetime   = int(time.mktime( simulated_date )) #datetime.datetime.now().timetuple()))
        elaspsed_time   = int(random.triangular(0,100, 50))
        
        xcache_state = random.choice(['MISS']*8 + ['HIT']*2)
        
        cdn_log =  ''
        cdn_log += 't_now={} '.format( unix_datetime )
        cdn_log += 't_elapsed={} '.format( elaspsed_time )
        cdn_log += 't_ttfb={} '.format( round((int(random.triangular(0,100,20)) / 1000), 4) )
        cdn_log += 't_start={} '.format( unix_datetime - elaspsed_time )
        cdn_log += 't_end={} '.format( unix_datetime )
        cdn_log += 'req_ip={} '.format( '104.237.{}.{}'.format(random.randint(1,254), random.randint(1,254)) )
        cdn_log += 'req_method={} '.format( 'GET' )
        cdn_log += 'req_host={} '.format( 'www.cnn.com' )
        #cdn_log+= 'req_url={} '.format( '/2018/09/{}/{}/'.format( random.randint(10,30), random.choice(['us','world','politics','opinions','health','entertainment','tech','style','travel','sports']) ) )
        cdn_log += 'req_url={} '.format( urls[int(random.triangular(0,len(urls)-2,1))] )
        cdn_log += 'resp_status={} '.format( random.choice( [200]*80 + [404]*20 ) )
        cdn_log += 'resp_size={} '.format( int(random.triangular(200, 175000, 2000)) )
        cdn_log += 'resp_age={} '.format( 0 )
        cdn_log += 'resp_xcache={} '.format( xcache_state )
        cdn_log += 'resp_setcookie={} '.format( 1 )
        cdn_log += 'req_ua={} '.format( random.choice(user_agents) )
        cdn_log += 'req_ref={} '.format( 'https://www.cnn.com' )
        cdn_log += 'resp_xcache={} '.format( xcache_state )
        cdn_log += 'fastly_pop={} '.format( 'IAD' )
        cdn_log += 'fastly_shield={} '.format( 1 )
        cdn_log += 'fastly_region={} '.format( 'US-East' )
        cdn_log += 'fastly_state={} '.format( '{}-CLUSTER'.format(xcache_state) )
        cdn_log += 'fastly_hits={} '.format( 0 if xcache_state=='MISS' else 1 )
        cdn_log += 'fastly_restarts={} '.format( 0 )
        cdn_log += 'geo_continent={} '.format( 'continent' )
        cdn_log += 'geo_country={} '.format( random.choice( countries ) )
        cdn_log += 'geo_region={}'.format( 'region' )
        
        cdn_logs.append(cdn_log)
    
    cdn_log_count = len(cdn_logs)
    cdn_logs      = '\n'.join( cdn_logs )
    print('[ INFO ] Simulated {} records'.format(cdn_log_count) )
    return cdn_logs, cdn_log_count



# Write cdn_logs string blob storage in Google Cloud Storage
def write_str_to_gcs(bucket_name, blob_str):
    '''
        Write blob string to Google Cloud Storage
    '''
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    #encryption_key = 'c7f32af42e45e85b9848a6a14dd2a8f6'
    bucket_filename = 'cdn_log_{}.txt'.format( datetime.datetime.now().strftime('%Y%m%d_%H%M%S') )
    blob = Blob(bucket_filename, bucket) # encryption_key=encryption_key)
    blob.upload_from_string( blob_str )
    print('[ INFO ] Wrote cdn logs to gs://{}/{}'.format(bucket_name, bucket_filename) )



if __name__ == "__main__":
    
    # Arguments - Only used for testing
    #args =  {
    #            "bucket_name": "cdn_logs_z2018",
    #            "iteration_count": 100
    #        }
    
    # Arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--bucket_name",     required=True, type=str, help="Google Cloud Storage bucket name")
    ap.add_argument("--iteration_count", required=True, type=int, help="Number of CDN logs to simulate")
    args = vars(ap.parse_args())
    
    # Simulate CDN Logs
    cdn_logs, cdn_log_count = simulate_cdn_logs( args['iteration_count'] )
    
    # # Write cdn_logs string blob storage in Google Cloud Storage
    write_str_to_gcs(args['bucket_name'], cdn_logs)
    
    print('[ INFO ] Simulation Complete')



#ZEND
