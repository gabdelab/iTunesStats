import argparse
from enum import Enum
import operator
from pyItunes import Library


class Options(Enum):

   ALBUM = 'album'

   ARTIST = 'artist'

   @classmethod
   def getAllValues(cls):
    return [method for method in dir(cls) if callable(getattr(cls, method))]


def groupByAlbums(plSongs, piStartYear, piEndYear, piNbResults=10):
  ldAlbums = {}
  for loSong in plSongs:
    if piStartYear > loSong.year or loSong.year > piEndYear:
      continue
    if not loSong.play_count:
      continue
    try:
      ldAlbums[loSong.album] += loSong.play_count
    except KeyError:
      ldAlbums[loSong.album] = loSong.play_count
  return sorted(ldAlbums.items(), key=operator.itemgetter(1), reverse=True)[:piNbResults]


def groupByArtists(plSongs, piStartYear, piEndYear, piNbResults=10):
  ldArtists = {}
  for loSong in plSongs:
    if piStartYear > loSong.year or loSong.year > piEndYear:
      continue
    if not loSong.play_count:
      continue
    try:
      ldArtists[loSong.artist] += loSong.play_count
    except KeyError:
      ldArtists[loSong.artist] = loSong.play_count
  return sorted(ldArtists.items(), key=operator.itemgetter(1), reverse=True)[:piNbResults]


def pretty_print(plResults):
  """Prints correctly a list of sorted tuples ('name', counter)"""
  lsOutput = "Results : \n"
  liCounter = 1
  for loResult in plResults:
    lsOutput += "%s: %s - %s\n" % (liCounter, loResult[0], loResult[1])
    liCounter += 1
  print lsOutput

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Analyse your iTunes library.')
  parser.add_argument('-o', dest="option", type=str, required=True, choices=['album', 'artist'],
                      help='Option (artist - album)')
  parser.add_argument('-s', dest="start", type=int, default=-10000, help='Start date')
  parser.add_argument('-e', dest='end', type=int, default=10000, help='End date')
  parser.add_argument('-n', dest='nb_results', type=int, default=10, help='Number of results')
  parser.add_argument('-f', dest='xml_file', type=str, default="stats.xml",
                      help='Path to the iTunes xml file.')
  args = parser.parse_args()

  l = Library("stats.xml")
  if args.option == 'album':
    pretty_print(groupByAlbums(l.songs.values(), args.start, args.end, args.nb_results))
  if args.option == 'artist':
    pretty_print(groupByArtists(l.songs.values(), args.start, args.end, args.nb_results))
