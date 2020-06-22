# Core Library
from abc import abstractmethod
from collections.abc import Collection
from typing import List


class AbstractTrie(Collection):
    @abstractmethod
    def autocomplete(self, prefix: str) -> List[str]:
        """Return a list of all words with the given prefix."""
        return []
