import json
import sys
import time
import urllib.request
import urllib.error
import locale
import pyttsx3
from sys import platform
from playsound import playsound
from mtranslate import translate

def run(sUrl, iDisplay=0, bAlert=False, bSpeech=False, bWait=False):
	"""
	Run()
    --------------------------------------------------------------------------------------
    Keyword arguments:
	--------------------------------------------------------------------------------------
    sUrl 		-- 	String 	-- Nightscout url 
    iDisplay 	-- 	Integer -- Option of print glucose data (0=All, 1=Glucose, 2=Direction, 3=Delta, 4=Minutes)
	bAlert		-- 	Boolean -- Alarm option (True or False)
	bSpeech		-- 	Boolean -- Speech option, with wait every zero min. (True or False)
	bWait		-- 	Boolean	-- Waiting time with a loop (True or False)
    --------------------------------------------------------------------------------------
    Example:	while 1:
					ns.run('https://account.herokuapp.com', 0, True, True, True)
	--------------------------------------------------------------------------------------
    """
	# Load JSON from url
	try:
		urlEntries = urllib.request.urlopen(sUrl + str('/api/v1/entries/sgv.json?count=2'))
		jsonEntries = json.load(urlEntries)
		urlStatus = urllib.request.urlopen(sUrl + str('/api/v1/status.json'))
		jsonStatus = json.load(urlStatus)
	except urllib.error.HTTPError as e:
		print(str('HTTP-Error: ') + str(e.code))
		sys.exit()
	except urllib.error.URLError as e:
		print(str('URL-Error: ') + str(e.args))
		sys.exit()

	# Read glucose values
	iSgv = int(jsonEntries[0]['sgv'])
	iLastSgv = int(jsonEntries[1]['sgv'])

    # Read unix date values diff
	iDate = int(jsonEntries[0]['date'])
	iLastDate = int(jsonEntries[1]['date'])
	iServerTimeEpoch = int(jsonStatus['serverTimeEpoch'])

	# Calculate and strings
	iMsServerTimeEpochDate = int(iServerTimeEpoch - iDate)
	iMsInterval = int(iDate - iLastDate)
	iMinInterval = int(round(iMsInterval / 60000 + 1, 0))
	iMinSecondInterval = int(iMinInterval * 2)
	iMin = int(iMsServerTimeEpochDate / 60000)

	# Calculate waiting time for glucose update
	fMin = float(iMsServerTimeEpochDate / 60000)
	fMinDiff = float(str(fMin)[1:])
	iMsWait = int(fMinDiff * 60000)
	if fMinDiff < 0.5:
		iMsWait = int(60000 - iMsWait)

	# Alarm with int values
	iBgHigh = int(jsonStatus['settings']['thresholds']['bgHigh'])
	iBgTargetTop = int(jsonStatus['settings']['thresholds']['bgTargetTop'])
	iBgTargetBottom = int(jsonStatus['settings']['thresholds']['bgTargetBottom'])
	iBgLow = int(jsonStatus['settings']['thresholds']['bgLow'])

	# String values
	sStatus = str(jsonStatus['status'])
	sUnits = str(jsonStatus['settings']['units'])

	# Check status of Nightscout
	if str('ok') not in sStatus:
		print(str('Status: [' + sStatus + ']'))

    # Check if sUnits: mmol
	i_fSgv = ''
	i_fLastSgv = ''
	if sUnits == str('mmol'):
		i_fSgv = round(float(iSgv * 0.0555), 1)
		i_fLastSgv = round(float(iLastSgv * 0.0555), 1)
	else:
		i_fSgv = iSgv
		i_fLastSgv = iLastSgv

    # Calculate delta
	sTmpDelta = ''
	i_fDelta = float(i_fSgv - i_fLastSgv)
	sTmpDelta = str(i_fDelta)
	sDirection = str(jsonEntries[0]['direction'])
	if i_fSgv < i_fLastSgv:
		if sDirection == str('FortyFiveUp') or sDirection == str('SingleUp') or sDirection == str('DoubleUp'):
			sTmpDelta = sTmpDelta.replace('-', '')
			i_fDelta = float(sTmpDelta)

	sDelta = ''
	if i_fDelta > 0:
		sDelta = str('+')
	if i_fDelta == 0:
 		sDelta = str('±')

	if sUnits == str('mg/dl'):
		i_fDelta = int(i_fDelta)
	else:
		i_fDelta = round(i_fDelta, 1)

	# Direction
	sTrend = ''
	sSpeechTrend = ''
	if sDirection == str("DoubleUp"):
		sTrend = str("⇈")
		sSpeechTrend = str('Tendency: rising fast')
	if sDirection == str("Flat"):
		sTrend = str("→︎")
		sSpeechTrend = str('Tendency: constant')
	if sDirection == str("SingleUp"):
		sTrend = str("↑")
		sSpeechTrend = str('Tendency: rising')
	if sDirection == str("FortyFiveUp"):
		sTrend = str("↗")
		sSpeechTrend = str('Tendency: slightly rising')
	if sDirection == str("FortyFiveDown"):
		sTrend = str("↘")
		sSpeechTrend = str('Tendency: sinks slightly')
	if sDirection == str("SingleDown"):
		sTrend = str("↓")
		sSpeechTrend = str('Tendency: sinks')
	if sDirection == str("DoubleDown"):
		sTrend = str("⇊")
		sSpeechTrend = str('Tendency: sinks quickly')

	# Detect local language
	sTmpLang = str(locale.getdefaultlocale())[:4]
	sLanguageDetect = sTmpLang[-2:]
	sSpeechTrend = translate(sSpeechTrend, sLanguageDetect, 'auto')

    # Notification
	sMin = str(iMin) + str(' min')
	sDelta = sDelta + str(i_fDelta)
	sGlucoseData = str(i_fSgv) + str(' • ') + sTrend + str(' • ') + sDelta + str(' • ') + sMin

	# Logic for display glucose and speech
	sDisplay = '' 
	if iDisplay == int(0):
		sDisplay = sGlucoseData
		print(sDisplay)
		if bSpeech == True:
			sDisplay = sDisplay.replace(sTrend, sSpeechTrend)
	if iDisplay == int(1):
		sDisplay = str(i_fSgv)	
		print(sDisplay)
	if iDisplay == int(2):
		sDisplay = sTrend
		print(sDisplay)
		if bSpeech == True:
			sDisplay = sSpeechTrend
	if iDisplay == int(3):
		sDisplay = sDelta
		print(sDisplay)
	if iDisplay == int(4):
		sDisplay = sMin
		print(sDisplay)

	# Speech engine
	engine = ''
	if bSpeech == True and bWait == True and iMin == 0:
		if platform == str("linux") or platform == str("linux2"):
			from google_speech import Speech
			engine = Speech(sDisplay.replace('.', ','), sLanguageDetect)
			engine.play()
		else:
			engine = pyttsx3.init()
			engine.say(sDisplay.replace('.', ','))
			engine.runAndWait()
		#if platform == str("win32") or platform == str("win64"): => WIN
		#if platform == str("darwin"): => MACOS

	if bSpeech == True and bWait == False:
		if platform == str("linux") or platform == str("linux2"):	
			from google_speech import Speech	
			engine = Speech(sDisplay.replace('.', ','), sLanguageDetect)
			engine.play()
		else:
			engine = pyttsx3.init()
			engine.say(sDisplay.replace('.', ','))
			engine.runAndWait()
		#if platform == str("win32") or platform == str("win64"): => WIN
		#if platform == str("darwin"): => MACOS

	# Alerts
	if bAlert == True and bWait == False:
		if iSgv <= iBgLow or iSgv >= iBgHigh or iSgv <= iBgTargetBottom or iSgv >= iBgTargetTop:
			playsound(sUrl + '/audio/alarm.mp3')
	if bAlert == True and bWait == True and iMin == 0:
		if iSgv <= iBgLow or iSgv >= iBgHigh or iSgv <= iBgTargetBottom or iSgv >= iBgTargetTop:
			playsound(sUrl + '/audio/alarm.mp3')

	if bWait == True:
		time.sleep(int(iMsWait * 0.001))
		
	# Check of glucose after every interval for new updates
	if sMin.endswith(str(iMinInterval)[-1:]) or sMin.endswith(str(iMinSecondInterval)[-1:]):
		for i in range(10):
			time.sleep(int(1))
			if iMin == 0:
				break

	# Close url
	urlEntries.close()
	urlStatus.close()