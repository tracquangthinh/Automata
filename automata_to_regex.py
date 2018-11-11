# import os
# os.environ["PATH"] += os.pathsep + "C:\\Users\\Trac Quang Thinh\\Desktop\\Source\\graphviz-2.38\\bin"

from graphviz import Digraph
from copy import deepcopy

class Automata:
  def __init__(self, states, alphabets, transition_matrix, init_state, final_states):
    self.states = states
    self.alphabets = alphabets
    self.init_state = init_state
    self.final_states = final_states
    self.n_states = len(self.states)
    self.n_alphabets = len(self.alphabets)

    self.transitions = self.get_trans_dict(transition_matrix)
    print(self.transitions)

  @staticmethod
  def empty():
    return "@e@"

  @staticmethod
  def not_exist():
    return "@n@"

  def get_trans_dict(self, matrix):
    # the shape of matrix is no.states * no.alphabet
    if len(matrix) < self.n_states or len(matrix[0]) < self.n_alphabets:
      raise Exception('The shape of transition matrix is not suitable')

    result = dict()
    for s in self.states:
      transition = dict()
      for s_ in self.states:
        transition[s_] = []
      result[s] = transition
    
    for i, s in enumerate(self.states):
      for j, a in enumerate(self.alphabets):
        reach_states = matrix[i][j]
        for reach_state in reach_states:
          if reach_state in self.states:
            result[s][reach_state].append(a)
    return result

  def draw_graph(self, title, file_name):
    graph = Digraph(format='svg')
    graph.attr('node', shape='point')
    graph.node('qi')
    for s in self.states:
        if s in self.final_states:
            graph.attr('node', shape='doublecircle', color='green', style='')
        elif s in self.init_state:
            graph.attr('node', shape='circle', color='black', style='')
        else:
            graph.attr('node', shape='circle', color='black', style='')
        graph.node(str(s))
        if s in self.init_state:
            graph.edge('qi', str(s), 'start')
    for s in self.transitions.keys():
        for s_ in self.transitions[s].keys():
          path = ",".join(self.transitions[s][s_])
          if len(path) > 0 and path != self.not_exist():
            graph.edge(str(s), str(s_), str(path))
    graph.body.append(r'label = "\n\n{0}"'.format(title))
    graph.render('{0}'.format(file_name), view=False)

  def get_pre_states(self, state):
    return [s for s, trans in self.transitions.items() if state in trans and len(trans[state]) > 0 and state!=s]    

  def get_post_states(self, state):
    return [s for s, trans in self.transitions[state].items() if state!=s and len(trans) > 0]
  
  def get_inter_states(self):
    return [s for s in self.states if s not in [self.init_state] + self.final_states]

  def get_alphabet_loop(self, state):
    if len(self.transitions[state][state]) > 0:
      return '+'.join(self.transitions[state][state])
    else:
      return ''

  def to_regex(self):
    dict_states = deepcopy(self.transitions)
    inter_states = self.get_inter_states()
    
    if len(inter_states) > 0:
      for inter_state in inter_states:
        pre_states = self.get_pre_states(inter_state)
        post_states = self.get_post_states(inter_state)
        inter_loop = self.get_alphabet_loop(inter_state)
        for pre_state in pre_states:
          for post_state in post_states:
            new_tran = "+".join(dict_states[pre_state][post_state])
            if len(new_tran)>0:
              new_tran += "+"
            new_tran += "+".join(dict_states[pre_state][inter_state])
            if inter_loop != "":
              new_tran += inter_loop+"*"
            new_tran += "+".join(dict_states[inter_state][post_state])
            dict_states[pre_state][post_state] = '(' + new_tran + ')'

        print(dict_states)
        dict_states_ = dict()
        for state in dict_states.keys():
          if state != inter_state:
            trans = {}
            for s in dict_states[state].keys():
              if s != inter_state:
                trans[s] = dict_states[state][s]
            dict_states_[state] = trans

        dict_states = dict_states_

    init_loop = self.get_alphabet_loop(self.init_state)
    init_to_final = "".join(dict_states[self.init_state][self.final_states[0]])
    final_loop = self.get_alphabet_loop(self.final_states[0])
    final_to_init = "".join(dict_states[self.final_states[0]][self.init_state])

    result = ""
    if len(init_loop) > 1:
      result += '(' + init_loop + ')*'
    elif len(init_loop) == 1:
      result += init_loop + '*'
    print(init_to_final)
    result += init_to_final
    if len(final_loop) > 1:
      result += '(' + final_loop + ')*'
    elif len(final_loop) == 1:
      result += final_loop + '*'
    result += final_to_init
    result = '(' + result + ')*' + init_to_final
    return result

if __name__ == "__main__":
  states = []
  alphabets = []
  start_state = None
  final_states = []
  transitions = []

  test_file = "automata_to_regex_1"
  f = open('./test/'+test_file, "r")
  f.readline()
  states = f.readline().rstrip().split()
  f.readline()
  alphabets = f.readline().rstrip().split()
  f.readline()
  start_state = f.readline().rstrip()
  f.readline()
  final_states = f.readline().rstrip().split()
  f.readline()
  for s in states:
    seqs = f.readline().rstrip().split()
    tran = []
    for seq in seqs:
      tran.append(seq.split(','))
    transitions.append(tran)

  regex = ""
  for s in final_states:
    sfa = Automata(states, alphabets, transitions, start_state, [s])
    if len(regex) > 0:
      regex += "+"+sfa.to_regex()
    else:
      regex = sfa.to_regex()
  fa = Automata(states, alphabets, transitions, start_state, final_states)
  fa.draw_graph(regex, "./graphs/"+test_file+".svg")
