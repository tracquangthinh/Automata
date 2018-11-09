import os
os.environ["PATH"] += os.pathsep + "C:\\Users\\Trac Quang Thinh\\Desktop\\Source\\graphviz-2.38\\bin"

from graphviz import Digraph

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
    dict_stages = self.transitions
    inter_states = self.inter_states()
    
    if len(inter_states) > 0:
      for inter_state in inter_states:
        pre_states = self.get_pre_states(inter_state)
        post_states = self.get_post_states(inter_state)
        inter_loop = self.get_alphabet_loop(inter_state)
        for pre_state in pre_states:
          for post_state in post_states:
            new_tran = "+".join(dict_stages[pre_state][post_state])
            new_tran = "+".join(new_tran, dict_stages[pre_state][inter_state])
            if inter_loop != "":
              new_tran = "+".join(new_tran, inter_loop+"*")
            new_tran = "+".join(new_tran, dict_stages[inter_state][post_state])
            dict_stages[pre_state][post_state] = new_tran

fa = Automata(['1', '2', '3'], ['a', 'b'], [[['3', '1'], ['2']], [['2'], ['3']], [['1'], ['3']]], '1', ['3'])
print(fa.get_inter_states())
fa.draw_graph("Test", "Graphs\\test.svg")
