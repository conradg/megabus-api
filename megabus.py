# Python 3.4

import requests, json, calendar
from bs4 import BeautifulSoup


query_params = {
  "originCode"                   : 56,
  "destinationCode"              : 187,
  "outboundDepartureDate"        : "28/01/2016",
  "passengerCount"               : 1,
}
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
    "__VIEWSTATE"                                           :"/wEPDwUJMjAxOTg2MjQ3D2QWAgIBD2QWDAIED2QWBAICDw8WAh4EVGV4dAUfV2VsY29tZSwgWW91IGFyZSBub3QgbG9nZ2VkIGluLmRkAgYPDxYCHwAFEFZpZXcgIEJhc2tldCAoMClkZAIGD2QWJAIDDw8WAh8ABQdFbmdsaXNoZGQCBQ8PFgYeCENzc0NsYXNzBSBmbGFnLWljb24gZmxhZy11ayB0b29sdGlwIGFjdGl2ZR4LTmF2aWdhdGVVcmwFTGh0dHA6Ly93d3cubWVnYWJ1cy5jb20vbGFuZ3VhZ2UuYXNoeD9jbj11ayZsbj1lbiZwYXRoPWRlZmF1bHQuYXNweCZzZWM9RmFsc2UeBF8hU0ICAmRkAgcPDxYCHwIFTGh0dHA6Ly93d3cubWVnYWJ1cy5jb20vbGFuZ3VhZ2UuYXNoeD9jbj1iZSZsbj1ubCZwYXRoPWRlZmF1bHQuYXNweCZzZWM9RmFsc2VkZAIJDw8WAh8CBUxodHRwOi8vd3d3Lm1lZ2FidXMuY29tL2xhbmd1YWdlLmFzaHg/Y249YmUmbG49bmwmcGF0aD1kZWZhdWx0LmFzcHgmc2VjPUZhbHNlZGQCCw8PFgIfAgVMaHR0cDovL3d3dy5tZWdhYnVzLmNvbS9sYW5ndWFnZS5hc2h4P2NuPWJlJmxuPWZyJnBhdGg9ZGVmYXVsdC5hc3B4JnNlYz1GYWxzZWRkAg0PDxYCHwIFTGh0dHA6Ly93d3cubWVnYWJ1cy5jb20vbGFuZ3VhZ2UuYXNoeD9jbj1mciZsbj1mciZwYXRoPWRlZmF1bHQuYXNweCZzZWM9RmFsc2VkZAIPDw8WAh8CBUxodHRwOi8vd3d3Lm1lZ2FidXMuY29tL2xhbmd1YWdlLmFzaHg/Y249ZGUmbG49ZGUmcGF0aD1kZWZhdWx0LmFzcHgmc2VjPUZhbHNlZGQCEQ8PFgIfAgVMaHR0cDovL3d3dy5tZWdhYnVzLmNvbS9sYW5ndWFnZS5hc2h4P2NuPW5sJmxuPW5sJnBhdGg9ZGVmYXVsdC5hc3B4JnNlYz1GYWxzZWRkAhMPDxYCHwIFTGh0dHA6Ly93d3cubWVnYWJ1cy5jb20vbGFuZ3VhZ2UuYXNoeD9jbj1lcyZsbj1lcyZwYXRoPWRlZmF1bHQuYXNweCZzZWM9RmFsc2VkZAIVDw8WAh8CBUxodHRwOi8vd3d3Lm1lZ2FidXMuY29tL2xhbmd1YWdlLmFzaHg/Y249ZXMmbG49ZXMmcGF0aD1kZWZhdWx0LmFzcHgmc2VjPUZhbHNlZGQCFw8PFgIfAgVMaHR0cDovL3d3dy5tZWdhYnVzLmNvbS9sYW5ndWFnZS5hc2h4P2NuPWVzJmxuPWNhJnBhdGg9ZGVmYXVsdC5hc3B4JnNlYz1GYWxzZWRkAhkPDxYCHwIFTGh0dHA6Ly93d3cubWVnYWJ1cy5jb20vbGFuZ3VhZ2UuYXNoeD9jbj1pdCZsbj1pdCZwYXRoPWRlZmF1bHQuYXNweCZzZWM9RmFsc2VkZAIbDw8WAh8CBUBodHRwOi8vd3d3Lm1lZ2FidXMuY29tL2xhbmd1YWdlLmFzaHg/Y249dXMmbG49ZW4mcGF0aD0mc2VjPUZhbHNlZGQCHQ8PFgIfAgVAaHR0cDovL3d3dy5tZWdhYnVzLmNvbS9sYW5ndWFnZS5hc2h4P2NuPXVzJmxuPWVuJnBhdGg9JnNlYz1GYWxzZWRkAh8PDxYCHwIFQGh0dHA6Ly93d3cubWVnYWJ1cy5jb20vbGFuZ3VhZ2UuYXNoeD9jbj11cyZsbj1lcyZwYXRoPSZzZWM9RmFsc2VkZAIhDw8WAh8CBUBodHRwOi8vd3d3Lm1lZ2FidXMuY29tL2xhbmd1YWdlLmFzaHg/Y249Y2EmbG49ZW4mcGF0aD0mc2VjPUZhbHNlZGQCIw8PFgIfAgVAaHR0cDovL3d3dy5tZWdhYnVzLmNvbS9sYW5ndWFnZS5hc2h4P2NuPWNhJmxuPWVuJnBhdGg9JnNlYz1GYWxzZWRkAiUPDxYCHwIFQGh0dHA6Ly93d3cubWVnYWJ1cy5jb20vbGFuZ3VhZ2UuYXNoeD9jbj1jYSZsbj1mciZwYXRoPSZzZWM9RmFsc2VkZAIMD2QWBAIBD2QWAmYPZBYYAgUPZBYCAgEPFgIeB1Zpc2libGVoZAIHDw8WAh8ABQEwFgIeCm9uS2V5UHJlc3MFHHJldHVybiBJc051bWVyaWMoZXZlbnQsdGhpcylkAgkPFgIfBGcWAgIDDw9kFgIfBQUccmV0dXJuIElzTnVtZXJpYyhldmVudCx0aGlzKWQCCw8WAh8EZxYCAgMPD2QWAh8FBRxyZXR1cm4gSXNOdW1lcmljKGV2ZW50LHRoaXMpZAIPDxYCHwRnFgJmDxYEHgVjbGFzcwUXc3RhdGVwcm92aW5jZSAgY2xlYXJmaXgeBXN0eWxlBRliYWNrZ3JvdW5kLWNvbG9yOiNFNEU0RTQ7FgYCAQ8PFgIfAAUHQ291bnRyeWRkAgMPEA8WBh4FV2lkdGgbAAAAAACAXEABAAAAHgtfIURhdGFCb3VuZGcfAwKAAmQQFQsDQWxsB0JlbGdpdW0HRW5nbGFuZAZGcmFuY2UHR2VybWFueQVJdGFseQtOZXRoZXJsYW5kcxNSZXB1YmxpYyBvZiBJcmVsYW5kCFNjb3RsYW5kBVNwYWluBVdhbGVzFQsBMAE1ATEBNgE4AjExATcBNAEyATkBMxQrAwtnZ2dnZ2dnZ2dnZxYBZmQCBQ8WAh8EZxYCAgEPFgIeCWlubmVyaHRtbAWkAm1lZ2FidXMuY29tIGhhcyBjb21lIGEgbG9uZyB3YXkgc2luY2UgaXRzIGxhdW5jaCBpbiAyMDAzLCBhbmQgd2UgYXJlIG5vdyBwcm91ZCB0byBzZXJ2ZSBvdmVyIDEwMCBkZXN0aW5hdGlvbnMgaW4gdGhlIFVLIGFuZCBNYWlubGFuZCBFdXJvcGUuIFRvIG1ha2Ugb3VyIGluY3JlYXNpbmdseSBsb25nIG9yaWdpbiBsaXN0IGVhc2llciB0byBuYXZpZ2F0ZSB3ZSBoYXZlIGFkZGVkIHRoaXMgbmV3IG9wdGlvbmFsIGNvdW50cnkgZmlsdGVyLiBXZSBob3BlIHlvdSBmaW5kIHRoaXMgbmV3IGZlYXR1cmUgaGVscGZ1bC5kAhUPEA8WBB8JZx4HRW5hYmxlZGhkEBW6AQZTZWxlY3QIQWJlcmRlZW4LQWJlcnlzdHd5dGgGQW1pZW5zCUFtc3RlcmRhbQZBbmdlcnMHQW50d2VycAhBdmllbW9yZQdBdmlnbm9uCUF4bWluc3RlcgdCYW5idXJ5CUJhcmNlbG9uYQhCYXJuc2xleQhCYXRoIFNwYQdCZWRmb3JkBkJlcmxpbgpCaXJtaW5naGFtIEJpcm1pbmdoYW0gSW50ZXJuYXRpb25hbCBBaXJwb3J0CUJsYWNrYnVybgdCb2xvZ25hBkJvbHRvbghCb3JkZWF1eAdCb3VyZ2VzC0JvdXJuZW1vdXRoCEJyYWRmb3JkBkJyZW1lbghCcmlnaHRvbgdCcmlzdG9sD0JyaXN0b2wgKEF6dGVjKRlCcmlzdG9sIChDcmliYnMgQ2F1c2V3YXkpEEJyaXN0b2wgKEZpbHRvbikLQnJpc3RvbCBVV0USQnJpdmUtbGEtR2FpbGxhcmRlCEJydXNzZWxzCENhbWJvcm5lCUNhbWJyaWRnZQpDYW50ZXJidXJ5B0NhcmRpZmYIQ2FybGlzbGUKQ2FybWFydGhlbgpDYXN0bGVmb3JkDUNoYXRlbGxlcmF1bHQKQ2hlbHRlbmhhbQdDaGVzdGVyDENoZXN0ZXJmaWVsZBBDbGVybW9udCBGZXJyYW5kCkNvbGNoZXN0ZXIHQ29sb2duZQhDb3ZlbnRyeQdDcmF3bGV5C0N1bWJlcm5hdWxkB0N3bWJyYW4IRGF2ZW50cnkFRGVyYnkFRGlqb24JRG9uY2FzdGVyCERvcnRtdW5kBkR1bmRlZQtEdW5mZXJtbGluZQxFYXN0IERlcmVoYW0VRWFzdCBNaWRsYW5kcyBQYXJrd2F5CUVkaW5idXJnaBFFZGluYnVyZ2ggQWlycG9ydAZFeGV0ZXIHRmFsa2lyawtGZWxka2lyY2hlbghGbG9yZW5jZRBGcmFua2Z1cnQgLyBNYWluBUdlbm9hBEdlbnQHR2xhc2dvdwpHbG91Y2VzdGVyCUdvdHRpbmdlbghHcmFudGhhbQdHcmltc2J5FEhhbGJlYXRoIEludGVyY2hhbmdlB0hhbWJ1cmcISGFubm92ZXIGSGF2YW50DEhpZ2ggV3ljb21iZQdIb25pdG9uDEh1ZGRlcnNmaWVsZARIdWxsDUludmVya2VpdGhpbmcJSW52ZXJuZXNzB0lwc3dpY2gGS2Fzc2VsCUtldHRlcmluZwpLaW5ncyBMeW5uB0tpbnJvc3MTTGEgU3BlemlhIChTYXJ6YW5hKQhMYW1wZXRlcglMYW5jYXN0ZXIITGUgSGF2cmUHTGUgTWFucwZMZWVkcyAJTGVpY2VzdGVyB0xlaXB6aWcFTGlsbGUHTGltb2dlcwdMaW5jb2xuCUxpdmVycG9vbAZMb25kb24MTG91Z2hib3JvdWdoBUx1dG9uBEx5b24KTWFuY2hlc3RlcglNYXJzZWlsbGUETWV0eg1NaWRkbGVzYnJvdWdoBU1pbGFuDU1pbHRvbiBLZXluZXMGTXVuaWNoBk5hbnRlcwZOYXBsZXMPTmV3YXJrLW9uLVRyZW50B05ld2J1cnkJTmV3Y2FzdGxlB05ld3BvcnQHTmV3cXVheQxOZXd0b24gQWJib3QLTm9ydGhhbXB0b24HTm9yd2ljaCJOb3J3aWNoLCBVbml2ZXJzaXR5IG9mIEVhc3QgQW5nbGlhCk5vdHRpbmdoYW0JTnVyZW1idXJnBk94Zm9yZAVQYWR1YQhQYWlnbnRvbgVQYXJpcw1QZW1icm9rZSBEb2NrCFBlbnphbmNlBlBlcnRoIAxQZXRlcmJvcm91Z2gEUGlzYQlQaXRsb2NocnkIUGx5bW91dGgIUG9pdGllcnMFUG9vbGUKUG9ydHNtb3V0aAhQcmVzdG9uIAdSZWFkaW5nB1JlZHJ1dGgFUmVpbXMGUmVubmVzBFJvbWUIUm9zc2xhcmUJUm90dGVyZGFtBVJvdWVuBVJ1Z2J5CVNhbGlzYnVyeQpTY3VudGhvcnBlCVNoZWZmaWVsZAVTaWVuYQtTaWx2ZXJzdG9uZQtTb3V0aGFtcHRvbhNTb3V0aGFtcHRvbiBBaXJwb3J0B1N0IEVydGgKU3QgRXRpZW5uZQhTdGlybGluZwlTdG9ja3BvcnQOU3Rva2UtT24tVHJlbnQKU3RyYXNib3VyZwlTdHV0dGdhcnQKU3VuZGVybGFuZAdTd2Fuc2VhB1N3aW5kb24HVGF1bnRvbghUaGV0Zm9yZAdUb3JxdWF5BlRvdWxvbghUb3Vsb3VzZQVUb3VycwlUb3djZXN0ZXIFVHVyaW4GVmVuaWNlBlZlcm9uYRZXYWtlZmllbGQvV29vbGxleSBFZGdlCldhcnJpbmd0b24IV2V5bW91dGgFV2lnYW4KV2luY2hlc3RlcglXb3JjZXN0ZXIIV29ydGhpbmcPWWVvdmlsIEp1bmN0aW9uBVlvcmsgFboBAi0xATEDMTQwAzE4NQMxMTADMjMzAzEzMwEyAzIwNgEzATQDMTcwATUBNgE3AzE5NwE4ATkDMTI4AzIxOQIxMAMyMzUDMjQyAjExAjEyAzE5MgMxNDMCMTMDMjI1AzIyNgMyMjcCMTQDMTcyAzExMgIxNgIxNwIxOQIyMAIyMQIyMgIyMwMyMzgCMjQDMTMwAjI1AzI0NAMxMjIDMTM1AjI3AzE0NAMxMjUCMjkDMTYyAjMwAzI0NgIzMQMxOTMCMzIDMTI2AzExOQIzMwIzNAIzNQIzNgMxMjcDMjEwAzIyMwMxODgDMjIwAzEyNAIzOAIzOQMxOTUDMTc3AzE3NAMxMzgDMTkxAzE5NAI0MgMxNDUCNDQCNDUCNDYCNDgCNDkDMTIzAzE5NgMxNzgDMTIwAjUxAzIyMQMxMzkDMTE2AzI0NwMyMzQCNTICNTMDMTk4AzEzMgMxNzEDMTc1AjU0AjU2AjU3AzE0MQMyMDACNTgDMjI5AzI0MQI1OQMxODcCNjADMTkwAzIzMQMyMTIDMTc2AjYyAjYzAjY0AjY1AzE1MAMxNjYCNjYCNjcCNjgDMTk5AjcxAzIxNwI3MgMxMTMCNzMCNzQCNzUDMTIxAzIyMgI3NgI3NwMyMzcCNzgCNzkCODACODECODIDMjM5AzIzMgMxODYCODMDMTM0AzI0OAI4NAI4NgI4OAI5MAMyMjQCOTECOTMDMTA4AzE2NQMyNDUCOTUDMTY0AzExOAMyMDkDMTg5Ajk2Ajk3Ajk4AzEwMAMxMDkDMTAxAzIzMAMxNzMDMjM2AzE2NwMyMTQDMjE2AzIxNQMxMDIDMTAzAzEwNAMxMjkDMTA1AzEzNgMxNDIDMTA2AzEwNxQrA7oBZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnFgFmZAIXDw8WAh8ABQ1UcmF2ZWxsaW5nIHRvZGQCGw8QDxYCHwtoZBAVABUAFCsDABYAZAIdDxYCHwRnFgICBA8QDxYCHwtoZGQWAGQCIQ8PFgQfAQULIGRhdGVwaWNrZXIfAwICZGQCJQ8PFgYfAQULIGRhdGVwaWNrZXIfC2gfAwICZGQCJw8WAh8EZ2QCAw8PFgIfAgUZfi9NYW5hZ2VSZXNlcnZhdGlvbnMuYXNweGRkAhAPZBYCZg8WAh4QZGF0YS1iYW5uZXItc3BlYwUgZmxhc2hiYW5uZXIvMV9zbGlkZXNob3ctZGF0YS54bWxkAhQPZBYCAgMPZBYCZg9kFgICAQ8WAh4LXyFJdGVtQ291bnQCAhYEZg9kFggCAQ8WAh8ABRZtZWdhYnVzLmNvbSBQYXJpcyBzdG9wZAIFDxYCHwAFF0ZyaWRheSwgMjIgSmFudWFyeSAyMDE2ZAIHDxYCHwAFaEFsbCBtZWdhYnVzLmNvbSBjb2FjaGVzIGluIFBhcmlzIHVzZSB0aGUgc3RvcCBhdCANCjxicj48YnI+DQpRdWFpIERlIFNlaW5lIEFycmV0IE1lZ2FidXMNCjxicj4yMDggUXVhLi4uZAIJDw8WAh8CBSd+L1NlcnZpY2VBZHZpc29yeS5hc3B4P2lkPTM2NSZob21lPXRydWVkZAIBD2QWCAIBDxYCHwAFGm1lZ2FidXMuY29tIEFtc3RlcmRhbSBzdG9wZAIFDxYCHwAFGlRodXJzZGF5LCAwNCBGZWJydWFyeSAyMDE2ZAIHDxYCHwAFaG1lZ2FidXMuY29tIHN0b3AgaW4gQW1zdGVyZGFtIGlzIG5vdyBvdXRzaWRlIFNsb3RlcmRpamsgUmFpbCBTdGF0aW9uIGluIFJhZGFyd2VnLiANCjxicj48YnI+DQo8aWZyYW1lLi4uZAIJDw8WAh8CBSd+L1NlcnZpY2VBZHZpc29yeS5hc3B4P2lkPTM3NSZob21lPXRydWVkZAIWD2QWAgIBDxYCHwRnZBgCBShTZXJ2aWNlQWR2aXNvcnlMaXN0MSRtdlNlcnZpY2VBZHZpc29yaWVzDw9kZmQFF1VzZXJTdGF0dXMkbXZVc2VyU3RhdHVzDw9kZmSMSMDDBOLCvn8nmXeEfkqSfaaHEw==",
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
    destination_map.append(option.contents[0].strip())
  return destination_map



# converts from "<option value="170">Barcelona</option>" to {'Barcelona':170}
location_mappings = open("location.txt",'r')
locationsoup = BeautifulSoup(location_mappings.read(),'html.parser')
location_mappings.close()
location_mapping = {}
for option in locationsoup.find_all("option"):
  location_mapping[option.contents[0].strip()] = option['value']


def get_journey(start, end, date):
  query_params['originCode']            = location_mapping[start]
  query_params['destinationCode']       = location_mapping[end]
  query_params['outboundDepartureDate'] = date
  journey = requests.get(journey_url, params=query_params)
  journeysoup = BeautifulSoup(journey.text, 'html.parser')

  journeys = journeysoup.find_all('ul', class_='journey')

  print (date)

  journey_json = {'date':date, 'times':[]}

  for j in journeys:
    timings = j.find_all(class_="two")[0].find_all('p')

    depart_time = timings[0].contents[2].strip()
    depart_loc  = timings[0].contents[4].strip()
    arrive_time = timings[1].contents[2].strip()
    arrive_loc  = timings[1].contents[4].strip()

    time_json = {'timings'  :{'depart':depart_time, 'arrive':arrive_time},
                 'locations':{'depart':depart_loc,  'arrive':arrive_loc }}

    duration    = j.find_all(class_="three")[0].find_all('p')[0].contents[0].strip()
    days = int(duration.split()[0][:-3]) // 24
    next_day = days+1 if arrive_time<depart_time else days
    next_day_string = "\+" + str(next_day) if next_day > 0 else ""

    cost        = j.find_all(class_="five")[0].find_all('p')[0].contents[0].strip()[1:]

    time_json['duration'] = duration
    time_json['days']     = days
    time_json['next_day'] = next_day
    time_json['cost']     = cost

    #print ("Departs:",depart_time,depart_loc, "       Duration:", duration, "    Cost:",str(cost))
    #print ("Arrives:",arrive_time+next_day_string,arrive_loc)
    #print ()

    journey_json['times'] += timings

  return journey_json

months = {v: k for k,v in enumerate(calendar.month_abbr)}

def get_cheapest_in_month(start, end, month_num):

  month_range = calendar.monthrange(2016,month_num)[1]

  for x in range(1,month_range):
    get_journey(start,end,str(x)+"/" + str(month_num) + "/2016")


