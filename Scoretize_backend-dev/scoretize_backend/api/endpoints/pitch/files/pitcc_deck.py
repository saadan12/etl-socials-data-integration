import openai
import time
import datetime
from dotenv import load_dotenv, find_dotenv
import os 

_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.getenv('OPENAI_API_KEY')


class Create_pitchdeck():
    def __init__(self, company, client):
        self.example_company = company
        self.client = client
    
    def get_samples(self, file_type):
        base_path = f'files/examples/{self.example_company}'
        with open(f'{base_path}/{self.example_company}_{file_type}.txt', 'r') as f:
            sample = " ".join(line.strip() for line in f)  
        return sample
    
    def get_client_brief(self):
        base_path = f'files/client'
        with open(f'{base_path}/{self.client}_brief.txt', 'r') as f:
            brief = f.readlines()
        return brief[0]
    
    def summarize(self, response):
        '''
            used to summarize chatgpt's output and feed into next chat
        '''
        response = openai.ChatCompletion.create(
        model = "gpt-4",
        temperature = 0.7,
        max_tokens = 2000,
        messages=[{"role": "system", "content": "You are an assistant that can extract useful information and keep the structure"},
                {"role": "user", "content": f"summrize the {response} into at least 1000 tokens"},
                ])
        print(f"""Summarized: \n{response["choices"][0]["message"]["content"]} \n""")
        return response["choices"][0]["message"]["content"]
    
    def get_key_learnings(self):
        '''
        prompt: 
            - debrief and objective from client
            - Scoretize metrics

        output:
        - key learnings(max tokens: 2048)
                - at least 5 points of keylearings
                - including buyer personas, micromoments, occasinos and search
                - list of keylearnings as conclusion

        Time consuption: 0:03:54.040782
        '''
        brief_sample, keylearnings_sample = self.get_samples('brief'), self.get_samples('keylearnings')
        client_brief = self.get_client_brief()
        response = openai.ChatCompletion.create(
            model = 'gpt-4',
            temperature = 1,
            max_tokens = 2048,
            messages = [{'role':'system', 'content':'Assistant is an agency that can create brilliant strategic pitch decks full of marketing insights. Assistant can understand the debrief from your client perfectly, and can analyze the extracted information to identify key points, objectives, and requirements that need to be addressed in the pitch deck. Assistant is also familiar with data audits; Assistant knows how to make the right strategic pillars based on reasonable statistical analysis.'},
                        {'role':'user','content':f'Here are the debrief and objectives of your client Cocacola, {brief_sample} \n Based on the debrief and objectives, give me more than 5 key learnings, those key learnings should have information like buyer personas, micro moments, priority occasions and current searches in details, then, in the end, list those key learnings as the conclusion.\n The response must have more than 2047 tokens.'},
                        {'role':'assistant', 'content': keylearnings_sample},
                        {'role':'user','content':f"Now you have a new client, Fifa Women's World Cup, Based on the debrief and objectives: {client_brief}, following the same structure of the keylearnings you just created, give me more than 5 key learnings, the 3rd key learning must have buyer personas, micro moments, the 4th key learning must be priority occasions, the last key learning must have current searches in details, then, in the end, list those key learnings as the conclusion.\n Output tokens must be more than 2047 tokens."}
                        ])
        key_learnings = response['choices'][0]['message']['content']
        with open('files/output/key_learnings.txt', 'w') as f:
            f.write(key_learnings)
        print(f"""Key learnings: \n{key_learnings} \n""")
        return key_learnings

    def get_action_plans(self):
        '''
        prompt:
            - debrief and objectives
            - summary of keylearnings
            - digital audit (not for now)
        output:
            - action plans
                - at least 5 action plans
                - each plan should include input and hypothesis
                - end with the key hypotheses as conclusion
                
        '''
        brief_sample, action_plans_sample = self.get_samples('brief'), self.get_samples('action_plans')
        client_brief = self.get_client_brief()
        key_learnings_summay = self.summarize(self.get_key_learnings())
        response = openai.ChatCompletion.create(
            model = 'gpt-4',
            temperature = 1,
            max_tokens = 2048,
            messages = [{'role':'system', 'content':'Assistant is an agency that can create brilliant strategic pitch decks full of marketing insights. Assistant can understand the debrief from your client perfectly, and can analyze the extracted information to identify key points, objectives, and requirements that need to be addressed in the pitch deck. Assistant is also familiar with data audits; Assistant knows how to make the right strategic pillars based on reasonable statistical analysis.'},
                        {'role':'user','content':f'Here are the debrief and objectives of your client Cocacola, {brief_sample} \n Based on the debrief and objectives, give me 5 action plans, the action plans should be based on reasonable conclusions including input and hypothesis, and lastly end with the key hypotheses as a conclusion. \n The response must have more than 2047 tokens.'},
                        {'role':'assistant', 'content': action_plans_sample},
                        {'role':'user','content':f"Now you have a new client, Fifa Women's World Cup, Based on the debrief and objectives: {client_brief}, and the keylearnings: {key_learnings_summay}, following the same structure of the action plans you just created, give me 5 action plans, the action plans should be based on reasonable conclusions including input and hypothesis, and lastly end with the key hypotheses as a conclusion.\n The response must have more than 2047 tokens."}
                        ])
        action_plans = response['choices'][0]['message']['content']
        with open('files/output/action_plans.txt', 'w') as f:
            f.write(action_plans)
        print(f"""Action plans: \n{action_plans} \n""")
        return action_plans

    def get_strategic_pillars(self):
        '''
        prompt:
            - debrief and objectives
            - summary of action plans 
        output:
            - strategic pillars
                - create 4 strategic pillars, each pillar should have a short explanation
                - followed by more details on each pillar     
        '''
        brief_sample, pillars_sample = self.get_samples('brief'), self.get_samples('pillars')
        client_brief = self.get_client_brief()
        action_plans_summay = self.summarize(self.get_action_plans())
        response = openai.ChatCompletion.create(
            model = 'gpt-4',
            temperature = 1,
            max_tokens = 2048,
            messages = [{'role':'system', 'content':'Assistant is an agency that can create brilliant strategic pitch decks full of marketing insights. Assistant can understand the debrief from your client perfectly, and can analyze the extracted information to identify key points, objectives, and requirements that need to be addressed in the pitch deck. Assistant is also familiar with data audits; Assistant knows how to make the right strategic pillars based on reasonable statistical analysis.'},
                        {'role':'user','content':f'Here are the debrief and objectives of your client Cocacola, {brief_sample} \n Based on the debrief and objectives, give me at least 4 strategic pillars, \ 1. list all strategic pillars, each pillar should have a short explanation, 2. followed by more details on each pillar. \n The response must have more than 2047 tokens.'},
                        {'role':'assistant', 'content': pillars_sample},
                        {'role':'user','content':f"Now you have a new client, Fifa Women's World Cup, Based on the debrief and objectives: {client_brief}, and the keylearnings: {action_plans_summay}, following the same structure of the action plans you just created, give me at least 4 strategic pillars, \ 1. list all strategic pillars, each pillar should have a short explanation, 2. followed by more details on each pillar. \n The response must have more than 2047 tokens."}
                        ])
        pillars = response['choices'][0]['message']['content']
        with open('files/output/pillars.txt', 'w') as f:
            f.write(pillars)
        print(f"""Strategic pillars: \n{pillars} \n""")
        return pillars

    def get_delpoyment_steps(self):
        '''
        prompt:
            - debrief and objectives
        output:
            - deployment steps
        '''
        brief_sample, deployment_steps_sample = self.get_samples('brief'), self.get_samples('deployment_steps')
        client_brief = self.get_client_brief()
        response = openai.ChatCompletion.create(
            model = 'gpt-4',
            temperature = 1,
            max_tokens = 2048,
            messages = [{'role':'system', 'content':'Assistant is an agency that can create brilliant strategic pitch decks full of marketing insights. Assistant can understand the debrief from your client perfectly, and can analyze the extracted information to identify key points, objectives, and requirements that need to be addressed in the pitch deck. Assistant is also familiar with data audits; Assistant knows how to make the right strategic pillars based on reasonable statistical analysis.'},
                        {'role':'user','content':f'Here are the debrief and objectives of your client Cocacola, {brief_sample} \n Based on the debrief and objectives, provide me deployment steps in detail, it must include core team, governance model, pilot countires, KPIs, key milestones and team budget. \n The response must have more than 2047 tokens.'},
                        {'role':'assistant', 'content': deployment_steps_sample},
                        {'role':'user','content':f"Now you have a new client, Fifa Women's World Cup, Based on the debrief and objectives: {client_brief},provide me deployment steps in detail, it must include core team, governance model, pilot countires, KPIs, key milestones and team budget . The response must have more than 2047 tokens."}
                        ])
        deployment_steps = response['choices'][0]['message']['content']
        with open('files/output/deployment_steps.txt', 'w') as f:
            f.write(deployment_steps)
        print(f"""Deployment steps: \n{deployment_steps} \n""")
        return deployment_steps

start_time = time.time()
create_pitch = Create_pitchdeck('cocacola', 'fifa')

summary_brief = create_pitch.summarize(create_pitch.get_client_brief())
