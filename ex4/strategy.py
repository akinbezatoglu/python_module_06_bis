from abc import ABC, abstractmethod

from ex3.capability import TransformCapability
from ex3.creature import Creature


class InvalidStrategyError(Exception):
    pass


class BattleStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Creature) -> list[str]:
        pass

    def _invalid(self, creature: Creature) -> InvalidStrategyError:
        return InvalidStrategyError(
            f"Invalid Creature '{creature.name}' for this "
            f"{self.name.lower()} strategy"
        )


class NormalStrategy(BattleStrategy):
    @property
    def name(self) -> str:
        return "Normal"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, Creature)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise self._invalid(creature)
        return [creature.attack()]


class AggressiveStrategy(BattleStrategy):
    @property
    def name(self) -> str:
        return "Aggressive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        if not isinstance(creature, TransformCapability):
            raise self._invalid(creature)
        return [creature.transform(), creature.attack(), creature.revert()]
