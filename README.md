# GlucoPy
A glucose python module for Nightscout

## Install modules
* `pip install pyttsx3`
* `pip install playsound`
* `pip install translate`
* `pip install locale`

## Example
* Run nightscout in console with a loop
```python 
import nightscout as ns

while 1:
  ns.run('https://[...].herokuapp.com', 0, True, True, True) 
  ```
## Keywords
### Run()
#### sUrl
* String: Nightscout url
* `https://[...].herokuapp.com` = URL
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
* Boolean: Waiting for glucose update in a loop
* `True` or `False`
