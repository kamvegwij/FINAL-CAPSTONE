'''
from twilio.rest import Client

account_sid = 'AC53c02b716c92cd490d905c2cb1367a7a'
auth_token = '460241dcc2bcbb0b3899cf117600c37a'
client = Client(account_sid, auth_token)

call = client.calls.create(
                        url='https://rackley-hummingbird-7239.twil.io/assets/Recording.m4a',
                        to='+27825748542',
                        from_='+14782428486'
                    )

print(call.sid)
'''