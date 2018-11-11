from graphviz import Digraph

class Automata:
  def __init__(self, alphabets = set(['a', 'b'])):
    self.states = set()
    self.start_state = None
    self.final_states = []
    self.transitions = dict()
    self.alphabets = alphabets

  @staticmethod
  def empty():
    return 'ε'

  def get_empty_by_state(self, state):
    results = set()
    states = set([state])
    while len(states)!= 0:
        state = states.pop()
        results.add(state)
        if state in self.transitions:
            for to_state in self.transitions[state]:
                if Automata.empty() in self.transitions[state][to_state] and to_state not in results:
                    states.add(to_state)
    return results

  def get_transitions(self, states, alphabet):
    if isinstance(states, int):
      states = [states]
    results = set()
    for state in states:
      if state in self.transitions:
        for to_state in self.transitions[state]:
          if alphabet in self.transitions[state][to_state]:
            results.add(alphabet)
    return results

  def set_start_state(self, state):
    self.start_state = state
    self.states.add(state)

  def add_final_states(self, state):
    if isinstance(state, int):
      state = [state]
    for s in state:
      if s not in self.final_states:
        self.final_states.append(s)

  def add_transition(self, from_state, to_state, alphabet):
    if isinstance(alphabet, str):
      alphabet = set([alphabet])
    self.states.add(from_state)
    self.states.add(to_state)
    if from_state in self.transitions:
      if to_state in self.transitions[from_state]:
        self.transitions[from_state][to_state] = self.transitions[from_state][to_state].union(alphabet)
      else:
        self.transitions[from_state][to_state] = alphabet
    else:
      self.transitions[from_state] = {to_state: alphabet}

  def add_transitions(self, transitions):
    for from_state, to_states in transitions.items():
      for state in to_states:
        self.add_transition(from_state, state, to_states[state])

  def print(self):
    print("States:", self.states)
    print("Start state:", self.start_state)
    print("Final states:", self.final_states)
    print("Transitions:")
    for f, t in self.transitions.items():
      for s in t:
        for c in t[s]:
          print("  ", f, "--", c, "->", s)
    print()

  def draw_graph(self, title, file_name, view=False):
    graph = Digraph(format='svg')
    graph.attr('node', shape='point')
    graph.node('qi')
    for s in self.states:
        if s in self.final_states:
            graph.attr('node', shape='doublecircle', color='green', style='')
        elif s == self.start_state:
            graph.attr('node', shape='circle', color='black', style='')
        else:
            graph.attr('node', shape='circle', color='black', style='')
        graph.node(str(s))
        if s == self.start_state:
            graph.edge('qi', str(s), 'start')
    for s in self.transitions.keys():
        for s_ in self.transitions[s].keys():
          path = ",".join(self.transitions[s][s_])
          if len(path) > 0:
            graph.edge(str(s), str(s_), str(path))
    graph.body.append(r'label = "\n\n{0}"'.format(title))
    graph.render('{0}'.format(file_name), view=view)

  def copy(self, start_state):
    translations = {}
    for i in list(self.states):
        translations[i] = start_state
        start_state += 1
    rebuild = Automata(self.alphabets)
    rebuild.set_start_state(translations[self.start_state])
    rebuild.add_final_states(translations[self.final_states[0]])
    for from_state, to_states in self.transitions.items():
        for state in to_states:
            rebuild.add_transition(translations[from_state], translations[state], to_states[state])
    return [rebuild, start_state]

