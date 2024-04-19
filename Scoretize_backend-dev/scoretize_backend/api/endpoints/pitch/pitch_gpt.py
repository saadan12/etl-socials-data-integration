import openai
import time
import datetime
from dotenv import load_dotenv, find_dotenv
import os 
import requests
import json
import time 

"""

_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.getenv('OPENAI_API_KEY')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

base_path = f'{BASE_DIR}/pitch/files'

"""
from ...views import get_user_id_from_user_project_pk, get_pitch_client_brief_by_user_id

_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.getenv('OPENAI_API_KEY')
base_path = 'api/endpoints/pitch/files'

'''
1. Debrief and Objective
2. Market snapshot and digital audit
3. Map of possibilites
4. Action plans
5. Deployment steps

'''


class Pitch_gpt():
    def __init__(self, client, pk):
        self.client = client
        self.pk = pk
        self.user_id = get_user_id_from_user_project_pk(pk)
        self.client_brief = get_pitch_client_brief_by_user_id(self.user_id)   

    def get_samples(self, file_type):
        base_path = f'files/examples/{self.example_company}'
        with open(f'{base_path}/{self.example_company}_{file_type}.txt', 'r') as f:
            sample = " ".join(line.strip() for line in f)  
        return sample
    
    def get_example(self, content):
        with open(f'{base_path}/examples/{content}.txt', 'r') as f:
            sample = "\n ".join(line.strip() for line in f)  
        return sample
    
    def get_json_example(self, content):
        f = open(f'{base_path}/examples/{content}.json')
        return json.load(f)
    
    def get_client_brief(self):
        return self.client_brief
    
    def read_client_output(self, content):
        with open(f'{base_path}/output_{self.client}_final_final/{content}.txt', 'r') as f:
            content = "\n ".join(line.strip() for line in f)
        return content
    
    def read_client_json_output(self, content):
        f = open(f'{base_path}/output_{self.client}_final_final/{content}.json')
        return json.load(f)
    
    def save_json_file(self, json_string, content):

        with open(f'{base_path}/output_{self.client}_final_final/{content}.json', 'w') as f:
            f.write(json_string)

    def summarize(self, response):
        '''
            used to summarize chatgpt's output and feed into next chat
        '''
        response = openai.ChatCompletion.create(
        model = "gpt-4",
        temperature = 1,
        max_tokens = 2000,
        messages=[{"role": "system", "content": "You are an assitant that can extract useful information and keep the structre"},
                {"role": "user", "content": f"summrize the {response}"},
                ])
        return response["choices"][0]["message"]["content"]
    
#  1 and 2. Generate Debrief and Objective based on client's brief 

    def get_debrief(self):
        '''
        prompt: 
            - brief from client

        output:
            - at least 4 points of debrief and objectives
            - list of keylearnings as conclusion

        '''
        client_brief = self.get_client_brief()
        debrief_example = self.get_json_example('debrief')
        response = openai.ChatCompletion.create(
            model = 'gpt-4',
            temperature = 0.7,
            max_tokens = 2048,
            messages = [{'role':'system', 'content':'You are an agency that can create brilliant strategic pitch decks full of marketing insights. You can understand the debrief from your client perfectly and can analyze the extracted information to identify key points, objectives, and requirements that need to be addressed in the pitch deck. You are also familiar with data audits; you know how to make the right strategic pillars based on reasonable statistical analysis.'},
                        {'role':'user','content':f"Based on the input, give me {self.client}'s Debrief and Objective, each part should have at least 4 bullet points, each point starts with a subtitle. \n Desired format:{debrief_example} \n INPUT: {client_brief} \n The response must have more than 2047 tokens and in JSON format."},
                        ])
        debrief = response['choices'][0]['message']['content']
        print(f"""Debrief: \n{debrief} \n""")
        if not os.path.exists(f'{base_path}/output_{self.client}_final_final/'):
            os.mkdir(f'{base_path}/output_{self.client}_final_final/')
        self.save_json_file(debrief, 'debrief')
        return debrief

# 3. get market snapshot and digital audit

    def get_digital_audit(self):
        '''
        prompt: 
            - Key competitors: based on Scoretize's metrics
            - Consumer: buyer personas
            - Digital audit: SWOT based on Scoretize's metrics

        output:
            - Key competitors
            - Consumer
            - Digital audit
        '''
        response_metrics = self.read_client_output('response_metrics')

        # 1. get key competitors 
        key_competitors_example = self.get_example('key_competitors')
        response_cometitors = openai.ChatCompletion.create(
            model = 'gpt-4',
            temperature = 0.8,
            max_tokens = 2048,
            messages = [{'role':'system', 'content':'You are an agency that can create brilliant strategic pitch decks full of marketing insights. You can understand the debrief from your client perfectly and can analyze the extracted information to identify key points, objectives, and requirements that need to be addressed in the pitch deck. You are also familiar with data audits; you know how to make the right strategic pillars based on reasonable statistical analysis.'},
                        {'role':'user','content':f"Give me a table analyzing {self.client} and its competitors on Website features, Website traffic, Messaging, Engagement rate and Social media content.\n DESIRED FORMAT: {key_competitors_example} \n INPUT:{response_metrics} \n The Engagement rate will be the average number of all social platforms.\n The response must have more than 2047 tokens and in JSON format."},
                        ])
        key_competitors_res = response_cometitors['choices'][0]['message']['content']
        self.save_json_file(key_competitors_res, 'key_competitors' )
        time.sleep(10)

        # 2. get buyer personas
        debrief_example = self.get_example('debrief')
        # client_debrief = self.read_client_output('debrief')
        client_debrief = self.read_client_json_output('debrief')
        buyperson_example = self.get_json_example('buyer_persona')
        response_consumers = openai.ChatCompletion.create(
            model = 'gpt-4',
            temperature = 0.8,
            max_tokens = 2048,
            messages = [{'role':'system', 'content':'You are an agency that can create brilliant strategic pitch decks full of marketing insights. You can understand the debrief from your client perfectly and can analyze the extracted information to identify key points, objectives, and requirements that need to be addressed in the pitch deck. You are also familiar with data audits; you know how to make the right strategic pillars based on reasonable statistical analysis.'},
                        {'role':'user','content':f'Here are the debrief and objectives of your client Cocacola, {debrief_example} \n Based on these information, give me more than 5 buyer personas, 4 micro moments in details, and the occasions in the end. \
                                                    All buyer personas must have a lot of details like Title, Age Range, Hot Zone Locations, Purchase Location, Average Income, Interests, Most Common Products,  Purchase Location, Top Purchase Triggers and Moment Of Consumption.\n The response must have more than 2047 tokens and in JSON format.'},
                        {'role':'assistant', 'content':  json.dumps(buyperson_example)}, # make sure the input and output are in string format
                        {'role':'user','content':f'Here are the debrief and objectives of your client {self.client}: {client_debrief} \n Based on these information, give me more than 5 buyer personas, 4 micro moments in details, and the occasions in the end. \
                                                    All buyer personas must have Title, Age Range, Hot Zone Locations, Average Income, Interests, Most Common Products,  Purchase Location, Top Purchase Triggers and Moment Of Consumption. \n The response must have more than 2047 tokens and in JSON format.'},
                        ])
        response_consumers_res = response_consumers['choices'][0]['message']['content']
        json_string = json.dumps(response_consumers_res, indent=3)
        self.save_json_file(json_string, 'buyer_persona')
        time.sleep(10)

        # 3. get digital audit
        swot_example = self.get_example('swot_analysis')
        response_digital_audit = openai.ChatCompletion.create(
        model = 'gpt-4',
        temperature = 0.7,
        max_tokens = 2048,
        messages = [{'role':'system', 'content':'You are an agency that can create brilliant strategic pitch decks full of marketing insights. You can understand the debrief from your client perfectly and can analyze the extracted information to identify key points, objectives, and requirements that need to be addressed in the pitch deck. You are also familiar with data audits; you know how to make the right strategic pillars based on reasonable statistical analysis.'},
                    {'role':'user','content':f'Generate a SWOT analysis in JSON for you client {self.client} based the metrics: {response_metrics} , each part should answer these questions:{swot_example} .\n The response must have more than 2047 tokens and be conveted into JSON.'},
                    ])
        response_digital_audit_res = response_digital_audit['choices'][0]['message']['content']   
        self.save_json_file(response_digital_audit_res, 'swot_analysis' )

# 4. get map of possbilities
# hypotesis
    def get_map_of_possibilities(self):
        '''
        prompt: 
            - Debrief + objectives
            - Market snaposhot

        output:
            - each possibility should include input and hypothesis
            - end with the key hypotheses as conclusion
        '''
        debrief_example, map_possibilies_example = self.get_json_example('debrief'), self.get_json_example('map_possibilities')
        client_debrief, key_competitors, buyer_persona, digital_audit = \
            self.read_client_json_output('debrief'),self.read_client_json_output('key_competitors'),self.read_client_json_output('buyer_persona'),self.read_client_json_output('digital_audit') 

        response_map_possibilites = openai.ChatCompletion.create(
            model = 'gpt-4',
            temperature = 0.8,
            max_tokens = 2048,
            messages = [{'role':'system', 'content':'Assistant is an agency that can create brilliant strategic pitch decks full of marketing insights. Assistant can understand the debrief from your client perfectly, and can analyze the extracted information to identify key points, objectives, and requirements that need to be addressed in the pitch deck. Assistant is also familiar with data audits; Assistant knows how to make the right strategic pillars based on reasonable statistical analysis.'},
                        {'role':'user','content':f'Here are the debrief and objectives of your client Cocacola, {debrief_example} \n Based on the debrief and objectives, give me 5 maps of possibilites, they must contain Action, Input and Hypothesis, and lastly end with all the key hypotheses in a conclusion. \n The response must have more than 2047 tokens and in JSON format.'},
                        {'role':'assistant', 'content': json.dumps(map_possibilies_example)},
                        {'role':'user','content':f"Now you have a new client, Fifa Women's World Cup, Based on the debrief and objectives: {client_debrief}, and the market snapshot: {key_competitors} \n {buyer_persona} \n {digital_audit}, \n following the same structure of the action plans you just created, give me 5 maps of possibilites, they must contain Action, Input and Hypothesis, and lastly end with all the key hypotheses in a conclusion.\n The response must have more than 2047 tokens and in JSON format."}
                        ])
        response_map_possibilites = response_map_possibilites['choices'][0]['message']['content']   
        json_string = json.dumps(response_map_possibilites, indent=3)
        self.save_json_file(json_string, 'map_possibilites')
        print(f"""Map of possibilites: \n{response_map_possibilites} \n""")

    def get_action_plans(self):
        '''
        prompt:
            - debrief and objectives
            - summary of market
            - map of possibilities

        - action plans
            - plans include awareness, consideration, conversion, and loyalty
                
        '''
        swot_analysis, action_plans_sample = self.get_example('swot_analysis'), self.get_json_example('action_plans')
        client_debrief, client_swot_analysis = self.read_client_json_output('debrief'), self.read_client_json_output('swot_analysis')
        # client_swot_analysis = self.read_client_output('swot_analysis')
        # client_market_snapshot_summay = self.summarize(client_market_snapshot)
        response = openai.ChatCompletion.create(
            model = 'gpt-4',
            temperature = 1,
            max_tokens = 2048,
            messages = [{'role':'system', 'content':'Assistant is an agency that can create brilliant strategic pitch decks full of marketing insights. Assistant can understand the debrief from your client perfectly, and can analyze the extracted information to identify key points, objectives, and requirements that need to be addressed in the pitch deck. Assistant is also familiar with data audits; Assistant knows how to make the right strategic pillars based on reasonable statistical analysis.'},
                        {'role':'user','content':f'Here are the swot analysis of your client Netflix: {swot_analysis} \n Based on these information, give some mindblowing action plans based on the marketing funnel steps of awareness, consideration, conversion, and loyalty. \n The response must have more than 2047 tokens.'},
                        {'role':'assistant', 'content': json.dumps(action_plans_sample)},
                        {'role':'user','content':f"Now you have a new client, Fifa Women's World Cup, Based on the debrief and objectives: {client_debrief}, and the swot analysis: {client_swot_analysis}, following the same structure of the action plans you just created, give me some action plans based on the marketing funnel steps of awareness, consideration, conversion, and loyalty.\n The response must have more than 2047 tokens and be converted into JSON."}
                        ])
        action_plans = response['choices'][0]['message']['content']
        json_string = json.dumps(action_plans, indent=3)
        self.save_json_file(json_string, 'action_plans')

        print(f"""Action plans: \n{action_plans} \n""")
        return action_plans

# 6. get deployment steps
    def get_delpoyment_steps(self):
        '''
        prompt:
            - debrief and objectives
        output:
            - deployment steps
        '''
        brief_sample, deployment_steps_sample = self.get_example('debrief'), self.get_json_example('deployment_steps')
        client_brief = self.get_client_brief()
        response = openai.ChatCompletion.create(
            model = 'gpt-4',
            temperature = 0.7,
            max_tokens = 2048,
            messages = [{'role':'system', 'content':'Assistant is an agency that can create brilliant strategic pitch decks full of marketing insights. Assistant can understand the debrief from your client perfectly, and can analyze the extracted information to identify key points, objectives, and requirements that need to be addressed in the pitch deck. Assistant is also familiar with data audits; Assistant knows how to make the right strategic pillars based on reasonable statistical analysis.'},
                        {'role':'user','content':f'Here are the debrief and objectives of your client Cocacola, {brief_sample} \n Based on the debrief and objectives, provide me deployment steps in detail, it must include core team, governance model, pilot countires, KPIs, key milestones and team budget. \n The response must have more than 2047 tokens.'},
                        {'role':'assistant', 'content': json.dumps(deployment_steps_sample)},
                        {'role':'user','content':f"Now you have a new client, Fifa Women's World Cup, Based on the debrief and objectives: {client_brief},provide me deployment steps in detail, it must include core team, governance model, pilot countires, KPIs, key milestones and team budget . The response must have more than 2047 tokens and in JSON format."}
                        ])
        deployment_steps = response['choices'][0]['message']['content']
        print(f"""Deployment steps: \n{deployment_steps} \n""")
        json_string = json.dumps(deployment_steps, indent=3)
        self.save_json_file(json_string, 'deployment_steps' )

        return deployment_steps

start_time = time.time()
