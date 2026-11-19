from ex3 import CreatureFactory, TransformCreatureFactory
from ex3.capability import TransformCapability
from ex3.creature import Creature


def main() -> None:
    print("Testing Creature with transform capability")
    factory: CreatureFactory = TransformCreatureFactory()
    stages: tuple[tuple[str, Creature], ...] = (
        ("base", factory.create_base()),
        ("evolved", factory.create_evolved()),
    )
    for label, creature in stages:
        print()
        print(f"{label}:")
        print(creature.describe())
        print(creature.attack())
        if isinstance(creature, TransformCapability):
            print(creature.transform())
            print(creature.attack())
            print(creature.revert())
        else:
            print(f"{creature.name} has no transform capability.")


if __name__ == "__main__":
    main()
