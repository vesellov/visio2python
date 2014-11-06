#!/usr/bin/python
#merge.py
#
#
# <<<COPYRIGHT>>>
#
#
#
#

import os
import sys
import re
import hashlib
import string

#------------------------------------------------------------------------------ 

D = None

#------------------------------------------------------------------------------ 

def compareCondition(found_condition, known_condition):
    found_words = found_condition.split(' ')
    known_words = known_condition.split(' ')
    correct_words = [] 
    for found in found_words:
        opened = 0
        while found.startswith('('):
            found = found[1:]
            opened += 1
        closed = 0
        while found.endswith('))'):
            found = found[:-1]
            closed += 1
        for i in range(opened):
            correct_words.append('(')
        if found.count('()') and not found.count('.A('):
            found = found.replace('()', '(arg)')
        if found.strip():
            correct_words.append(found)
        for i in range(closed):
            correct_words.append(')')
    known_joined = ' '.join(known_words)
    correct_joined = ' '.join(correct_words)
    return known_joined == correct_joined

def processLink(name, condition, state_from, state_to):
    global D
    found_link_id = ''
    for link_id, link_info in D[name]['links'].items():
        if compareCondition(condition, link_info['condition']):
#            print '            (%s) %s' % (link_id, link_info['condition'])
#            print '                [%s %s]' % (state_from, state_to)
#            print '                [%s %s]' % (link_info['from'], link_info['to'])
            if link_info['from'] == state_from and link_info['to'] == state_to:
                found_link_id = link_id
                break
            elif link_info['to'] == state_from and link_info['from'] == state_to:
                # found_link_id = link_id
                print '    WARNING    it seems connection is turned contrary in Visio Document: [%s]<->[%s]' % (state_from, state_to)
                break 
#    print '        <' + found_link_id + '> ' + condition
    return found_link_id
            
def mergeStateMachine(old, new, name):
    global D
    if name not in D.keys():
        return old, []
    A = {}
    merged = ''
    errors = []
    lines = old.splitlines()
    start_line = -1
    end_line = -1
    found_class = ''
    found_def_A = False
    paragraph_def_A = -1
    found_state = ''
    found_newstate = False
    found_return_newstate = False
    found_flag_post = ''
    found_flag_fast = ''
    states_found = []
    found_condition = ''
    flags = []
    if D[name]['label'].endswith(']'):
        for flag in D[name]['label'].split('\\n')[-1].strip('[]').split(','):
            flags.append(flag.strip())
    for line_index in range(1, len(lines)+1):
        line = lines[line_index-1]
        if line.strip().startswith('#'):
            continue
        paragraph = len(line) - len(line.lstrip(' '))

        if line.count('class ') and ( line.count('Automat') or line.count('automat.Automat')):
            found_class = re.search('class (\w+?)\(.*Automat.*\):', line)
            if found_class is None:
                found_class = re.search('class (\w+?)\(.*automat\.Automat.*\):', line)
            if found_class is None:
                errors.append('ERROR     class name not recognized in line %d' % line_index)
                found_class = ''
                return old, errors
            else:
                found_class = found_class.group(1)

        elif line.count('fast') and line.count('=') and (line.count('True') or line.count('False')):
            if found_class and found_flag_fast == '' and not line.strip().startswith('#'):
                found_flag_fast = 'True' if line.count('True') else 'False'
                if found_flag_fast and 'fast' not in flags: 
                    flags.append('fast')

        elif line.count('post') and line.count('=') and (line.count('True') or line.count('False')):
            if found_class and found_flag_post == '' and not line.strip().startswith('#'):
                found_flag_post = 'True' if line.count('True') else 'False'
                if found_flag_post and 'post' not in flags: 
                    flags.append('post')

        # elif line.count('fast') and line.count('=') and (line.count('True') or line.count('False')) and found_class:
        #     found_flag_fast = 'True' if line.count('True') else 'False'

        elif line.count('def A(self, event, arg):') and found_class:
            found_def_A = True
            paragraph_def_A = paragraph
            start_line = line_index
            
        elif line.count('newstate = self.state') and found_def_A:
            found_newstate = True
            
        elif line.count('return newstate') and found_def_A:
            found_return_newstate = True

        elif ( line.count('if self.state is') or line.count('if self.state ==') ) and found_class and found_def_A:
            if found_condition and found_state:
                link_id = processLink(name, found_condition, found_state, found_state)
                found_condition = ''
                if link_id:
                    A[found_state].append({'from': found_state, 
                                           'to': found_state, 
                                           'condition': D[name]['links'][link_id]['condition'],
                                           'link_id': link_id,})
            found_state = re.search('if self\.state == \'(.+?)\'.*?\:', line)
            if found_state is None:
                found_state = re.search('if self\.state is \'(.+?)\'.*?\:', line)
            if found_state is None:
                errors.append('ERROR    state not recognized in line %d' % line_index)
                found_state = ''
                return old, errors
            else:
                found_state = found_state.group(1)
                if found_state in D[name]['states']:
                    A[found_state] = []
                    states_found.append(found_state)
                else:
                    found_state = ''
                found_condition = ''

        elif ( line.count(' if ') or line.count(' elif ') ) and line.count(':') and found_state:
            if found_condition and found_state:
                link_id = processLink(name, found_condition, found_state, found_state)
                found_condition = ''
                if link_id:
                    A[found_state].append({'from': found_state, 
                                           'to': found_state, 
                                           'condition': D[name]['links'][link_id]['condition'],
                                           'link_id': link_id,})
            found_condition = re.search('if(.+?)\:', line, )
            if found_condition is None:
                errors.append('ERROR    condition not recognized in line %d' % line_index)
                found_condition = ''
                return old, errors
            else:
                found_condition = found_condition.group(1).strip()
#                print '    [%s]'%found_condition
                    
        elif line.count('self.state =') and found_state:
            state_to = re.search('self\.state = \'(.+?)\'', line)
            if state_to is None:
                errors.append('ERROR    transition state not recognized in line %d' % line_index)
                found_condition = ''
                return old, errors
            else:
                state_to = state_to.group(1)
                if found_condition:
                    link_id = processLink(name, found_condition, found_state, state_to)
                    found_condition = ''
                    if link_id:
                        A[found_state].append({'from': found_state, 
                                               'to': state_to, 
                                               'condition': D[name]['links'][link_id]['condition'],
                                               'link_id': link_id,})
                    
        else:
            if paragraph == paragraph_def_A:
                if found_condition and found_state:
                    link_id = processLink(name, found_condition, found_state, found_state)
                    found_condition = ''
                    if link_id:
                        A[found_state].append({'from': found_state, 
                                               'to': found_state, 
                                               'condition': D[name]['links'][link_id]['condition'],
                                               'link_id': link_id,})
                found_def_A = False
                found_state = ''
                found_condition = ''
                end_line = line_index
                break

    merged = ''
    state_index = 0  
    first_state = ''
    for state_index in range(len(states_found)):
        state = states_found[state_index]
        if state not in D[name]['states']:
            continue
        merged += '        #---%s---\n' % state
        if not first_state:
            merged += "        if self.state == '%s':\n" % state
            first_state = state
        else:
            merged += "        elif self.state == '%s':\n" % state
        has_actions = False
        for link_id, link_info in D[name]['links'].items():
            if link_info['from'] != state:
                continue
            found_link = False
            for link_index in range(len(A[state])):
                if link_id == A[state][link_index]['link_id']:
                    found_link = True
                    break
            if not found_link:
                A[state].append({  'from': link_info['from'], 
                                   'to': link_info['to'], 
                                   'condition': link_info['condition'],
                                   'link_id': link_id,})
                # print '    append '+link_info['condition'] 
        for link_index in range(len(A[state])):
            link_id = A[state][link_index]['link_id']
            condition = A[state][link_index]['condition']
            actions = D[name]['links'][link_id]['actions']
            # print link_id, actions
            if link_index == 0:
                merged += "            if %s :\n" % condition
            else:
                merged += "            elif %s :\n" % condition
            has_actions = has_actions or len(actions) > 0
            if len(actions) == 0:
                merged += "                pass\n"
            else:
                for action in actions:
                    merged += "                %s\n" % action
        if not has_actions:
            merged += "            pass\n"
            
    for state in D[name]['states']:
        if state in states_found:
            continue
        merged += '        #---%s---\n' % state
        if not first_state:
            merged += "        if self.state == '%s':\n" % state
            first_state = state
        else:
            merged += "        elif self.state == '%s':\n" % state
        has_actions = False
        first_link = ''
        for link_id, link_info in D[name]['links'].items():
            if link_info['from'] != state:
                continue
            condition = D[name]['links'][link_id]['condition']
            actions = D[name]['links'][link_id]['actions']
            if not first_link:
                merged += "            if %s :\n" % condition
                first_link = link_id
            else:
                merged += "            elif %s :\n" % condition
            has_actions = has_actions or len(actions) > 0
            if len(actions) == 0:
                merged += "                pass\n"
            else:
                for action in actions:
                    merged += "                %s\n" % action
        if not has_actions:
            merged += "            pass\n"
    
    if 'post' in flags:
        # if not found_newstate: 
            merged = '        newstate = self.state\n' + merged
    
    if 'post' in flags:
        merged += '        return newstate\n'
    else:
        merged += '        return None\n'
    
    if start_line >= 0 and end_line >= 0:
        src = ''
        src += '\n'.join(lines[:start_line])
        src += '\n' + merged + '\n'
        src += '\n'.join(lines[end_line-1:])
        src += '\n'
        return src, errors
    else:
        errors.append('    ERROR    not found State Machine code in existing file, start=%d, end=%d' % (start_line, end_line)) 
        return old, errors
        
def mergeMethods(old, new, name):
    global D
    if name not in D.keys():
        return old, []
    merged = ''
    errors = []
    lines = old.splitlines()
    start_line = -1
    end_line = -1
    last_not_empty_line_index = -1
    found_class = '' 
    found_def_A = False
    paragraph_class = -1
    paragraph_def_A = -1
    known_conditions = D[name]['conditions']
    known_actions = D[name]['actions']
    automat_method_line_index = -1
    non_automat_method_line_index = -1
    class_finished_line_index = -1

    for line_index in range(1, len(lines)+1):
        line = lines[line_index-1]
        if line.strip().startswith('#'):
            continue
        paragraph = len(line) - len(line.lstrip(' '))
        if line.strip():
            last_not_empty_line_index = line_index
            if found_class and paragraph <= paragraph_class and class_finished_line_index == -1:
                class_finished_line_index = line_index - 1
                if non_automat_method_line_index == -1:
                    non_automat_method_line_index = class_finished_line_index 

        if line.count('class ') and ( line.count('Automat') or line.count('automat.Automat')):
            found_class = re.search('class (\w+?)\(.*Automat.*\):', line)
            if found_class is None:
                found_class = re.search('class (\w+?)\(.*automat\.Automat.*\):', line)
            if found_class is None:
                errors.append('ERROR     class name not recognized in line %d' % line_index)
                found_class = ''
                return old, errors
            else:
                found_class = found_class.group(1)
                paragraph_class = paragraph

        elif line.count('def A(self, event, arg):') and found_class:
            found_def_A = True
            paragraph_def_A = paragraph
            start_line = line_index

        else:
            if paragraph <= paragraph_def_A and found_def_A:
                found_def_A = False
                end_line = line_index - 1
                # print 'end_line', end_line
                # class_finished_line_index = line_index - 1
            if paragraph <= paragraph_class and line.strip() != '' and end_line > 0 and class_finished_line_index == -1:
                class_finished_line_index = line_index - 1
                # print 'class_finished_line_index', class_finished_line_index
                
    if class_finished_line_index == -1 and end_line > 0:
        class_finished_line_index = last_not_empty_line_index + 1 

    if end_line < 0 or class_finished_line_index < 0:
        errors.append('    ERROR    not found State Machine code in existing file, end_class=%d, end_def=%d' % (class_finished_line_index, end_line))
        return old, errors

    merged = '\n'.join(lines[:end_line])
    merged += '\n'
    
    for line_index in range(end_line+1, len(lines)+1):
        line = lines[line_index-1]
        comment = line.strip().startswith('#')
        paragraph = len(line) - len(line.lstrip(' '))
        ln = line
        line = line.strip()
        
        if line.startswith('class '):
            merged += '\n'.join(lines[line_index-1:])
            non_automat_method_line_index = line_index - 1
            break
            # continue
        
        if not ( line.startswith('def ') and line.endswith(':') ):
            merged += ln + '\n'
            continue
        
        if paragraph != paragraph_def_A:
            merged += ln + '\n'
            continue
        
        method = line[line.find('def') + 4 : line.rfind(':')].strip(' ')
        if method[:2] not in ['is', 'do']:
            if non_automat_method_line_index < automat_method_line_index:
                non_automat_method_line_index = line_index - 1
            merged += ln + '\n'
            continue
        
        automat_method_line_index = line_index - 1
        
        params = method[method.find('(')+1 : method.rfind(')')]
        params = map(string.strip, params.split(','))
        ok = False
        if len(params) == 0:
            params = ['self', 'arg']
            ok = True
        elif len(params) == 1:
            if params[0] == 'self':
                params.append('arg')
                ok = True
        else:
            if params[0] == 'self':
                ok = True
        if not ok:
            print '        WARNING    non canonical function name in line %d: %s' % (line_index, method)
            params = ['self', 'arg']
            
        method_name = method[:method.find('(')]
        # print method_name
        
        found = False
        if method_name.startswith('is'):
            for condition in D[name]['conditions']:
                if condition.startswith('self.'+method_name+'('):
                    found = True
                    known_conditions.remove(condition)
                    # print '    ' + condition
                    break
        else:
            for action in D[name]['actions']:
                if action.startswith('self.'+method_name+'('):
                    found = True
                    known_actions.remove(action)
                    # print '    ' + action
                    break
        if not found:
            print '    WARNING    method %s in line %s is unused' % (method_name, line_index)
            merged += ln + '\n'
            continue
        
        merged += ' ' * paragraph + 'def ' + method_name + '(' + ', '.join(params) + '):\n'

    # print 'non_automat_method_line_index', non_automat_method_line_index 

    if non_automat_method_line_index == -1:
        non_automat_method_line_index = class_finished_line_index

    merged_lines = merged.splitlines()
    
    src = '\n'.join(merged_lines[:non_automat_method_line_index])
    src += '\n'

    for condition in known_conditions:
        print '    made empty method %s' % condition
        method = condition.replace('self.', 'def ').replace('(', '(self, ')+':'
        src += ' ' * paragraph_def_A + method + '\n'
        src += ' ' * (paragraph_def_A + 4) + '"""\n'
        src += ' ' * (paragraph_def_A + 4) + 'Condition method.\n'
        src += ' ' * (paragraph_def_A + 4) + '"""\n\n'

    for action in known_actions:
        print '    made empty method %s' % action
        method = action.replace('self.', 'def ').replace('(', '(self, ')+':'
        src += ' ' * paragraph_def_A + method + '\n'
        src += ' ' * (paragraph_def_A + 4) + '"""\n'
        src += ' ' * (paragraph_def_A + 4) + 'Action method.\n'
        src += ' ' * (paragraph_def_A + 4) + '"""\n\n'
    
    # src += '\n'
    src += '\n'.join(merged_lines[non_automat_method_line_index:])
    src += '\n'
        
    return src, errors

def mergeTimers(old, new, name):
    global D
    if name not in D.keys():
        return old, []
    if len(D[name]['timers']) == 0:
        return old, []
    errors = []
    lines = old.splitlines()
    start_line = -1
    end_line = -1
    found_class = '' 
    found_timers = False
    for line_index in range(1, len(lines)+1):
        line = lines[line_index-1]
        if line.strip().startswith('#'):
            continue
        paragraph = len(line) - len(line.lstrip(' '))
        if line.count('class ') and ( line.count('Automat') or line.count('automat.Automat')):
            found_class = re.search('class (\w+?)\(.*Automat.*\):', line)
            if found_class is None:
                found_class = re.search('class (\w+?)\(.*automat\.Automat.*\):', line)
            if found_class is None:
                errors.append('ERROR     class name not recognized in line %d' % line_index)
                found_class = ''
                return old, errors
            else:
                found_class = found_class.group(1)
        elif line.count('timers = {') and found_class:
            found_timers = True
            start_line = line_index
            if line.count('}'):
                end_line = line_index
                break
        elif line.count('}') and found_timers:
            end_line = line_index
            break
    if not found_class:
        errors.append('    ERROR    not found State Machine code in existing file')
        return old, errors
    if not found_timers:
        errors.append('    ERROR    not found timers in existing file')
        return old, errors
    stimers = ''
    for timer, states in D[name]['timers'].items():
        try:
            delay = timer[6:].strip()
            if delay.endswith('sec'):
                delay = delay[:-3]
                if delay.startswith('0') and '0.'+delay[1:] != delay:
                    delay = '0.'+delay[1:]
                delay = float(delay)
            elif delay.endswith('min'):
                delay = int(delay[:-3]) * 60
            elif delay.endswith('hour'):
                delay = int(delay[:-4]) * 60 * 60
            else:
                delay = 0
        except:
            delay = 0
        if delay == 0:
            errors.append('    WARNING: can not understand timer event: %s' % timer)
            continue
        stimers += "        '%s': (%s, [%s]),\n" % (timer, str(delay), ','.join(map(lambda x: "'%s'" % x, states)))
        
#    print start_line, end_line
#    print stimers
#    print '----'
#    print '\n'.join(lines[start_line-1:start_line])
#    print '----'
#    print '\n'.join(lines[end_line-1:end_line])
#    print '----'

    merged = '\n'.join(lines[:start_line])
    merged += '\n'
    merged += stimers
    merged += '\n'.join(lines[end_line-1:])
    merged += '\n'
    return merged, errors    
            

def mergeEvents(old, new, name):
    global D
    if name not in D.keys():
        return old, []
    if len(D[name]['events']) == 0:
        return old, []
    errors = []
    lines = old.splitlines()
    start_line = -1
    end_line = -1
    head_start_line = -1
    head_end_line = -1
    found_class = '' 
    found_heading = False
    found_events = False
    for line_index in range(1, len(lines)+1):
        line = lines[line_index-1]
        if line.strip().startswith('#'):
            continue
        paragraph = len(line) - len(line.lstrip(' '))
        if line.count('.. module::'):
            found_heading = True
            head_start_line = line_index
        elif line.count('"""') and found_heading and head_end_line == -1:
            head_end_line = line_index
        elif line.count('class ') and ( line.count('Automat') or line.count('automat.Automat')):
            found_class = re.search('class (\w+?)\(.*Automat.*\):', line)
            if found_class is None:
                found_class = re.search('class (\w+?)\(.*automat\.Automat.*\):', line)
            if found_class is None:
                errors.append('ERROR     class name not recognized in line %d' % line_index)
                found_class = ''
                return old, errors
            else:
                found_class = found_class.group(1)
        elif line.count('EVENTS:'):
            found_events = True
            start_line = line_index
            end_line = line_index
        elif line.count('* :red:`') and found_events:
            end_line = line_index
    if not found_class:
        errors.append('    ERROR    not found State Machine code in existing file')
        return old, errors
    if not found_events:
#         if not found_heading or head_end_line == -1:
            errors.append('    ERROR    not found "EVENTS:" marker in existing file')
            return old, errors
  #       start_line = head_end_line
 #        end_line = head_end_line - 1
    events = '\n'            
    events += 'EVENTS:\n'
    for event in sorted(D[name]['events']):
        events += '    * :red:`%s`\n' % event
    # events += '\n'
    merged = '\n'.join(lines[:start_line-1])
    merged += events
    merged += '\n'.join(lines[end_line:])
    merged += '\n'
    return merged, errors    


def mergeHeading(old, new, name):
    global D
    if name not in D.keys():
        return old, []
    merged = ''
    errors = []
    lines = old.splitlines()
    head_start_line = -1
    head_end_line = -1
    found_heading = False
    for line_index in range(1, len(lines)+1):
        line = lines[line_index-1]
        if line.strip().startswith('#'):
            continue
        paragraph = len(line) - len(line.lstrip(' '))
        if line.count('.. module::'):
            found_heading = True
            head_start_line = line_index
        elif line.count('"""') and found_heading and head_end_line == -1:
            head_end_line = line_index
    if not found_heading:
        head = '\n\n"""\n'
        head += '.. module:: %s\n' % name.replace('(', '').replace(')', '')
        head += '.. role:: red\n\n'
        if D[name]['label']:
            head += ' '.join(D[name]['label'].split('\\n'))
            head += '\n\n'
        head += '.. raw:: html\n\n'
        head += '    <a href="%s.png" target="_blank">\n' % name.replace('(', '').replace(')', '')
        head += '    <img src="%s.png" style="max-width:100%%;">\n' % name.replace('(', '').replace(')', '')
        head += '    </a>\n\n'
        head += '"""\n\n'
        merged += head
        merged += old
    else:
        merged = old
    return merged, errors    


def main():
    global D
    D = eval(open(sys.argv[1]).read())
    path_new = sys.argv[2]
    path_old = sys.argv[3]
    only_update = sys.argv[4] == '1'
    remove_new = sys.argv[5] == '1'
    dont_modify = sys.argv[6] == '1'
    files_new = os.listdir(path_new)
    files_old = os.listdir(path_old) 
    # print
    for filename in files_new:
        if not filename.endswith('.py'):
            continue
        filepath_new = os.path.abspath(os.path.join(path_new, filename))
        if not os.path.isfile(filepath_new):
            continue
        if not os.access(filepath_new, os.R_OK):
            print 'can not read file %s, do not have read permissions' % filepath_new
            continue
        filepath_old = os.path.abspath(os.path.join(path_old, filename))
        if os.path.isfile(filepath_old) and not os.access(filepath_old, os.W_OK):
            print 'do not have write permissions for file %s' % filepath_old
            continue
        automat_name = filename.replace('.py', '') + '()'
        filepath = os.path.join(path_old, filename)
        fp = filepath.ljust(50)
        
        src_new = open(filepath_new).read() 
    
        if filename not in files_old:
            if not only_update:
                open(filepath_old, 'w').write(src_new)
                print fp, '    new file created'.upper(), len(src_new), 'bytes long'
                continue
            # print fp, '    skip'.upper()
            continue
        
        fin = open(filepath_old)
        src_old = fin.read()
        fin.close()  
        src_merged = src_old        
        
        print 'process', fp
        
        src_merged, errors = mergeStateMachine(src_merged, src_new, automat_name)
        if errors:
            print fp, ' : mergeStateMachine()\n' + ( '\n    '.join(errors) )
            continue
        
        src_merged, errors = mergeMethods(src_merged, src_new, automat_name)
        if errors:
            print fp, ' : mergeMethods()\n    ' + ( '\n    '.join(errors) )
            continue
        
        src_merged, errors = mergeTimers(src_merged, src_new, automat_name)
        if errors:
            print fp, ' : mergeTimers()\n    ' + ( '\n    '.join(errors) )
            continue

        src_merged, errors = mergeHeading(src_merged, src_new, automat_name)
        if errors:
            print fp, ' : mergeHeading()\n    ' + ( '\n    '.join(errors) )
            continue

        src_merged, errors = mergeEvents(src_merged, src_new, automat_name)
        if errors:
            print fp, ' : mergeEvents()\n    ' + ( '\n    '.join(errors) )
            continue
        
        md5_old = hashlib.md5(src_old).hexdigest()
        md5_merged = hashlib.md5(src_merged).hexdigest()
        if md5_old != md5_merged:
            if dont_modify:
                print '    changed'.upper()
            else:
                print '    updated'.upper()

        if dont_modify:
            import difflib
            for line in difflib.unified_diff(src_old.splitlines(1), src_merged.splitlines(1)):
                sys.stdout.write(line)
            # d = difflib.Differ()
            # result = list(d.compare(src_old.splitlines(1), src_merged.splitlines(1)))
            # pprint.pprint(result)            
            # sys.stdout.writelines(result)
        else:
            # fout = open(filepath_old+'.new', 'w')
            if md5_old != md5_merged:
                fout = open(filepath_old, 'w')
                fout.write(src_merged)
                fout.close()
        
        # os.system('diff %s %s' % (filepath_old, filepath_old+'.new'))
        
        if remove_new:
            try:
                os.remove(filepath_new)
            except:
                print '    can not delete the file', filepath_new
                
        # if md5_old == md5_merged:
            # print fp, '    not changed'.upper()
            
        # if automat_name.count('fire_hire'):
        #     break
        
    # raw_input("\nPress ENTER to close the window")


   
if __name__ == '__main__':
    main()   


