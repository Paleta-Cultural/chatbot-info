import sys
import json
import pandas as pd
import credentials
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator



##########################
# Getting data from GitHub table
##########################

url='https://github.com/Paleta-Cultural/chatbot-info/blob/master/Sample100.csv'
table=pd.read_csv(url, index_col=0)

###########################
# Set up Authenticators
###########################
authenticator = IAMAuthenticator(credentials.api_key)
assistant = AssistantV2(
    version='2020-04-01',
    authenticator=authenticator)
assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com/')

#########################
# Start Session
#########################

session = assistant.create_session(credentials.assistant_id).get_result()
session_id=session["session_id"]

#########################
# Set Context
#########################

ctx= {
        'global': {
            'system': {
                'user_id': 'my_user_id'
            }
        },
        'skills': {
            'main skill': {
                'user_defined': {
                    'account_number': '123456'
                    'some_other_var' : 'fuck u'
                }
            }
        }
    }

#######################
# Deploy Context to Watson
#######################

message=assistant.message(
    assistant_id=credentials.assistant_id,
    session_id='{}'.format(session_id),
    input={
        'message_type': 'text',
        'text': 'Olá, quero viajar com voces',
        'options': {
            'return_context': True
        }
    },
    context=ctx
)


print(json.dumps(message.get_result(), indent=2))
print(message.get_headers())
print("\nREQUEST FINISHED WITH STATUS CODE " + str(message.get_status_code()))

###################
# Delete Session
###################

assistant.delete_session(credentials.assistant_id, "{}".format(session_id))\
         .get_result()
