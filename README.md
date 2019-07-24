# GlucoPy
A glucose python module for Nightscout

## Modules
### Windows
* `pip install pyttsx3`
### Linux
* `pip install google-speech`
### Alert option
* `pip install playsound`
### Speech option
* `pip install translate`
* `pip install locale`

## Example
* Run nightscout in console with a loop
```python 
import nightscout as ns

while 1:
  ns.run('https://[...].herokuapp.com', 0, 0, True, True, True) 
  ```
## Keywords
### Run()
#### sUrl
* String: Nightscout url
* `https://[...].herokuapp.com` = URL
#### iUnit
* Integer: Units of glucose
* 0=Auto, 1=mg/dl, 2=mmol
#### iDisplay
* Integer: Option of print glucose data
* `0` = All, `1`= Glucose, `2` = Direction, `3` = Delta, `4` = Minutes
#### bAlert
* Boolean: Alarm option 
* `True` or `False`
#### bSpeech
* Boolean: Speech option, with wait every zero min.
* `True` or `False`
#### bWait
* Boolean: Wait for glucose update
* `True` or `False`
