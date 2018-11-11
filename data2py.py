#!/usr/bin/env python
# data2py.py
#
# Copyright (C) 2008-2016 Veselin Penev, http://bitdust.io
#
# This file (data2py.py) is part of BitDust Software.
#
# BitDust is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BitDust Software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with BitDust Software.  If not, see <http://www.gnu.org/licenses/>.
#
# Please contact us if you have any questions at bitdust.io@gmail.com


import os
import sys
import re
import string
import pprint


def split_name_vs_state(inp):
    if inp.count('(') == 1 and inp.count(')') == 1:
        name, _, state = inp.partition('(')
        state = state.rstrip(')')
        if state:
            return name, state
    return inp, 'AT_STARTUP'


def main():
    d = {}
    page = ''
    link_id = ''
    for line in open(sys.argv[1]).read().splitlines():
        line = line.strip()
        
        if line == '':
            continue
        #---page
        if line.startswith('page'):
            page = line.split(' ')[1].replace('-', '_')
            if page.startswith('Page'):
                page = page.replace('Page', 'Automat') 
            if not page.endswith('()'):
                page += '()'
            d[page] = {'states': [], 
                       'links': {}, 
                       'label': '', 
                       'errors': [], 
                       'actions': set(), 
                       'conditions': set(), 
                       'events': set(),
                       'timers': {},
                       'msgfunc': False,
                       'messages': [], }
            continue
        
        #---state
        if line.startswith('state'):
            state = line.split(' ')[1]
            d[page]['states'].append(state)
            continue
        
        #---label
        if line.startswith('label'):
            label = ' '.join(line.split(' ')[1:])
            d[page]['label'] = label
            continue
        
        #---link
        if line.startswith('link'):
            x, link_id, state_from, arrow, state_to = line.split(' ')
            state_from = state_from.strip('[]')
            state_to = state_to.strip('[]')
            d[page]['links'][link_id] = {'from': state_from, 
                                         'to':  state_to,
                                         'data': [],
                                         'condition': '',
                                         'actions': [],}
            continue

        #---ERROR!
        if line.startswith('ERROR!'):
            d[page]['errors'].append(line[6:])
            print('ERROR %s' % line[6:])
            continue

        words = line.strip('{}').split('#')
        color, style = words[:2]
        word = '#'.join(words[2:])
        word = word.replace('\\n', ' ').replace('  ', ' ')
        style = int(style)
        
        if len(d[page]['links'][link_id]['data']) > 0 and d[page]['links'][link_id]['data'][-1][0] == color:
            d[page]['links'][link_id]['data'][-1][2] += word
        else:
            d[page]['links'][link_id]['data'].append([color, style, word])
        
    # print
    print('Found %d pages in the file "%s"' % (len(d), sys.argv[1]))
    # print
   
    for page, info in d.items():
        filename = page.replace('()', '') + '.py'
        filepath = os.path.abspath(os.path.join(sys.argv[3], filename))
        print('creating %s' % filepath)
        automatname, begin_state = split_name_vs_state(page)
        # automatname = page.replace('()', '')
        classname = ''.join(map(string.capitalize, automatname.split('_')))
        label = info['label'].strip()
        modes = []
        if label:
            if label.count('\\n') >= 2 or label.lower().startswith('bitdust'):
                lbl = label.split('\\n')[1]
            else:
                lbl = label.split('\\n')[0]
            automatname, begin_state = split_name_vs_state(lbl)
            classname = ''.join(map(string.capitalize, automatname.split('_')))
            # automatname = lbl
            if label.endswith(']'):
                for mod in label.split('\\n')[-1].strip('[]').split(','):
                    modes.append(mod.strip())
        classname = classname.replace('(', '').replace(')', '')
        automatname = automatname.replace('(', '').replace(')', '')
        src = ''
        src_switch = ''
        src_actions = ''
        src_conditions = ''
        
        #---switch start
        for state_index in range(len(info['states'])):
            has_conditions = False
            state = info['states'][state_index]
            src += '        #---%s---\n' % state
            if state_index == 0:
                src += "        if self.state == '%s':\n" % state
            else:
                src += "        elif self.state == '%s':\n" % state

            link_index = 0

            for link_id, link in info['links'].items():

                if link['from'] != state:
                    continue

                condition = ''
                actions = []
                underlined = False
                is_action = False
                has_actions = False

                for color, style, word in link['data']:
                    if word.strip() == '':
                        continue

                    if style != 0:
                        underlined = True
                    if underlined and style == 0:
                        is_action = True
                    if word.strip().startswith('do') and color == '[0;0;255]':
                        is_action = True
                    if color == '[128;128;0]' and word.lower() == word and word.count('.state') == 0 and word.rstrip().endswith('('):
                        is_action = True 

                    if color == '[255;0;0]':
                        event = word.strip()
                        if is_action:
                            if event.count(','):
                                for e in event.split(','): 
                                    if e.strip():
                                        actions.append("'%s', " % e.strip())
                            else:
                                actions.append("'%s'" % event)
                        else: 
                            if condition and condition[-1] != ' ':
                                condition += ' '
                            condition += "event == '%s'" % event
                            d[page]['events'].add(event)
                            if event.count('timer'):
                                if event not in d[page]['timers']:
                                    d[page]['timers'][event] = []
                                if state not in d[page]['timers'][event]:
                                    d[page]['timers'][event].append(state) 

                    elif color == '[0;0;0]':
                        if is_action:
                            w = word.strip()
                            if w not in ['and', 'or', 'not', ',', ';', 'arg', 'args', 'kwargs']:
                                i = w.find('MSG')
                                if i >= 0:
                                    if i > 0:
                                        d[page]['messages'].append(w[i:])
                                        w = "%sself.msg('%s', *args, **kwargs)" % (w[:i-1], w[i:])
                                    else:
                                        d[page]['messages'].append(w)
                                        w = "self.msg('%s', *args, **kwargs)" % w
                                    d[page]['msgfunc'] = True
                                else:   
                                    if not ( w.count(' ') or w.count(',') ): 
                                        w = "'%s'" % w
                            if w != ';':
                                actions.append(w)
                        else:
                            if condition and condition[-1] != ' ':
                                condition += ' '
                            condition += word.lstrip() 

                    elif color == '[0;128;0]':
                        if condition and condition[-1] != ' ':
                            condition += ' '
                        # if word.count(')') > word.count('(') and word.count('(') == 1:
                        if re.search('is\w+?\(\)', word.strip()):
                            condition += 'self.' + word.strip().replace('()', '(*args, **kwargs)').lstrip()
                            d[page]['conditions'].add('self.' + word.strip().replace('()', '(*args, **kwargs)'))
                        elif re.search('is\w+?\(\w+?\)', word.strip()):
                            condition += 'self.' + word.strip().replace(')', ', *args, **kwargs)').lstrip()
                            d[page]['conditions'].add('self.' + word.strip().replace(')', ', *args, **kwargs)'))
                        elif word.count('.state'):
                            condition += word.strip().replace('.state', '.A().state')
                        elif word.count(','):
                            for w in word.split(','):
                                if w.strip().upper() == w.strip():
                                    condition += "'%s', " % w.strip()
                                else:
                                    condition += "%s, " % w.strip()
                        elif word.strip().upper() == word.strip():
                            condition += "'%s'" % word.strip()
                        elif word.strip().count('len('):
                            condition += word.strip().replace('len(', 'len(self.')
                        else:
                            condition += 'self.' + word.strip()

                    elif color == '[128;128;0]': 
                        if is_action:
                            actions.append("%s" % word.strip().replace('(', '.A('))
                        else:
                            if condition and condition[-1] != ' ':
                                condition += ' '
                            condition += '%s' % word.replace('().state', '.A().state').lstrip()

                    elif color == '[0;0;255]':
                        if is_action:
                            for nl in word.replace(';', '\n').split('\n'): 
                                for w in nl.split(' '):
                                    if w.strip():
                                        prefix = ''
                                        if w.lstrip().startswith('#'):
                                            i = 0
                                            nw = w.lstrip('# ')
                                            prefix = w[:len(w) - len(nw)]
                                            w = nw
                                        if re.match('^do\w+?\(\)$', w):
                                            actions.append(prefix + 'self.' + w.replace('()', '(*args, **kwargs)').strip())
                                        elif re.match('^do\w+?\(.*?MSG_\d+.*?\)$', w):
                                            def _repl(mo):
                                                d[page]['messages'].append(mo.group(1))
                                                d[page]['msgfunc'] = True
                                                return "self.msg('%s', *args, **kwargs)" % mo.group(1)
                                            w = re.sub('(MSG_\d+)', _repl, w.strip())
                                            actions.append(prefix + 'self.' + w)
                                        elif re.match('^do\w+?\(.+?\)$', w):
                                            actions.append(prefix + 'self.' + w.strip())
                                        elif re.match('^[\w\ ]+[\=\+\-\*\\\/\^\%\!\&]+[\w\ ]+?$', w):
                                            actions.append(prefix + 'self.' + w.strip())
                                        elif re.match('^[\w\_\ ]+\.[\w\_\ ]+\(\)$', w):
                                            actions.append(prefix + w.strip())
                                        elif w.strip() == 'pass':
                                            actions.append('pass')
                                        else:
                                            print('            ? %s %s' % (prefix, w))
                    else:
                        print('skipped: %s %s %s %s %s' %( link['from'], link['to'], color, style, word))

                if link['to'] != state:
                    if 'post' in modes:
                        if 'fast' in modes:
                            actions.append("newstate = '%s'" % link['to'])
                        else:
                            actions.append("self.state = '%s'" % link['to'])
                    else:
                        actions.insert(0, "self.state = '%s'" % link['to']) 

                condition = condition.strip()
                while True:
                    r = re.search('event == \'(\w+?)\.state\' is \'([\w\s\!\?\.\-]+?)\'', condition)
                    if r:
                        condition = re.sub('event == \'\w+?\.state\' is \'[\w\s\!\?\.\-]+?\'', '( event == \'%s.state\' and args[0] == \'%s\' )' % (r.group(1), r.group(2)), condition, 1)
                        # print 1, condition 
                    else:
                        break
                while True:
                    r = re.search('event == \'(\w+?)\.state\' == \'([\w\s\!\?\.\-]+?)\'', condition)
                    if r:
                        condition = re.sub('event == \'\w+?\.state\' == \'[\w\s\!\?\.\-]+?\'', '( event == \'%s.state\' and args[0] == \'%s\' )' % (r.group(1), r.group(2)), condition, 1)
                        # print 1, condition 
                    else:
                        break
                while True:
                    r = re.search('event == \'(\w+?)\.state\' in \[([\'\,\w\s\!\?\.\-]+?)\]', condition)
                    if r:
                        condition = re.sub('event == \'\w+?\.state\' in \[[\'\,\w\s\!\?\.\-]+?\]', '( event == \'%s.state\' and args[0] in [ %s ] )' % (r.group(1), r.group(2)), condition, 1)
                        # print 2, condition 
                    else:
                        break
                while True:
                    r = re.search('event == \'(\w+?)\.state\' not in \[([\'\,\w\s\!\?\.\-]+?)\]', condition)
                    if r:
                        condition = re.sub('event == \'\w+?\.state\' not in \[[\'\,\w\s\!\?\.\-]+?\]', '( event == \'%s.state\' and args[0] not in [ %s ] )' % (r.group(1), r.group(2)), condition, 1)
                        # print 3, condition 
                    else:
                        break
                condition = condition.replace('  ', ' ')

                has_conditions = True

                if link_index == 0:
                    src += "            if %s:\n" % condition
                else:
                    src += "            elif %s:\n" % condition

                d[page]['links'][link_id]['condition'] = condition

                has_actions = has_actions or len(actions) > 0

                opened = ''

                for action in actions:
                    if action.count('(') == 1 and action.count(')') == 1:
                        if action.find('(') > action.find(')'):
                            if opened:
                                opened += action.split(')')[0]+')'
                                action1 = opened
                                opened = ''
                                src += "                "
                                src += action1
                                src += '\n'
                                if action1.startswith('self.'):
                                    d[page]['actions'].add(action1)
                                d[page]['links'][link_id]['actions'].append(action1)
                            action = action.split(')')[1].lstrip()
                            opened = action
                        else:
                            if opened == '':
                                src += "                "
                                src += action
                                src += '\n'
                                if action.startswith('self.'):
                                    d[page]['actions'].add(action)
                                d[page]['links'][link_id]['actions'].append(action)
                            else:
                                opened += ' ' + action
                    elif action.count('(') == 1 and action.count(')') == 0:
                        if opened != '':
                            opened += action
                        else:
                            opened = action
                    elif action.count('(') == 0 and action.count(')') == 0:
                        if opened != '':
                            opened += action
                        else:
                            src += "                "
                            src += action
                            src += '\n'
                            d[page]['links'][link_id]['actions'].append(action)
                    elif action.count('(') == 0 and action.count(')') == 1:
                        if opened.count('(') < opened.count(')') + 1:
                            opened += action
                        else:
                            opened += action
                            action = opened
                            opened = ''
                            src += "                "
                            src += action
                            src += '\n'
                            if action.startswith('self.'):
                                d[page]['actions'].add(action)
                            d[page]['links'][link_id]['actions'].append(action)
                    elif action.count('(') == 2 and action.count(')') == 2 and action.count('self.msg') == 1:
                        funct = action[0:action.find('(')]
                        action1 = funct + '(*args, **kwargs)'
                        src += "                "
                        src += action
                        src += '\n'
                        found = False
                        for a in d[page]['actions']:
                            if a.startswith(funct):
                                found = True
                        if not found: 
                            if action.startswith('self.'):
                                d[page]['actions'].add(action1)
                        d[page]['links'][link_id]['actions'].append(action)
                    else:
                        print('            ? %s' % action)
                link_index += 1

                if not has_actions:
                    src += '                pass\n'

            if not has_conditions:
                src += '            pass\n'

        d[page]['conditions'] = list(d[page]['conditions'])
        d[page]['actions'] = list(d[page]['actions'])
        d[page]['events'] = list(d[page]['events'])

        #---switch end
        src_switch = src
        src = ''

        #---conditions
        func_names = set()
        for condition in d[page]['conditions']:
            if condition.count('(*args, **kwargs)'):
                func_name = condition.replace('self.', '').replace('(*args, **kwargs)', '')
                name = condition.replace('self.', '').replace('(*args, **kwargs)', '(self, *args, **kwargs)')
            else:
                func_name, _, func_args = condition.replace('self.', '').partition('(')
                func_args = func_args.replace('*args, **kwargs)', '')
                name = '%s(self, *args, **kwargs)' % func_name
            if func_name not in func_names:
                src += '    def %s:\n' % name
                src += '        """\n'
                src += '        Condition method.\n'
                src += '        """\n\n'
                func_names.add(func_name)

        src_conditions = src
        src = ''

        #---actions
        for action in d[page]['actions']:
            name = action.replace('self.', '').replace('(*args, **kwargs)', '(self, *args, **kwargs)')
            src += '    def %s:\n' % name
            if name.count('doDestroyMe'):
                src += '        """\n'
                src += '        Remove all references to the state machine object to destroy it.\n'
                src += '        """\n'
                src += '        self.destroy()\n\n'
            else:
                src += '        """\n'
                src += '        Action method.\n'
                src += '        """\n\n'

        src_actions = src
        src = ''

        #---header
        head = ''
        head += '''#!/usr/bin/env python
# {}.py
#
'''.format(automatname.replace('(', '').replace(')', ''))
        head += '\n\n"""\n'
        head += '.. module:: %s\n' % automatname.replace('(', '').replace(')', '')
        head += '.. role:: red\n\n'
        if label:
            head += ' '.join(label.split('\\n'))
            head += '\n\n'
        if False:
            head += '.. raw:: html\n\n'
            head += '    <a href="%s.png" target="_blank">\n' % automatname.replace('(', '').replace(')', '')
            head += '    <img src="%s.png" style="max-width:100%%;">\n' % automatname.replace('(', '').replace(')', '')
            head += '    </a>\n\n'
        head += 'EVENTS:\n'
        for event in sorted(d[page]['events']):
            head += '    * :red:`%s`\n' % event
        if len(d[page]['errors']) > 0:
            head += 'ERRORS:\n'
            for error in d[page]['errors']:
                head += '    * %s\n' % error
                print('    ERROR: %s' % error)
        head += '"""\n\n\n'
        head += 'from automats import automat\n\n\n'
        if True:
            head += '_%s = None\n\n\n' % classname
            head += 'def A(event=None, *args, **kwargs):\n'
            head += '    """\n'
            head += '    Access method to interact with `%s()` machine.\n' % automatname
            head += '    """\n'
            head += '    global _%s\n' % classname
            head += '    if event is None and arg is None:\n'
            head += '        return _%s\n' % classname
            head += '    if _%s is None:\n' % classname
            head += '        # set automat name and starting state here\n'
            head += '        _%s = %s(\'%s\', \'%s\')\n' % (classname, 
                                                            classname, 
                                                            automatname.replace('(', '').replace(')', ''), 
                                                            begin_state)
            head += '    if event is not None:\n'
            head += '        _%s.automat(event, *args, **kwargs)\n' % classname
            head += '    return _%s\n\n\n' % classname
            head += 'def Destroy():\n'
            head += '    """\n'
            head += '    Destroy `%s()` automat and remove its instance from memory.\n' % automatname 
            head += '    """\n'
            head += '    global _%s\n' % classname
            head += '    if _%s is None:\n' % classname
            head += '        return\n'
            head += '    _%s.destroy()\n' % classname
            head += '    del _%s\n' % classname
            head += '    _%s = None\n\n\n' % classname
        head += 'class %s(automat.Automat):\n' % classname
        head += '    """\n'
        head += '    This class implements all the functionality of ``%s()`` state machine.\n' % automatname.replace('(', '').replace(')', '')
        head += '    """\n\n'
        #---mode "fast"
        if 'fast' in modes:
            head += '    fast = True\n\n'
        #---mode "post"
        if 'post' in modes:
            head += '    post = True\n\n'
        if len(d[page]['timers']) > 0:
            head += '    timers = {\n'
            for timer, states in d[page]['timers'].items():
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
                    print('    WARNING: can not understand timer event: %s' % timer)
                    continue
                head += "        '%s': (%s, [%s]),\n" % (timer, str(delay), ', '.join(map(lambda x: "'%s'" % x, states)))
            head += '        }\n\n'
        if d[page]['msgfunc']:
            head += '    MESSAGES = {\n'
            for msg in sorted(set(d[page]['messages'])):
                head += "        '%s': '',\n" % msg 
            head += '        }\n\n'
            head += '    def msg(self, msgid, *args, **kwargs):\n'
            head += "        return self.MESSAGES.get(msgid, '')\n\n"
        head += '    def __init__(self, debug_level=0, log_events=False, log_transitions=False, publish_events=False, **kwargs):\n'
        head += '        """\n'
        head += '        Builds `%s()` state machine.\n' % (automatname,)
        head += '        """\n'
        head += '        super(%s, self).__init__(\n' % classname
        head += '            name="%s",\n' % automatname.replace('()','') 
        head += '            state="%s",\n' % begin_state
        head += '            debug_level=debug_level,\n'
        head += '            log_events=log_events,\n'
        head += '            log_transitions=log_transitions,\n'
        head += '            publish_events=publish_events,\n'
        head += '            **kwargs\n'
        head += '        )\n\n'
        head += '    def init(self):\n'
        head += '        """\n'
        head += '        Method to initialize additional variables and flags\n' 
        head += '        at creation phase of `%s()` machine.\n' % automatname
        head += '        """\n\n'
        head += '    def state_changed(self, oldstate, newstate, event, *args, **kwargs):\n'
        head += '        """\n'
        head += '        Method to catch the moment when `%s()` state were changed.\n' % automatname
        head += '        """\n\n'
        head += '    def state_not_changed(self, curstate, event, *args, **kwargs):\n'
        head += '        """\n'
        head += '        This method intended to catch the moment when some event was fired in the `%s()`\n' % automatname
        head += '        but automat state was not changed.\n'
        head += '        """\n\n'
        head += '    def A(self, event, *args, **kwargs):\n'
        head += '        """\n'
        head += '        The state machine code, generated using `visio2python <http://bitdust.io/visio2python/>`_ tool.\n'
        head += '        """\n'

        #---tail
        tail = ''
        if 'init' in d[page]['events']:
            if False:
                tail += '\n\ndef main():\n'
                tail += '    from twisted.internet import reactor\n'
                tail += "    reactor.callWhenRunning(A, 'init')\n"
                tail += '    reactor.run()\n\n'
                tail += 'if __name__ == "__main__":\n'
                tail += '    main()\n\n'

        #---modes
        if 'post' in modes and 'fast' in modes:
            head += '        newstate = self.state\n'
            src_switch += '        return newstate\n'

        src = head + src_switch + '\n\n' + src_conditions + src_actions + tail
        
        open(filepath, 'w').write(src)

    open(sys.argv[2], 'w').write(pprint.pformat(d))

    print('DONE! %d items wrote to %s' % (len(d), sys.argv[2]))
          
   
if __name__ == '__main__':
    try:
        main()
    except:
        import traceback
        traceback.print_exc()
