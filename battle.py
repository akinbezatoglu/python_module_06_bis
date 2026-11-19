from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
from ex3.creature import Creature


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    for creature in (factory.create_base(), factory.create_evolved()):
        print(creature.describe())
        print(creature.attack())


def test_battle(first: CreatureFactory, second: CreatureFactory) -> None:
    print("Testing battle")
    fighter_a: Creature = first.create_base()
    fighter_b: Creature = second.create_base()
    print(fighter_a.describe())
    print("vs.")
    print(fighter_b.describe())
    print("fight!")
    print(fighter_a.attack())
    print(fighter_b.attack())


def main() -> None:
    flame: CreatureFactory = FlameFactory()
    transform: CreatureFactory = TransformCreatureFactory()
    test_factory(flame)
    print()
    test_factory(transform)
    print()
    test_battle(flame, transform)


if __name__ == "__main__":
    main()
