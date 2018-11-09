#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
os.environ["PATH"] += os.pathsep + "C:\\Users\\Trac Quang Thinh\\Desktop\\Source\\graphviz-2.38\\bin"

from graphviz import Digraph
import copy


class DFA:
    def __init__(self, states, alphabets, init_state, final_states, transition_funct):
        self.states = states
        self.alphabets = alphabets
        self.init_state = init_state
        self.final_states = final_states
        self.transition_funct = transition_funct
        self.regex = ''
        self.ds = {}
        self.transition_dict = {}
        self.set_transition_dict()
        # self.draw_graph('', 'first')

    def draw_graph(self, label, name):
        gr = Digraph(format='svg')
        gr.attr('node', shape='point')
        gr.node('qi')
        for i in self.states:
            if i in self.final_states:
                gr.attr('node', shape='doublecircle', color='green', style='')
            elif i in self.init_state:
                gr.attr('node', shape='circle', color='black', style='')
            else:
                gr.attr('node', shape='circle', color='black', style='')
            gr.node(str(i))
            if i in self.init_state:
                gr.edge('qi', str(i), 'start')
        for k1, v1 in self.transition_dict.items():
            for k2, v2 in v1.items():
                if str(v2) != 'ϕ':
                    gr.edge(str(k1), str(k2), str(v2))
        gr.body.append(r'label = "\n\n{0}"'.format(label))
        gr.render('{0}'.format(name), view=True)

    def set_transition_dict(self):
        dict_states = {r: {c: 'ϕ' for c in self.states} for r in self.states}
        for i in self.states:
            for j in self.states:
                indices = [ii for ii, v in enumerate(self.transition_funct[i]) if v == j]  # get indices of states
                if len(indices) != 0:
                    dict_states[i][j] = '+'.join([str(self.alphabets[v]) for v in indices])
        self.ds = dict_states
        print(dict_states)
        self.transition_dict = copy.deepcopy(dict_states)

    def get_intermediate_states(self):
        return [state for state in self.states if state not in ([self.init_state] + self.final_states)]

    def get_predecessors(self, state):
        result = [key for key, value in self.ds.items() if state in value.keys() and value[state] != 'ϕ' and key != state]
        print('PRE', state, result)
        return result

    def get_successors(self, state):
        return [key for key, value in self.ds[state].items() if value != 'ϕ' and key != state]

    def get_if_loop(self, state):
        if self.ds[state][state] != 'ϕ':
            return self.ds[state][state]
        else:
            return ''

    def toregex(self):
        intermediate_states = self.get_intermediate_states()
        dict_states = self.ds

        for inter in intermediate_states:
            predecessors = self.get_predecessors(inter)
            successors = self.get_successors(inter)
            # print('inter : ', inter)
            # print('predecessor : ', predecessors)
            # print('successor : ', successors)

            # dd = {r: {c: 'ϕ' for c in self.states if c != inter} for r in self.states if r != inter}
            ##dd = {r: {c: 'ϕ' for c in temp_states if c != inter} for r in temp_states if r != inter}
            for i in predecessors:
                for j in successors:
                    inter_loop = self.get_if_loop(inter)
                    # print('i : ', i, ' j : ', j)
                    dict_states[i][j] = '+'.join(
                        ('(' + dict_states[i][j] + ')', 
                        ''.join(('(' + dict_states[i][inter] + ')', '(' + inter_loop + ')' + '*', '(' + dict_states[inter][j] + ')'))

                        ))

            dict_states = {r: {c: v for c, v in val.items() if c != inter} for r, val in dict_states.items() if
                           r != inter}  # remove inter node
            self.ds = copy.deepcopy(dict_states)

        init_loop = dict_states[self.init_state][self.init_state]
        init_to_final = dict_states[self.init_state][self.final_states[0]] + '(' + dict_states[self.final_states[0]][
            self.final_states[0]] + ')' + '*'
        final_to_init = dict_states[self.final_states[0]][self.init_state]
        re = '(' + '(' + init_loop + ')' + '+' + '(' + init_to_final + ')' + '(' + final_to_init + ')' + ')' + '*' + '(' + init_to_final + ')'
        #re = '(' + re + ')*'
        #print('Regular Expression : ', re)
        return re


def main():
    states = input('Enter the states in your DFA : ')
    states = states.split()
    alphabets = input('Enter the alphabets : ')
    alphabets = alphabets.split()
    init_state = input('Enter initial state : ')
    final_states = input('Enter the final states : ')
    final_states = final_states.split()
    print('Define the transition function : ')
    transition_matrix = [list(map(str, input().split())) for _ in range(len(states))]
    print(transition_matrix)
    transition_funct = dict(zip(states, transition_matrix))
    print(transition_funct)
    # print('transition funct : ', transition_funct)
    r = ''
    for f in final_states:
        #dfa = DFA(states, alphabets, init_state, final_states, transition_funct)
        # regex = dfa.toregex()

        dfa = DFA(states, alphabets, init_state, [f], transition_funct)
        r+= '+' + dfa.toregex()
    dfa.draw_graph('test', 'second')
    print(r[1:])
    # print(dfa.transition_dict)
    # print(dfa.ds)


if __name__ == '__main__':
    main()