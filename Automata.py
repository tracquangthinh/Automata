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

  def get_trans_dict(self, matrix):
    # the shape of matrix is no.states * no.alphabet
    if len(matrix) < self.n_states or len(matrix[0]) < self.n_alphabets:
      raise Exception('The shape of transition matrix is not suitable')

    result = dict()
    for s in self.states:
      transition = dict()
      for s_ in self.states:
        transition[s_] = self.empty()
      result[s] = transition
    
    for i, s in enumerate(self.states):
      for j, a in enumerate(self.alphabets):
        reach_state = matrix[i][j]
        if reach_state in self.states:
          result[s][reach_state] = a
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
          path = self.transitions[s][s_]
          if path != self.empty():
            graph.edge(str(s), str(s_), str(path))
    graph.body.append(r'label = "\n\n{0}"'.format(title))
    graph.render('{0}'.format(file_name), view=True)

fa = Automata(['1', '2'], ['a', 'b'], [['1', '2'], ['@e@', '2']], '1', ['2'])
fa.draw_graph("Test", "test.svg")
