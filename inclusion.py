from automata import Automata

def complement(fa):
  new_final_states = []
  for state in fa.states:
    if state not in fa.final_states:
      new_final_states.append(state)

  fa_c = Automata(fa.alphabets)
  fa_c.set_start_state(fa.start_state)
  fa_c.add_final_states(new_final_states)
  fa_c.add_transitions(fa.transitions)

  return fa_c
  
def intersection(fa_1, fa_2):
  fa = Automata(fa_1.alphabets)
  states = []
  for s1 in fa_1.states:
    for s2 in fa_2.states:
      states.append((s1, s2))

  start = (fa_1.start_state, fa_2.start_state)
  fa.set_start_state(",".join(start))
  
  final_states = []
  for (s1, s2) in states:
    if s1 in fa_1.final_states and s2 in fa_2.final_states:
      final_states.append((s1, s2))
      final = ",".join((s1, s2))
      fa.add_final_states(final)
      
      
  for (s1, s2) in states:
    for alphabet in fa_1.alphabets: 
      next_s1 = list(fa_1.get_transitions(s1, alphabet))[0]
      next_s2 = list(fa_2.get_transitions(s2, alphabet))[0]
      start = ",".join((s1, s2))
      to = ",".join((next_s1, next_s2))
      fa.add_transition(start, to, alphabet)
    
  return fa
  
def reachable(fa, iteration, state):
  print(iteration, state)
  if iteration > 10:
    return False
  pre_states = fa.get_pre_states(state)
  if fa.start_state in pre_states:
    return True
  else:
    if len(pre_states) > 0:
      for pre_state in pre_states:
        return reachable(fa, iteration+1, pre_state)
    else:
      return False

# decide L(fa_1) belongs to L(fa_2) or not
def inclusion(fa_1, fa_2):
  fa_2_c = complement(fa_2)
  fa = intersection(fa_1, fa_2_c)
  fa.draw_graph("inclusion", "./graphs/inclusion.svg")
  for final_state in fa.final_states:
    if reachable(fa, 0, final_state):
      return False
  return True

def generate_fa(file):
  states = []
  alphabets = []
  start_state = None
  final_states = []
  transitions = []

  f = open(file, "r")
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

  fa = Automata(alphabets)
  fa.set_start_state(start_state)
  fa.add_final_states(final_states)
  for i, transition in enumerate(transitions):
    for j, alphabet in enumerate(alphabets):
      fa.add_transition(states[i], transitions[i][j][0], alphabet)
  return fa
  
      

if __name__ == "__main__":
  fa_1= generate_fa("./test/intersection_1")
  fa_1.print()

  fa_2 = generate_fa("./test/intersection_2")
  fa_2.print()

  print(inclusion(fa_1, fa_2))
