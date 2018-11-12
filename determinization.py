from automata import Automata
from copy import deepcopy

class Determinization:
  def __init__(self, nfa):
    self.dfa = self.construct(nfa)

  def get_dfa(self):
    return self.dfa

  def remove_empty(self, nfa):
    #generate states
    new_states = [] 
    for state in nfa.states:
      state_group = nfa.get_empty_by_state(state)
      inclusion = False
      for new_state in new_states:
        if state_group & new_state[1] == state_group:
          inclusion = True
          break
      if not inclusion:
        new_states.append((state, state_group))
    
    #generate transitions
    transitions = []
    for state in new_states:
      original_state = state[0]
      new_state = state[1]
      for state_ in new_states:
        if state_ != state:
          for s in state_[1]:
            if s in nfa.transitions and original_state in nfa.transitions[s]:
              alphabet = deepcopy(nfa.transitions[s][original_state])
              if len(alphabet)>0:
                alphabet = alphabet.pop()
                if alphabet != Automata.empty():
                  transitions.append((state_[1], alphabet, new_state))

    #generate loop transitions
    for state in new_states:
      new_state = state[1]
      for state_ in new_state:
        for s in new_state:
          if state_ in nfa.transitions and s in nfa.transitions[state_]:
            
            alphabet = deepcopy(nfa.transitions[state_][s])
            if len(alphabet)>0:
              alphabet = alphabet.pop()
              if alphabet != Automata.empty():
                transitions.append((new_state, alphabet, new_state))
    
    #map states
    map_states = dict()
    for i, state in enumerate(new_states):
      map_states[",".join(map(str,list(state[1])))] = i

    #map transitions
    transitions_ = []
    for transition in transitions:
      transitions_.append((map_states[",".join(map(str,list(transition[0])))],
        transition[1],map_states[",".join(map(str,list(transition[2])))]))
    transitions = transitions_

    new_nfa = Automata(alphabets=nfa.alphabets)
    #set start state
    for state in new_states:
      new_state = state[1]
      if nfa.start_state in new_state:
        new_nfa.set_start_state(map_states[",".join(map(str,list(new_state)))])
        break
    #set final states:
    for state in new_states:
      new_state = state[1]
      for final_state in nfa.final_states:
        if final_state in new_state:
          new_nfa.add_final_states(map_states[",".join(map(str,list(new_state)))])

    #add transitions
    for transition in transitions:
      state1 = transition[0]
      alphabet = transition[1]
      state2 = transition[2]
      new_nfa.add_transition(state1, state2, alphabet)

    return new_nfa

  def completion(self, nfa):
    nfa_transitions = deepcopy(nfa.transitions)
    for state, transitions in nfa_transitions.items():
      alphabets = set()
      for transition in transitions.values():
        while(1):
          if len(transition) == 0:
            break
          alphabets.add(transition.pop())
      if alphabets!=nfa.alphabets:
        difference = alphabets.symmetric_difference(nfa.alphabets)
        while(1):
          if len(difference) == 0:
            break
          nfa.add_transition(state, -1, difference.pop())
        for alphabet in nfa.alphabets:
          nfa.add_transition(-1, -1, alphabet)
    return nfa

  def check_deterministic(self, nfa):
    transitions = deepcopy(nfa.transitions)
    for state, trans in transitions.items():
      alphabets = []
      for tran in trans.values():
        while len(tran) > 0:
          alphabets.append(tran.pop())
      if sorted(alphabets) != sorted(list(nfa.alphabets)):
        print(state, alphabets, list(nfa.alphabets))
        return False
    return True


  def construct(self, nfa):
    nfa = self.remove_empty(nfa)
    nfa = self.completion(nfa)
    
    if self.check_deterministic(nfa):
      return nfa

    q = []
    dfa = Automata(alphabets=nfa.alphabets)
    dfa.set_start_state(nfa.start_state)

    nfa_transitions = dict()
    dfa_transitions = dict()

    for from_state, to_states in nfa.transitions.items():
      for to_state, trans in nfa.transitions[from_state].items():
        transition_symbol = list(trans)[0]
        if (from_state, transition_symbol) not in nfa_transitions:
          nfa_transitions[(from_state, transition_symbol)] = [to_state]
        else:
          nfa_transitions[(from_state, transition_symbol)].append(to_state)

    q.append((0,))

    for dfa_state in q:
      for alphabet in nfa.alphabets:
        if len(dfa_state) == 1 and (dfa_state[0], alphabet) in nfa_transitions:
          dfa_transitions[(dfa_state, alphabet)] = nfa_transitions[(dfa_state[0], alphabet)]
          q_new = dfa_transitions[(dfa_state, alphabet)]
          if tuple(q_new) not in q:
            q.append(tuple(q_new))
        else:
          destinations = []
          final_destination = []
          
          for nfa_state in dfa_state:
            if (nfa_state, alphabet) in nfa_transitions and nfa_transitions[(nfa_state, alphabet)] not in destinations:
              destinations.append(nfa_transitions[(nfa_state, alphabet)])

          if not destinations:
            final_destination.append(None)
          else:  
            for destination in destinations:
              for value in destination:
                if value not in final_destination:
                  final_destination.append(value)
              
          dfa_transitions[(dfa_state, alphabet)] = final_destination

          if tuple(final_destination) not in q:
              q.append(tuple(final_destination))

    for key in dfa_transitions:
      dfa.add_transition(q.index(tuple(key[0])), q.index(tuple(dfa_transitions[key])), key[1])

    for q_state in q:
      for nfa_final_state in nfa.final_states:
        if nfa_final_state in q_state:
          dfa.add_final_states(q.index(q_state))

    return dfa

from regex_to_automata import RegexToNFA
regex = "a*b(a+b)*"
converter = RegexToNFA(regex)
fa = converter.get_nfa()
# fa.draw_graph(regex, "./graphs/test1.svg", view=True)
# fa.draw_graph("test", "./graphs/test.svg", view=True)

determinization = Determinization(fa)
dfa = determinization.get_dfa()
# print(dfa)
dfa.draw_graph(regex, "./graphs/test.svg", view=True)

