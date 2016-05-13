# Python 3.4

from flask import Flask
import requests, json, calendar
from bs4 import BeautifulSoup
from collections import deque


query_params = {
  "originCode"                   : 56,
  "destinationCode"              : 187,
  "outboundDepartureDate"        : "28/01/2016",
  "passengerCount"               : 1,}
'''  "inboundDepartureDate"         : "",
  "transportType"                : -1,
  "concessionCount"              : 0,
  "nusCount"                     : 0,
  "outboundWheelchairSeated"     : 0,
  "outboundOtherDisabilityCount" : 0,
  "inboundWheelchairSeated"      : 0,
  "inboundOtherDisabilityCount"  : 0,
  "outboundPcaCount"             : 0,
  "inboundPcaCount"              : 0,
  "promotionCode"                : 0,
  "withReturn"                   : 0,'''

journey_url = "http://uk.megabus.com/JourneyResults.aspx"


def get_destinations(place_name):
  post_form_data = {
    "UserStatus$ScriptManager1"                             :"JourneyPlanner$UpdatePanel1|JourneyPlanner$ddlLeavingFrom",
    "UserStatus_ScriptManager1_HiddenField"                 :"",
    "__EVENTTARGET:JourneyPlanner$ddlLeavingFrom"           :"",
    "__EVENTARGUMENT"                                       :"",
    "__LASTFOCUS"                                           :"",
    "__VIEWSTATE"                                           :"/wEPDwUJMjAxOTg2MjQ3D2QWAgIBD2QWDAIED2QWBAICDw8WAh4EVGV4dAUfV2VsY29tZSwgWW91IGFyZSBub3QgbG9nZ2VkIGluLmRkAgYPDxYCHwAFEFZpZXcgIEJhc2tldCAoMClkZAIGD2QWJAIDDw8WAh8ABQdFbmdsaXNoZGQCBQ8PFgYeCENzc0NsYXNzBSBmbGFnLWljb24gZmxhZy11ayB0b29sdGlwIGFjdGl2ZR4LTmF2aWdhdGVVcmwFTGh0dHA6Ly93d3cubWVnYWJ1cy5jb20vbGFuZ3VhZ2UuYXNoeD9jbj11ayZsbj1lbiZwYXRoPWRlZmF1bHQuYXNweCZzZWM9RmFsc2UeBF8hU0ICAmRkAgcPDxYCHwIFTGh0dHA6Ly93d3cubWVnYWJ1cy5jb20vbGFuZ3VhZ2UuYXNoeD9jbj1iZSZsbj1ubCZwYXRoPWRlZmF1bHQuYXNweCZzZWM9RmFsc2VkZAIJDw8WAh8CBUxodHRwOi8vd3d3Lm1lZ2FidXMuY29tL2xhbmd1YWdlLmFzaHg/Y249YmUmbG49bmwmcGF0aD1kZWZhdWx0LmFzcHgmc2VjPUZhbHNlZGQCCw8PFgIfAgVMaHR0cDovL3d3dy5tZWdhYnVzLmNvbS9sYW5ndWFnZS5hc2h4P2NuPWJlJmxuPWZyJnBhdGg9ZGVmYXVsdC5hc3B4JnNlYz1GYWxzZWRkAg0PDxYCHwIFTGh0dHA6Ly93d3cubWVnYWJ1cy5jb20vbGFuZ3VhZ2UuYXNoeD9jbj1mciZsbj1mciZwYXRoPWRlZmF1bHQuYXNweCZzZWM9RmFsc2VkZAIPDw8WAh8CBUxodHRwOi8vd3d3Lm1lZ2FidXMuY29tL2xhbmd1YWdlLmFzaHg/Y249ZGUmbG49ZGUmcGF0aD1kZWZhdWx0LmFzcHgmc2VjPUZhbHNlZGQCEQ8PFgIfAgVMaHR0cDovL3d3dy5tZWdhYnVzLmNvbS9sYW5ndWFnZS5hc2h4P2NuPW5sJmxuPW5sJnBhdGg9ZGVmYXVsdC5hc3B4JnNlYz1GYWxzZWRkAhMPDxYCHwIFTGh0dHA6Ly93d3cubWVnYWJ1cy5jb20vbGFuZ3VhZ2UuYXNoeD9jbj1lcyZsbj1lcyZwYXRoPWRlZmF1bHQuYXNweCZzZWM9RmFsc2VkZAIVDw8WAh8CBUxodHRwOi8vd3d3Lm1lZ2FidXMuY29tL2xhbmd1YWdlLmFzaHg/Y249ZXMmbG49ZXMmcGF0aD1kZWZhdWx0LmFzcHgmc2VjPUZhbHNlZGQCFw8PFgIfAgVMaHR0cDovL3d3dy5tZWdhYnVzLmNvbS9sYW5ndWFnZS5hc2h4P2NuPWVzJmxuPWNhJnBhdGg9ZGVmYXVsdC5hc3B4JnNlYz1GYWxzZWRkAhkPDxYCHwIFTGh0dHA6Ly93d3cubWVnYWJ1cy5jb20vbGFuZ3VhZ2UuYXNoeD9jbj1pdCZsbj1pdCZwYXRoPWRlZmF1bHQuYXNweCZzZWM9RmFsc2VkZAIbDw8WAh8CBUBodHRwOi8vd3d3Lm1lZ2FidXMuY29tL2xhbmd1YWdlLmFzaHg/Y249dXMmbG49ZW4mcGF0aD0mc2VjPUZhbHNlZGQCHQ8PFgIfAgVAaHR0cDovL3d3dy5tZWdhYnVzLmNvbS9sYW5ndWFnZS5hc2h4P2NuPXVzJmxuPWVuJnBhdGg9JnNlYz1GYWxzZWRkAh8PDxYCHwIFQGh0dHA6Ly93d3cubWVnYWJ1cy5jb20vbGFuZ3VhZ2UuYXNoeD9jbj11cyZsbj1lcyZwYXRoPSZzZWM9RmFsc2VkZAIhDw8WAh8CBUBodHRwOi8vd3d3Lm1lZ2FidXMuY29tL2xhbmd1YWdlLmFzaHg/Y249Y2EmbG49ZW4mcGF0aD0mc2VjPUZhbHNlZGQCIw8PFgIfAgVAaHR0cDovL3d3dy5tZWdhYnVzLmNvbS9sYW5ndWFnZS5hc2h4P2NuPWNhJmxuPWVuJnBhdGg9JnNlYz1GYWxzZWRkAiUPDxYCHwIFQGh0dHA6Ly93d3cubWVnYWJ1cy5jb20vbGFuZ3VhZ2UuYXNoeD9jbj1jYSZsbj1mciZwYXRoPSZzZWM9RmFsc2VkZAIMD2QWBAIBD2QWAmYPZBYYAgUPZBYCAgEPFgIeB1Zpc2libGVoZAIHDw8WAh8ABQEwFgIeCm9uS2V5UHJlc3MFHHJldHVybiBJc051bWVyaWMoZXZlbnQsdGhpcylkAgkPFgIfBGcWAgIDDw9kFgIfBQUccmV0dXJuIElzTnVtZXJpYyhldmVudCx0aGlzKWQCCw8WAh8EZxYCAgMPD2QWAh8FBRxyZXR1cm4gSXNOdW1lcmljKGV2ZW50LHRoaXMpZAIPDxYCHwRnFgJmDxYEHgVjbGFzcwUXc3RhdGVwcm92aW5jZSAgY2xlYXJmaXgeBXN0eWxlBRliYWNrZ3JvdW5kLWNvbG9yOiNFNEU0RTQ7FgYCAQ8PFgIfAAUHQ291bnRyeWRkAgMPEA8WBh4FV2lkdGgbAAAAAACAXEABAAAAHgtfIURhdGFCb3VuZGcfAwKAAmQQFQsDQWxsB0JlbGdpdW0HRW5nbGFuZAZGcmFuY2UHR2VybWFueQVJdGFseQtOZXRoZXJsYW5kcxNSZXB1YmxpYyBvZiBJcmVsYW5kCFNjb3RsYW5kBVNwYWluBVdhbGVzFQsBMAE1ATEBNgE4AjExATcBNAEyATkBMxQrAwtnZ2dnZ2dnZ2dnZxYBZmQCBQ8WAh8EZxYCAgEPFgIeCWlubmVyaHRtbAWkAm1lZ2FidXMuY29tIGhhcyBjb21lIGEgbG9uZyB3YXkgc2luY2UgaXRzIGxhdW5jaCBpbiAyMDAzLCBhbmQgd2UgYXJlIG5vdyBwcm91ZCB0byBzZXJ2ZSBvdmVyIDEwMCBkZXN0aW5hdGlvbnMgaW4gdGhlIFVLIGFuZCBNYWlubGFuZCBFdXJvcGUuIFRvIG1ha2Ugb3VyIGluY3JlYXNpbmdseSBsb25nIG9yaWdpbiBsaXN0IGVhc2llciB0byBuYXZpZ2F0ZSB3ZSBoYXZlIGFkZGVkIHRoaXMgbmV3IG9wdGlvbmFsIGNvdW50cnkgZmlsdGVyLiBXZSBob3BlIHlvdSBmaW5kIHRoaXMgbmV3IGZlYXR1cmUgaGVscGZ1bC5kAhUPEA8WBB8JZx4HRW5hYmxlZGhkEBW6AQZTZWxlY3QIQWJlcmRlZW4LQWJlcnlzdHd5dGgGQW1pZW5zCUFtc3RlcmRhbQZBbmdlcnMHQW50d2VycAhBdmllbW9yZQdBdmlnbm9uCUF4bWluc3RlcgdCYW5idXJ5CUJhcmNlbG9uYQhCYXJuc2xleQhCYXRoIFNwYQdCZWRmb3JkBkJlcmxpbgpCaXJtaW5naGFtIEJpcm1pbmdoYW0gSW50ZXJuYXRpb25hbCBBaXJwb3J0CUJsYWNrYnVybgdCb2xvZ25hBkJvbHRvbghCb3JkZWF1eAdCb3VyZ2VzC0JvdXJuZW1vdXRoCEJyYWRmb3JkBkJyZW1lbghCcmlnaHRvbgdCcmlzdG9sD0JyaXN0b2wgKEF6dGVjKRlCcmlzdG9sIChDcmliYnMgQ2F1c2V3YXkpEEJyaXN0b2wgKEZpbHRvbikPQnJpc3RvbCBBaXJwb3J0C0JyaXN0b2wgVVdFEkJyaXZlLWxhLUdhaWxsYXJkZQhCcnVzc2VscwhDYW1ib3JuZQlDYW1icmlkZ2UKQ2FudGVyYnVyeQdDYXJkaWZmCkNhcm1hcnRoZW4KQ2FzdGxlZm9yZA1DaGF0ZWxsZXJhdWx0CkNoZWx0ZW5oYW0HQ2hlc3RlcgxDaGVzdGVyZmllbGQQQ2xlcm1vbnQgRmVycmFuZApDb2xjaGVzdGVyB0NvbG9nbmUIQ292ZW50cnkHQ3Jhd2xleQtDdW1iZXJuYXVsZAdDd21icmFuCERhdmVudHJ5BURlcmJ5BURpam9uCURvbmNhc3RlcghEb3J0bXVuZAZEdW5kZWULRHVuZmVybWxpbmUMRWFzdCBEZXJlaGFtFUVhc3QgTWlkbGFuZHMgUGFya3dheQlFZGluYnVyZ2gRRWRpbmJ1cmdoIEFpcnBvcnQGRXhldGVyB0ZhbGtpcmsLRmVsZGtpcmNoZW4IRmxvcmVuY2UQRnJhbmtmdXJ0IC8gTWFpbgVHZW5vYQRHZW50B0dsYXNnb3cKR2xvdWNlc3RlcglHb3R0aW5nZW4IR3JhbnRoYW0HR3JpbXNieRRIYWxiZWF0aCBJbnRlcmNoYW5nZQdIYW1idXJnCEhhbm5vdmVyBkhhdmFudAxIaWdoIFd5Y29tYmUHSG9uaXRvbgxIdWRkZXJzZmllbGQESHVsbA1JbnZlcmtlaXRoaW5nCUludmVybmVzcwdJcHN3aWNoBkthc3NlbAlLZXR0ZXJpbmcKS2luZ3MgTHlubgdLaW5yb3NzE0xhIFNwZXppYSAoU2FyemFuYSkITGFtcGV0ZXIJTGFuY2FzdGVyCExlIEhhdnJlB0xlIE1hbnMGTGVlZHMgCUxlaWNlc3RlcgdMZWlwemlnBUxpbGxlB0xpbW9nZXMHTGluY29sbglMaXZlcnBvb2wGTG9uZG9uDExvdWdoYm9yb3VnaAVMdXRvbgRMeW9uCk1hbmNoZXN0ZXIJTWFyc2VpbGxlBE1ldHoNTWlkZGxlc2Jyb3VnaAVNaWxhbg1NaWx0b24gS2V5bmVzBk11bmljaAZOYW50ZXMGTmFwbGVzD05ld2Fyay1vbi1UcmVudAdOZXdidXJ5CU5ld2Nhc3RsZQdOZXdwb3J0B05ld3F1YXkMTmV3dG9uIEFiYm90C05vcnRoYW1wdG9uB05vcndpY2giTm9yd2ljaCwgVW5pdmVyc2l0eSBvZiBFYXN0IEFuZ2xpYQpOb3R0aW5naGFtCU51cmVtYnVyZwZPeGZvcmQFUGFkdWEIUGFpZ250b24FUGFyaXMNUGVtYnJva2UgRG9jawhQZW56YW5jZQZQZXJ0aCAMUGV0ZXJib3JvdWdoBFBpc2EJUGl0bG9jaHJ5CFBseW1vdXRoCFBvaXRpZXJzBVBvb2xlClBvcnRzbW91dGgIUHJlc3RvbiAHUmVhZGluZwdSZWRydXRoBVJlaW1zBlJlbm5lcwRSb21lCFJvc3NsYXJlCVJvdHRlcmRhbQVSb3VlbgVSdWdieQlTYWxpc2J1cnkKU2N1bnRob3JwZQlTaGVmZmllbGQFU2llbmELU2lsdmVyc3RvbmULU291dGhhbXB0b24TU291dGhhbXB0b24gQWlycG9ydAdTdCBFcnRoClN0IEV0aWVubmUIU3RpcmxpbmcJU3RvY2twb3J0DlN0b2tlLU9uLVRyZW50ClN0cmFzYm91cmcJU3R1dHRnYXJ0ClN1bmRlcmxhbmQHU3dhbnNlYQdTd2luZG9uB1RhdW50b24IVGhldGZvcmQHVG9ycXVheQZUb3Vsb24IVG91bG91c2UFVG91cnMJVG93Y2VzdGVyBVR1cmluBlZlbmljZQZWZXJvbmEWV2FrZWZpZWxkL1dvb2xsZXkgRWRnZQpXYXJyaW5ndG9uCFdleW1vdXRoBVdpZ2FuCldpbmNoZXN0ZXIJV29yY2VzdGVyCFdvcnRoaW5nD1llb3ZpbCBKdW5jdGlvbgVZb3JrIBW6AQItMQExAzE0MAMxODUDMTEwAzIzMwMxMzMBMgMyMDYBMwE0AzE3MAE1ATYBNwMxOTcBOAE5AzEyOAMyMTkCMTADMjM1AzI0MgIxMQIxMgMxOTIDMTQzAjEzAzIyNQMyMjYDMjI3AzI0OQIxNAMxNzIDMTEyAjE2AjE3AjE5AjIwAjIyAjIzAzIzOAIyNAMxMzACMjUDMjQ0AzEyMgMxMzUCMjcDMTQ0AzEyNQIyOQMxNjICMzADMjQ2AjMxAzE5MwIzMgMxMjYDMTE5AjMzAjM0AjM1AjM2AzEyNwMyMTADMjIzAzE4OAMyMjADMTI0AjM4AjM5AzE5NQMxNzcDMTc0AzEzOAMxOTEDMTk0AjQyAzE0NQI0NAI0NQI0NgI0OAI0OQMxMjMDMTk2AzE3OAMxMjACNTEDMjIxAzEzOQMxMTYDMjQ3AzIzNAI1MgI1MwMxOTgDMTMyAzE3MQMxNzUCNTQCNTYCNTcDMTQxAzIwMAI1OAMyMjkDMjQxAjU5AzE4NwI2MAMxOTADMjMxAzIxMgMxNzYCNjICNjMCNjQCNjUDMTUwAzE2NgI2NgI2NwI2OAMxOTkCNzEDMjE3AjcyAzExMwI3MwI3NAI3NQMxMjEDMjIyAjc2Ajc3AzIzNwI3OAI3OQI4MAI4MQI4MgMyMzkDMjMyAzE4NgI4MwMxMzQDMjQ4Ajg0Ajg2Ajg4AjkwAzIyNAI5MQI5MwMxMDgDMTY1AzI0NQI5NQMxNjQDMTE4AzIwOQMxODkCOTYCOTcCOTgDMTAwAzEwOQMxMDEDMjMwAzE3MwMyMzYDMTY3AzIxNAMyMTYDMjE1AzEwMgMxMDMDMTA0AzEyOQMxMDUDMTM2AzE0MgMxMDYDMTA3FCsDugFnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2cWAWZkAhcPDxYCHwAFDVRyYXZlbGxpbmcgdG9kZAIbDxAPFgIfC2hkEBUAFQAUKwMAFgBkAh0PFgIfBGcWAgIEDxAPFgIfC2hkZBYAZAIhDw8WBB8BBQsgZGF0ZXBpY2tlch8DAgJkZAIlDw8WBh8BBQsgZGF0ZXBpY2tlch8LaB8DAgJkZAInDxYCHwRnZAIDDw8WAh8CBRl+L01hbmFnZVJlc2VydmF0aW9ucy5hc3B4ZGQCEA9kFgJmDxYCHhBkYXRhLWJhbm5lci1zcGVjBSBmbGFzaGJhbm5lci8xX3NsaWRlc2hvdy1kYXRhLnhtbGQCFA9kFgICAw9kFgJmD2QWAgIBDxYCHgtfIUl0ZW1Db3VudAICFgRmD2QWCAIBDxYCHwAFE05ldyBTdHV0dGdhcnQgU3RvcCBkAgUPFgIfAAUVRnJpZGF5LCAyOSBBcHJpbCAyMDE2ZAIHDxYCHwAFaFdlIGFyZSB1c2luZyBhIG5ldyBzdG9wIGluIFN0dXR0Z2FydCBzaXR1YXRlZCBhdCB0aGUgQWlycG9ydC4NCjxicj48L2JyPg0KUGxlYXNlIHNlZSBvdXIgU3R1dHRnYXJ0IFN0Li4uZAIJDw8WAh8CBSd+L1NlcnZpY2VBZHZpc29yeS5hc3B4P2lkPTM5OSZob21lPXRydWVkZAIBD2QWCAIBDxYCHwAFFm1lZ2FidXMuY29tIFBhcmlzIHN0b3BkAgUPFgIfAAUXRnJpZGF5LCAyMiBKYW51YXJ5IDIwMTZkAgcPFgIfAAVoQWxsIG1lZ2FidXMuY29tIGNvYWNoZXMgaW4gUGFyaXMgdXNlIHRoZSBzdG9wIGF0IA0KPGJyPjxicj4NClF1YWkgRGUgU2VpbmUgQXJyZXQgTWVnYWJ1cw0KPGJyPjIwOCBRdWEuLi5kAgkPDxYCHwIFJ34vU2VydmljZUFkdmlzb3J5LmFzcHg/aWQ9MzY1JmhvbWU9dHJ1ZWRkAhYPZBYCAgEPFgIfBGdkGAIFKFNlcnZpY2VBZHZpc29yeUxpc3QxJG12U2VydmljZUFkdmlzb3JpZXMPD2RmZAUXVXNlclN0YXR1cyRtdlVzZXJTdGF0dXMPD2RmZBNhyFG1WxzbkYYKr3gCogikN6RG",
    "JourneyPlanner$txtNumberOfPassengers"                  :1,
    "JourneyPlanner$txtNumberOfConcessionPassengers"        :0,
    "JourneyPlanner$txtNumberOfNUSPassengers"               :0,
    "JourneyPlanner$ddlLeavingFromState"                    :0,
    "JourneyPlanner$hdnSelected"                            :-1,
    "JourneyPlanner$ddlLeavingFrom"                         :location_mapping[place_name],
    "JourneyPlanner$txtOutboundDate"                        :"",
    "JourneyPlanner$txtReturnDate"                          :"",
    "JourneyPlanner$txtPromotionalCode"                     :"",
    "ServiceAdvisoryList1$RpServiceAdvisories$ctl00$hdnFlag":True,
    "ServiceAdvisoryList1$RpServiceAdvisories$ctl01$hdnFlag":True,
    "__ASYNCPOST"                                           :True,
  }

  post_url = "http://uk.megabus.com/default.aspx"
  post_response = requests.post(post_url,data=post_form_data)

  post_soup = BeautifulSoup(post_response.text, 'html.parser')
  select = post_soup.find_all("select", id="JourneyPlanner_ddlTravellingTo")[0]
  destination_map = []
  for option in select.find_all("option"):
    name = option.contents[0].strip()
    if name == "Select":
      continue
    destination_map.append(name)
  return destination_map



# converts from "<option value="170">Barcelona</option>" to {'Barcelona':170}
location_mappings = open("location.txt",'r')
locationsoup = BeautifulSoup(location_mappings.read(),'html.parser')
location_mappings.close()
location_mapping = {}
all_locations = []
for option in locationsoup.find_all("option"):
  name = option.contents[0].strip()
  all_locations.append(name)
  location_mapping[name] = option['value']

with open('routes.json','r') as f:
  try:
    routes = json.load(f)
  except ValueError:
    routes = {}

def update_route_map():
  routes = {}
  counter = 0
  for x in all_locations:
    print (counter/len(all_locations)*100,"%")
    counter +=1
    routes[x] = get_destinations(x)

  with open('routes.json','w') as f:
    f.write(json.dumps(routes))


def route_search(start,end):
  results = []
  for destination in routes[start]:
    if end in routes[destination]:
      results.append([start, destination, end])
  return results




def get_journey(start, end, date):
  global query_params
  query_params['originCode']            = location_mapping[start]
  query_params['destinationCode']       = location_mapping[end]
  query_params['outboundDepartureDate'] = date
  query_params['passengerCount'] = 1
  journey = requests.get(journey_url, params=query_params)
  journeysoup = BeautifulSoup(journey.text, 'html.parser')

  journeys = journeysoup.find_all('ul', class_='journey')

  journey_json = []

  for j in journeys:
    timings = j.find_all(class_="two")[0].find_all('p')

    depart_time = timings[0].contents[2].strip()
    depart_loc  = timings[0].contents[4].strip()
    arrive_time = timings[1].contents[2].strip()
    arrive_loc  = timings[1].contents[4].strip()

    duration    = j.find_all(class_="three")[0].find_all('p')[0].contents[0].strip()
    days = int(duration.split()[0][:-3]) // 24

    next_day = days+1 if arrive_time<depart_time else days
    next_day_string = "\+" + str(next_day) if next_day > 0 else ""

    cost        = j.find_all(class_="five")[0].find_all('p')[0].contents[0].strip()[1:]

    time_json = {'timings'  :
                   {'depart':depart_time,
                    'arrive':arrive_time},
                 'locations':
                   {'depart':depart_loc,
                    'arrive':arrive_loc},
                 'duration' : duration,
                 'days'     : days,
                 'next_day' : next_day,
                 'cost'     : cost,
                 'date'     : date}

    #print (", ".join([depart_time,depart_loc,arrive_time,arrive_loc,str(duration),str(days),str(next_day),"$"+cost]))

    #print ("Departs:",depart_time,depart_loc, "       Duration:", duration, "    Cost:",str(cost))
    #print ("Arrives:",arrive_time+next_day_string,arrive_loc)
    #print ()

    journey_json.append(time_json)
  return journey_json

months = {v: k for k,v in enumerate(calendar.month_abbr)}

def get_cheapest_in_month(start, end, month_num):

  month_range = calendar.monthrange(2016,month_num)[1]

  journeys = []
  lowest_price = "999999"
  for x in range(1,month_range):
    print (x)
    day = get_journey(start,end,str(x)+"/" + str(month_num) + "/2016") 
    for journey in day:
      if journey['cost'] < lowest_price:
        lowest_price = journey['cost']
      journeys.append(journey)

  cheapest_journeys = []
  for journey in journeys:
    if journey['cost'] == lowest_price:
      cheapest_journeys.append(journey)

  return cheapest_journeys

