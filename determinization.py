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
      print("FUCK")
      return nfa

    new_nfa = Automata(alphabets=nfa.alphabets)
    nfa_transitions = deepcopy(nfa.transitions)

    combine_states = []
    new_transitions = []
    for state, transitions in nfa_transitions.items():
      alphabets = dict()
      for state_, transition in transitions.items():
        while(1):
          if len(transition) == 0:
            break
          a = transition.pop()
          if a not in alphabets:
            alphabets[a] = [state_]
          else:
            alphabets[a].append(state_)
      new_transitions.append((state, alphabets))

      for alphabet in alphabets.values():
        if len(alphabet) > 1:
          if alphabet not in combine_states:
            combine_states.append(alphabet)

    print(new_transitions)
    print(combine_states)

    #remove state belong combine state
    new_transitions_ = []
    for transition in new_transitions:
      state = transition[0]
      trans = transition[1]
      in_combine = False
      for combine_state in combine_states:
        if state in combine_state:
          new_transitions_.append((combine_state, trans))
          in_combine = True
      if not in_combine:
        new_transitions_.append(([state], trans))

    new_transitions = new_transitions_
    print(new_transitions)

    final_states = set()

    #replace combine state by a single state
    new_transitions_ = dict()
    max_state_index = max(nfa.states)+1
    for combine_state in combine_states:
      #get final state
      for final_state in nfa.final_states:
        if final_state in combine_state:
          final_states.add(max_state_index)

      for transition in new_transitions:
        if transition[0] == combine_state:
          new_transitions_[max_state_index] = dict()
          for alphabet in nfa.alphabets:
            if transition[1][alphabet] == combine_state:
              new_transitions_[max_state_index][alphabet] = max_state_index
            else:
              new_transitions_[max_state_index][alphabet] = transition[1][alphabet][0]
        else:
          new_transitions_[transition[0][0]] = dict()
          for alphabet, tran in transition[1].items():
            if tran == combine_state:
              new_transitions_[transition[0][0]][alphabet] = max_state_index
            else:
              new_transitions_[transition[0][0]][alphabet] = transition[1][alphabet][0]

      max_state_index += 1

    if len(new_transitions_) > 0:
      new_transitions = new_transitions_
    else:
      new_transitions_ = dict()
      for transition in new_transitions:
        i = transition[0][0]
        tran = dict()
        for alphabet in alphabets:
          tran[alphabet] = transition[1][alphabet][0]
        new_transitions_[i] = tran
      new_transitions = new_transitions_
    print(new_transitions)
    
    #map states
    new_states = new_transitions.keys()
    map_states = dict()
    for i, new_state in enumerate(new_states):
      map_states[new_state] = i
      if new_state in nfa.final_states:
        final_states.add(i)
    print(map_states)
    print(new_transitions)
    new_transitions_ = dict()
    for new_state in new_states:
      for alphabet in nfa.alphabets:
        print(new_state, alphabet)
        i = map_states[new_state]
        a = new_transitions[new_state][alphabet]
        if a in map_states:
          j = map_states[a]
          print("HAIZZ", j)
        else:
          map_states[a] = max(map_states.values())+1
        if i not in new_transitions_:
          new_transitions_[i] = dict()
        if j not in new_transitions_[i]:
          new_transitions_[i][j] = set()
        new_transitions_[i][j] = new_transitions_[i][j].union(alphabet)
    
    print(new_transitions)
    new_transitions = new_transitions_
    print(new_transitions)
    new_nfa.add_transitions(new_transitions)

    new_nfa.set_start_state(map_states[nfa.start_state])

    while 1:
      if len(final_states) == 0:
        break
      a = final_states.pop()
      if a in map_states:
        new_nfa.add_final_states(map_states[a])

    return new_nfa

from regex_to_automata import RegexToNFA
regex = "b*aba*"
converter = RegexToNFA(regex)
fa = converter.get_nfa()
# fa.draw_graph(regex, "./graphs/test1.svg", view=True)
# fa.draw_graph("test", "./graphs/test.svg", view=True)

determinization = Determinization(fa)
dfa = determinization.get_dfa()
# print(dfa)
dfa.draw_graph(regex, "./graphs/test.svg", view=True)

