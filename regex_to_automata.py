from automata import Automata

class AutomataConstruction:
  @staticmethod
  def basic_structure(alphabet):
    fa = Automata()
    fa.set_start_state(1)
    fa.add_final_states(2)
    fa.add_transition(1, 2, alphabet)
    return fa

  @staticmethod
  def dot_construct(automata_1, automata_2):
    [automata_1, m1] = automata_1.copy(1)
    [automata_2, m2] = automata_2.copy(m1)
    state1 = 1
    state2 = m2-1
    dot = Automata()
    dot.set_start_state(state1)
    dot.add_final_states(state2)
    dot.add_transition(automata_1.final_states[0], automata_2.start_state, Automata.empty())
    dot.add_transitions(automata_1.transitions)
    dot.add_transitions(automata_2.transitions)
    return dot

  @staticmethod
  def plus_construct(automata_1, automata_2):
    [automata_1, m1] = automata_1.copy(2)
    [automata_2, m2] = automata_2.copy(m1)
    state1 = 1
    state2 = m2
    plus = Automata()
    plus.set_start_state(state1)
    plus.add_final_states(state2)
    plus.add_transition(plus.start_state, automata_1.start_state, Automata.empty())
    plus.add_transition(plus.start_state, automata_2.start_state, Automata.empty())
    plus.add_transition(automata_1.final_states[0], plus.final_states[0], Automata.empty())
    plus.add_transition(automata_2.final_states[0], plus.final_states[0], Automata.empty())
    plus.add_transitions(automata_1.transitions)
    plus.add_transitions(automata_2.transitions)
    return plus

  @staticmethod
  def star_construct(automata_1):
    [automata_1, m1] = automata_1.copy(2)
    state1 = 1
    state2 = m1
    star = Automata()
    star.set_start_state(state1)
    star.add_final_states(state2)
    star.add_transition(star.start_state, automata_1.start_state, Automata.empty())
    star.add_transition(star.start_state, star.final_states[0], Automata.empty())
    star.add_transition(automata_1.final_states[0], star.final_states[0], Automata.empty())
    star.add_transition(automata_1.final_states[0], automata_1.start_state, Automata.empty())
    star.add_transitions(automata_1.transitions)
    return star

class RegexToNFA:
  def __init__(self, regex):
    self.operators = [RegexToNFA.plus(), RegexToNFA.dot()]
    self.regex = regex
    self.alphabets = [chr(i) for i in range(65,91)]
    self.alphabets.extend([chr(i) for i in range(97,123)])
    self.alphabets.extend([chr(i) for i in range(48,58)])
    self.construct_NFA()

  @staticmethod
  def star():
    return '*'

  @staticmethod
  def dot():
    return "."

  @staticmethod
  def plus():
    return '+'

  @staticmethod
  def opening_bracket():
    return '('

  @staticmethod
  def closing_bracket():
    return ')'

  def add_operator_to_stack(self, operator):
    while (1):
      if len(self.stack) == 0:
        break
      top = self.stack[-1]
      if top == RegexToNFA.opening_bracket():
        break
      if top == operator or top == RegexToNFA.dot():
        o = self.stack.pop()
        self.construct_sNFA(o)
      else:
        break
    self.stack.append(operator)

  def construct_sNFA(self, operator):
    if len(self.automata) == 0:
      raise Exception("Empty stack!")
    if operator == RegexToNFA.star():
      fa = self.automata.pop()
      self.automata.append(AutomataConstruction.star_construct(fa))
      # AutomataConstruction.star_construct(fa).print()
    elif operator in self.operators:
      if len(self.automata) < 2:
        raise Exception("Inadequate operands")
      fa_1 = self.automata.pop()
      fa_2 = self.automata.pop()
      if operator == RegexToNFA.plus():
        self.automata.append(AutomataConstruction.plus_construct(fa_2, fa_1))
      elif operator == RegexToNFA.dot():
        self.automata.append(AutomataConstruction.dot_construct(fa_2, fa_1))

  def construct_NFA(self):
    language = set()
    self.stack = []
    self.automata = []
    previous = Automata.empty()

    for char in self.regex:
      if char in self.alphabets:
        language.add(char)
        if previous != RegexToNFA.dot() and (previous in self.alphabets or previous in [RegexToNFA.closing_bracket(), RegexToNFA.star()]):
          self.add_operator_to_stack(RegexToNFA.dot())
        self.automata.append(AutomataConstruction.basic_structure(char))
      elif char == RegexToNFA.opening_bracket():
        if previous != RegexToNFA.dot() and (previous in self.alphabets or previous in [RegexToNFA.closing_bracket(), RegexToNFA.star()]):
          self.add_operator_to_stack(RegexToNFA.dot())
        self.stack.append(char)
      elif char == RegexToNFA.closing_bracket():
        while(1):
          if len(self.stack) == 0:
            raise Exception("Empty stack!")
          operator = self.stack.pop()
          if operator == RegexToNFA.opening_bracket():
            break
          elif operator in self.operators:
            self.construct_sNFA(operator)
      elif char == RegexToNFA.star():
        if previous in [RegexToNFA.star(), RegexToNFA.plus(), RegexToNFA.opening_bracket()]:
          raise Exception("No matching!")
        self.construct_sNFA(char)
      elif char in self.operators:
        if previous in self.operators or previous == RegexToNFA.opening_bracket():
          raise Exception("No matching!")
        else:
          self.add_operator_to_stack(char)
      else:
        raise Exception("No matching!")

      previous = char

    while (len(self.stack) > 0):
      operator = self.stack.pop()
      self.construct_sNFA(operator)

    self.nfa = self.automata.pop()
    self.nfa.alphabets = language

  def get_nfa(self):
    return self.nfa
          
if __name__=='__main__':
    regex = input("Regular expression: ")
    converter = RegexToNFA(regex)
    fa_ = converter.get_nfa()
    # # print(num)
    # print(fa_.get_empty_by_state(fa_.start_state))
    fa_.draw_graph(regex, "./graphs/"+regex+".svg", view=True)

