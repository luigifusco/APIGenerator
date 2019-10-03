import json
from random import randint, randrange, choice, random
import sys
from math import floor

with open('config.json') as file:
    config = json.loads(''.join(file.readlines()))

cum_prob = {}
cum_prob['addrel'] = config['probabilities']['addrel']
cum_prob['delrel'] = cum_prob['addrel'] + config['probabilities']['delrel']
cum_prob['delent'] = cum_prob['delrel'] + config['probabilities']['delent']
cum_prob['report'] = cum_prob['delent'] + config['probabilities']['report']

if cum_prob['report'] != 1:
    print('The probabilities don\'t sum up to one!')
    quit()


characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
entities = []
relations = []
active_relations = []
advancement = 0

sys.stdout.write('Generating entity names... ')
sys.stdout.flush()
for i in range(config['n_entities']):
    new_ent = ''
    for j in range(randint(config['min_string_length'], config['max_string_length'])):
        new_ent += choice(characters)
    entities.append(new_ent)
sys.stdout.write('done\n')
sys.stdout.write('Generating relations names... ')
sys.stdout.flush()
for i in range(config['n_relations']):
    new_rel = ''
    for j in range(randint(config['min_string_length'], config['max_string_length'])):
        new_rel += choice(characters)
    relations.append(new_rel)
sys.stdout.write('done\n')

with open(config['output_file'], "w") as file:
    sys.stdout.write('Adding all entities... ')
    sys.stdout.flush()
    for ent in entities:
        file.write('addent "{}"\n'.format(ent))
    sys.stdout.write('done\n')

    sys.stdout.write('Writing commands...\n')
    sys.stdout.write('0%')
    sys.stdout.flush()
    for i in range(config['n_commands']):
        if floor(i*100/config['n_commands']) > advancement:
            advancement = floor(i*100/config['n_commands'])
            sys.stdout.write('\r{}%'.format(advancement))
            sys.stdout.flush()
        random_number = random()
        if random_number < cum_prob['addrel']:
            ent1 = choice(entities)
            ent2 = choice(entities)
            while ent1 == ent2:
                ent2 = choice(entities)
            new_rel = (ent1, ent2, choice(relations))
            file.write('addrel "{}" "{}" "{}"\n'.format(new_rel[0], new_rel[1], new_rel[2]))
            active_relations.append(new_rel)
        elif random_number < cum_prob['delrel']:
            if(active_relations == []):
                continue
            rel = choice(active_relations)
            file.write('delrel "{}" "{}" "{}"\n'.format(rel[0], rel[1], rel[2]))
            active_relations.remove(rel)
        elif random_number < cum_prob['delent']:
            if len(entities) < config['n_min_entities']:
                continue
            ent = choice(entities)
            file.write('delent "{}"\n'.format(ent))
            entities.remove(ent)
        else:
            file.write('report\n')
        
    file.write('end\n')
    sys.stdout.write('\ndone\n')