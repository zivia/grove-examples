// Terminal Expansions
enum IdPrecondition { ON_BORDER, ON_NEST, ON_FOOD, HOLDING_FOOD }

enum IdBehavior { PICKUP_FOOD, DROP_FOOD, RANDOM_WALK, RETURN_HOME }

enum IdAction { PICKUP_FOOD, DROP_FOOD, RANDOM_WALK, RETURN_HOME }

enum Probability { P0.001, P0.005, P0.01, P0.025, P0.05, P0.075, P0.1, P1.0 }



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

struct Root {
	1: Behavior default_behavior = {"id_behavior": IdBehavior.RANDOM_WALK},
  2: list<Rule> rules = []
}
