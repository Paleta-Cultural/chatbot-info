import sys
import json
import pandas as pd
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
authenticator = IAMAuthenticator('pvBJMVAmpAiuICOy8pPAePIhcazNEqNKzdM6s93jVcWb')
assistant = AssistantV2(
    version='2020-04-01',
    authenticator=authenticator)
assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com/')

#########################
# Start Session
#########################

session = assistant.create_session("d8ec0377-fe74-451c-8214-01e9f01a6e6d").get_result()
session_id=session["session_id"]

#########################
# Set Context
#########################

ctx= asda



#######################
# Deploy Context to Watson
#######################

message=assistant.message(
    assistant_id='d8ec0377-fe74-451c-8214-01e9f01a6e6d',
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

assistant.delete_session("d8ec0377-fe74-451c-8214-01e9f01a6e6d", "{}".format(session_id))\
         .get_result()
