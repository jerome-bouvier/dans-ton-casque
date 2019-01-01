# dans-ton-casque

Using slack api to extract data from a specific channel

Requires python module SlackClient for api calls

A token is issued on slack api website https://api.slack.com/custom-integrations/legacy-tokens

A channel id is also required. It can be retrieved using :
sc.api_call("channels.list")
