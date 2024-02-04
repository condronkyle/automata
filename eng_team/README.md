# automata

TLDR: You can give a prompt for a deliverable software product or architecture, and by running this program, a series of chatgpt enabled agents will work together to produce the code, which you can then copy into your real computer and use yourself.

How to Use:
1. If desired, update the initial_prompt in config.json
2. cd eng_team
3. python3 main.py
4. You can follow along the conversation via the print statements, but eventually, they should converge and then the program will stop once the software is finished. You will then have to go through those print statements to grab the code. This could easily be improved by using the Files API by OpenAI but i didnt set that up yet.
5. If you follow along and the AI is being stupid, just kill the program and try again. I've had to hardcode some prompt-editing to avoid the agents looping ineffectively, but sometimes it still happens.

Prerequisites
1. Requires installing python obviously
2. Also requires installing openai package (pip install openai):
https://platform.openai.com/docs/api-reference?lang=python
3. Obtaining an openai key - this code currently uses chatgpt4 (gpt-4-1106-preview) which requires a paid openai account, but you could update the assistant.py class to use chatgpt3.5 instead which is free (though still needs a key i think)


File Info:
3 directories in this Repo:

1. neighborhood - empty for now, hope to add framework to simulate a neighborhood of agents walking around and interacting when they encounter eachother
2. utils - as expected, though i didnt finish migrating utils out of eng_team
3. eng_team - this is the main directory of the setup to enabled 3 agents to interact with eachother to build software

eng_team files
Most of these are self explanatory files containing classes.
main.py is what is executed of course and also contains most of the logic
utils.py has a potpourri of necessary functionality
config.json is used so that in theory, agents can be reused rather than recreated each time (if you populated assistant_ids), and also so that conversations can be resumed rather than restarted (if you populated assistant_ids AND thread_ids). These ids are printed at the start of each run of main.py