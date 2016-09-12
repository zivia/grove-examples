// Actions Blacklists
const map<string, set<string>> idaction_blacklist = {
	'BEHAVIOR_4': ['BEHAVIOR_0', 'BEHAVIOR_1', 'BEHAVIOR_2', 'BEHAVIOR_3', 'BEHAVIOR_5', 'BEHAVIOR_6'],
	'BEHAVIOR_5': ['BEHAVIOR_4', 'BEHAVIOR_6'],
	'BEHAVIOR_6': ['BEHAVIOR_5']
}

const map<string, set<string>> idaction_whitelist = {
	'BEHAVIOR_6': ['BEHAVIOR_4']
}



// Terminal Expansions
enum IdPrecondition {
	PRECONDITION_0 = 0,
	PRECONDITION_1 = 1,
	PRECONDITION_2 = 2,
	PRECONDITION_3 = 3
}

enum IdBehavior {
  // BEHAVIOR_0 = 0,
  // BEHAVIOR_1 = 1,
  // BEHAVIOR_2 = 2,
  // BEHAVIOR_3 = 3,
  BEHAVIOR_4 = 4,
  BEHAVIOR_5 = 5,
  BEHAVIOR_6 = 6,
  BEHAVIOR_7 = 7,
}

enum IdAction {
  // ACTION_0 = 0,
  // ACTION_1 = 1,
  // ACTION_2 = 2,
  // ACTION_3 = 3,
  ACTION_4 = 4,
  ACTION_5 = 5,
  ACTION_6 = 6,
  ACTION_7 = 7,
}

enum Probability {
	PROB_0 = 0,
	PROB_1 = 1,
	PROB_2 = 2,
	PROB_3 = 3,
	PROB_4 = 4,
	PROB_5 = 5,
	PROB_6 = 6,
	PROB_7 = 7
}

enum ProbInitState {
	PROB_INIT_STATE_0 = 0,
	PROB_INIT_STATE_1 = 1,
	PROB_INIT_STATE_2 = 2,
	PROB_INIT_STATE_3 = 3,
	PROB_INIT_STATE_4 = 4,
	PROB_INIT_STATE_5 = 5,
	PROB_INIT_STATE_6 = 6,
	PROB_INIT_STATE_7 = 7,
	PROB_INIT_STATE_8 = 8,
	PROB_INIT_STATE_9 = 9
}



// Non-terminal Expansions
struct Precondition {
  1: IdPrecondition id_precondition
}

struct Behavior {
  1: IdBehavior id_behavior
}

struct Action {
  1: IdAction id_action,
  2: Probability prob
}

struct Rule {
  1: list<Precondition> preconditions = [],
  2: list<Behavior> behaviors = [],
  3: list<Action> actions = []
}

struct Initialization {
  1: ProbInitState init_1,
  2: ProbInitState init_2,
  3: ProbInitState init_3
}

struct Root {
  1: Initialization init,
	2: Behavior default_behavior,
  3: list<Rule> rules = []
}
