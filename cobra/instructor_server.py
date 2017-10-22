import falcon
import yaml
from random import *
import uuid
import json
from utility import decode_message
from server_utility import add_user

def load_yaml(yaml_file):
    with open(yaml_file, 'r') as f:
        data = yaml.load(f.read())
    return data

    
class QuestionResource():
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        question_id = '4464b29f-86a1-4e4c-9261-f581d1b1c8e8'    # this will be pulled from somewhere else
        
        title = data[question_id]['title']
        text = data[question_id]['text']
        signature = data[question_id]['signature']
        tags = data[question_id]['tags']
        unittests = data[question_id]['unittests']
        imports = data[question_id]['imports']
        setup = data[question_id]['setup']
        teardown = data[question_id]['teardown']
        pretest = data[question_id]['pretest']
        posttest = data[question_id]['posttest'] 
        token = str(uuid.uuid4())    # this will probably be from a user database or something, once multiuser is worked out.
        seed = 323423                # this will eventually be randomized per session
        body = {'id': question_id,
                'title': title, 
                'text': text, 
                'signature': signature, 
                'tags': tags, 
                'unittests': unittests, 
                'setup': setup, 
                'teardown': teardown,
                'pretest': pretest,
                'posttest': posttest,
                'imports': imports,
                'token': token,
                'seed': seed}
        
        #body = data[question_id]
        #body['seed'] = 215646
        #body.pop('solution')
        #body.pop('history')
        
        resp.body = (json.dumps(body))

class AddUser():
    def on_post(self, req, resp):
        post_info = json.loads(req.stream.read().decode('utf-8'))
        ip = req.remote_addr
        username = post_info['username']
        password = post_info['password']
        sessionid = add_user(username, password, ip)
        resp.body = sessionid

        
data = load_yaml('format_example.yml')
app = falcon.API()
instructions = QuestionResource()
adduser = AddUser()
app.add_route('/getquestion', instructions)
app.add_route('/newuser', adduser)

