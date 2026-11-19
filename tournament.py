from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
from ex3.creature import Creature
from ex4 import (
    AggressiveStrategy,
    BattleStrategy,
    InvalidStrategyError,
    NormalStrategy,
)


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    fighters: list[tuple[Creature, BattleStrategy]] = [
        (factory.create_base(), strategy) for factory, strategy in opponents
    ]
    roster: str = ", ".join(
        f"({creature.name}+{strategy.name})" for creature, strategy in fighters
    )
    print(f"[ {roster} ]")
    print("*** Tournament ***")
    print(f"{len(fighters)} opponents involved")
    try:
        for i, (creature_a, strategy_a) in enumerate(fighters):
            for creature_b, strategy_b in fighters[i + 1:]:
                print()
                print("* Battle *")
                print(creature_a.describe())
                print("vs.")
                print(creature_b.describe())
                print("now fight!")
                for line in strategy_a.act(creature_a):
                    print(line)
                for line in strategy_b.act(creature_b):
                    print(line)
    except InvalidStrategyError as err:
        print(f"Battle error, aborting tournament: {err}")


def main() -> None:
    flame: CreatureFactory = FlameFactory()
    transform: CreatureFactory = TransformCreatureFactory()
    normal: BattleStrategy = NormalStrategy()
    aggressive: BattleStrategy = AggressiveStrategy()

    print("Tournament 0 (basic)")
    battle([(flame, normal), (transform, aggressive)])
    print()
    print("Tournament 1 (error)")
    battle([(transform, aggressive), (flame, aggressive)])
    print()
    print("Tournament 2 (multiple)")
    battle([(flame, normal), (transform, aggressive), (flame, normal)])


if __name__ == "__main__":
    main()
