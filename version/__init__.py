VERSION = 'DEV_VERSION'
try:
  versionFile = open("VERSION_FILE", "r")
  VERSION = versionFile.read().strip()
except:
  pass
