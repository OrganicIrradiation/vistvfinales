from imdb import IMDb
import numpy as np
import matplotlib.pyplot as plt
import pprint
import cPickle
import os
import os.path

PROCESSQUEUEPATH = 'pyIMDBShowRatingComparison.p'

def sortedSeasons(m):
    """Return a sorted list of seasons of the given series."""
    seasons = m.get('episodes', {}).keys()
    seasons.sort()
    return seasons

def sortedEpisodes(m, season=None):
    """Return a sorted list of episodes of the given series,
    considering only the specified season(s) (every season, if None)."""
    episodes = []
    seasons = season
    if season is None:
        seasons = sortedSeasons(m)
    else:
        if not isinstance(season, (tuple, list)):
            seasons = [season]
    for s in seasons:
        eps_indx = m.get('episodes', {}).get(s, {}).keys()
        eps_indx.sort()
        for e in eps_indx:
            episodes.append(m['episodes'][s][e])
    return episodes

print 'Loading submissions that have already been processed'
if os.path.isfile(PROCESSQUEUEPATH):
    # Delete the PROCESSQUEUEPATH file if you want to redownload the rating scores
    theData = cPickle.load(open(PROCESSQUEUEPATH, 'rb'))
else:
    theData =   [{'ID': '0285331', 'Name': '24'},
                 {'ID': '0066626', 'Name': 'All in the Family'},
                 {'ID': '0285333', 'Name': 'Alias'},
                 {'ID': '0367279', 'Name': 'Arrested Development'},
                 {'ID': '0076984', 'Name': 'Battlestar Galactica (1978-1979)'},
                 {'ID': '0407362', 'Name': 'Battlestar Galactica (2004-2009)'},
                 {'ID': '0185906', 'Name': 'Band of Brothers'},
                 {'ID': '0105958', 'Name': 'Boy Meets World'},
                 {'ID': '0903747', 'Name': 'Breaking Bad'},
                 {'ID': '0758737', 'Name': 'Brothers & Sisters'},
                 {'ID': '0118276', 'Name': 'Buffy the Vampire Slayer'},
                 {'ID': '0083399', 'Name': 'Cheers'},
                 {'ID': '0934814', 'Name': 'Chuck'},
                 {'ID': '0077000', 'Name': 'Dallas (1978-1991)'},
                 {'ID': '0410975', 'Name': 'Desperate Housewives'},
                 {'ID': '0773262', 'Name': 'Dexter'},
                 {'ID': '0387199', 'Name': 'Entourage'},
                 {'ID': '0108757', 'Name': 'ER'},
                 {'ID': '0115167', 'Name': 'Everybody Loves Raymond'},
                 {'ID': '0106004', 'Name': 'Frasier'},
                 {'ID': '0108778', 'Name': 'Friends'},
                 {'ID': '1119644', 'Name': 'Fringe'},
                 {'ID': '0083413', 'Name': 'Family Ties'},
                 {'ID': '0108778', 'Name': 'Friends'},
                 {'ID': '0149460', 'Name': 'Futurama'},
                 {'ID': '0813715', 'Name': 'Heroes'},
                 {'ID': '0101120', 'Name': 'Home Improvement'},
                 {'ID': '0412142', 'Name': 'House M.D.'},
                 {'ID': '0460649', 'Name': 'How I Met Your Mother'},
                 {'ID': '0106057', 'Name': 'Lois & Clark: The New Adventures of Superman'},
                 {'ID': '0411008', 'Name': 'Lost'},
                 {'ID': '0068098', 'Name': 'M*A*S*H'},
                 {'ID': '0080240', 'Name': 'Magnum, P.I.'},
                 {'ID': '0460091', 'Name': 'My Name is Earl'},
                 {'ID': '0361217', 'Name': 'Nip/Tuck'},
                 {'ID': '0455275', 'Name': 'Prison Break'},
                 {'ID': '0491738', 'Name': 'Psych'},
                 {'ID': '0094540', 'Name': 'Roseanne'},
                 {'ID': '0285403', 'Name': 'Scrubs'},
                 {'ID': '0098904', 'Name': 'Seinfeld'},
                 {'ID': '0159206', 'Name': 'Sex and the City'},
                 {'ID': '0248654', 'Name': 'Six Feet Under'},
                 {'ID': '0279600', 'Name': 'Smallville'},
                 {'ID': '1442449', 'Name': 'Spartacus: War of the Damned'},
                 {'ID': '0244365', 'Name': 'Star Trek: Enterprise'},
                 {'ID': '0092455', 'Name': 'Star Trek: The Next Generation'},
                 {'ID': '0112178', 'Name': 'Star Trek: Voyager'},
                 {'ID': '0118480', 'Name': 'Stargate SG-1'},
                 {'ID': '0374455', 'Name': 'Stargate: Atlantis'},
                 {'ID': '1286039', 'Name': 'Stargate: Universe'},
                 {'ID': '0086687', 'Name': 'The Cosby Show'},
                 {'ID': '0056757', 'Name': 'The Fugitive'},
                 {'ID': '0330251', 'Name': 'The L Word'},
                 {'ID': '0290978', 'Name': 'The Office (UK)'},
                 {'ID': '0386676', 'Name': 'The Office (US)'},
                 {'ID': '0374463', 'Name': 'The Pacific'},
                 {'ID': '0286486', 'Name': 'The Shield'},
                 {'ID': '0141842', 'Name': 'The Sopranos'},
                 {'ID': '0306414', 'Name': 'The Wire'},
                 {'ID': '0106179', 'Name': 'The X Files'}]

# Start up IMDbPY
i = IMDb()

# Load the rating information if it was not already processed
for currentShow in theData:
    if not 'ratingSeries' in currentShow:
        m = i.get_movie(currentShow['ID'])
        currentShow['ratingSeries'] = m['rating']
    if not 'ratingLastEpisode' in currentShow:
        m = i.get_movie(currentShow['ID'])
        i.update(m, 'episodes')
        lastSeason = sortedSeasons(m)[-1]
        lastEpisode = sortedEpisodes(m, season=lastSeason)[-1]
        i.update(lastEpisode, 'main')
        currentShow['ratingLastEpisode'] = lastEpisode['rating']

    cPickle.dump(theData, open(PROCESSQUEUEPATH, 'wb'))

## Sort the data by show rating
theData = sorted(theData, key=lambda k: k['ratingSeries'])
## Other sorting possibilities
# theData = sorted(theData, key=lambda k: k['ratingLastEpisode'])
# theData = sorted(theData, key=lambda k: (k['ratingLastEpisode']-k['ratingSeries']))
# theData = reversed(sorted(theData, key=lambda k: k['Name']))

## Plot the data
labels = []
yVal = 0
fig = plt.figure(num=1, figsize=(5, 9))
ax = plt.gca()
## For each show, add the name to the list of y labels, create an arrow from the average rating
## to the rating of the finale (colored red if the finale was lower than the average and green
## if it was higher), and plot a black circle for the average rating.
for currentShow in theData:
    labels.append(currentShow['Name'])
    yVal=yVal+1
    if currentShow['ratingLastEpisode'] > currentShow['ratingSeries']:
        ax.arrow(currentShow['ratingSeries'],yVal,
                  currentShow['ratingLastEpisode']-currentShow['ratingSeries'],0,color='g',
                  head_width=0.25, head_length=0.125,length_includes_head=True)
    elif currentShow['ratingLastEpisode'] < currentShow['ratingSeries']:
        ax.arrow(currentShow['ratingSeries'],yVal,
                  -(currentShow['ratingSeries']-currentShow['ratingLastEpisode']),0,color='r',
                  head_width=0.25, head_length=0.125,length_includes_head=True)
    ax.plot(currentShow['ratingSeries'],yVal,'ok',markersize=4)
## Set the axis parameters
ax.axis([4.0,10.0,0.0,yVal+1.0])
ax.set_aspect('auto')
ax.set_yticks(range(1,len(labels)+1))
ax.set_yticklabels(labels, fontsize=8, va='bottom')
plt.tight_layout()

# Explanatory text
fig.text(0.025, 0.975, '''IMDB.com ratings of
television shows\'
series finales
relative to
average
show
ratings

Sorted by
show rating''',
         fontsize=12, color='black', weight='bold', ha='left', va='top', alpha=1, transform=ax.transAxes)
# Add some additional info
plt.text(-0.05, 0, '/u/ChallengeResponse - Inspired by figure by @PhJulien - CC BY-NC-SA',
         fontsize=6, color='black', ha='right', va='top', alpha=0.5, transform=ax.transAxes)

# Show the plot
plt.show()
