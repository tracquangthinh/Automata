from automata import Automata
from collections import Counter

class DFA(Automata):
  def __init__(self, states, alphabets, transition_matrix, init_state, final_states):
    print(transition_matrix)
    if self.empty() in alphabets:
      raise Exception("DFAs do not contain empty")
    
    for i in range(len(transition_matrix)):
      if self.not_exist() in transition_matrix[i]:
        raise Exception("The transition matrix is not suitable for DFA")
    
    super().__init__(states, alphabets, transition_matrix, init_state, final_states)


fa = DFA(['1', '2'], ['a', 'b'], [['1', '2'], ['2', '2']], '1', ['2'])