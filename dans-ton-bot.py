from slackclient import SlackClient

# token provided by slack api website https://api.slack.com/
sc = SlackClient(
    'SLACK_TOKEN')
# dans-ton-casque chan id
chan = 'CHAN_ID'

def get_last_message_id(channel_id):
    last_msg = sc.api_call(
        "channels.history",
        channel=channel_id,
        count=1
    )
    if last_msg['ok']:
        msg_id = last_msg['messages'][0]['client_msg_id']
    else:
        print('something went wrong')
    return msg_id


def msg_exist(id):
    found = False
    try:
        f = open('dans-ton-casque.txt', 'r')
    except FileNotFoundError:
        return found
    for line in f:
        if id in line:
            found = True
            break
    f.close()
    return found


def clean_message(msg):
    cleaned = ''
    for c in msg:
        if str(c) == '<' or str(c) == '>':
            pass
        else:
            cleaned = cleaned + c
    return str(cleaned)


def save_message(id, message, title):
    f = open('dans-ton-casque.txt', 'a+')
    f.write(id + '\n')
    f.write(title + '\n')
    f.write(message + '\n')
    f.close()


def get_all_messages(channel_id):
    history = sc.api_call(
        "channels.history",
        channel=channel_id,
        count=1000
    )
    if history['ok']:
        for e in history['messages']:
            if 'client_msg_id' in e:
                id_m = e['client_msg_id']
            if 'text' in e:
                msg = clean_message(e['text'])
            if 'attachments' in e:
                title = e['attachments'][0]['title']
            save_message(id_m, msg, title)
    else:
        print('something went wrong')


if __name__ == '__main__':
    if sc.rtm_connect(with_team_state=False):
        print('Connected !')
        id_msg = get_last_message_id(chan)
        if msg_exist(id_msg):
            print('no new message to be saved')
        else:
            get_all_messages(chan)
            print('data saved !')
    else:
        print('Connection failed.')
