from logging import Logger, getLogger
from typing import Dict, Optional

from sc_client.constants.sc_types import NODE_CONST_ROLE
from sc_client.core.sc_client_ import ScClient
from sc_client.models import ScAddr, ScIdtfResolveParams, ScType
from sc_client.sc_exceptions import ErrorNotes, InvalidValueError


class ScKeynodes:
    """Class which provides the ability to cache the identifier and ScAddr of keynodes stored in the KB."""

    def __init__(self, sc_client: ScClient) -> None:
        self._sc_client = sc_client
        self._dict: Dict[str, ScAddr] = {}
        self._logger: Logger = getLogger(f"{__name__}.{self.__class__.__name__}")
        self._max_rrel_index: int = 10

    def delete(self, identifier: str) -> bool:
        """Delete keynode from the kb and memory and return boolean status"""
        addr = self.get(identifier, required=True)
        del self._dict[identifier]
        return self._sc_client.delete_elements(addr)

    def get(self, identifier: str, required: bool = False) -> ScAddr:
        """Get keynode by `identifier`. If `required` is True, addr cannot be ScAddr(0), else InvalidValueError"""
        addr = self.resolve(identifier, None)
        if required and not addr.is_valid():
            self._logger.error("Failed to get ScAddr by %s keynode: ScAddr is invalid", identifier)
            raise InvalidValueError(ErrorNotes.SC_ADDR_OF_IDENTIFIER_IS_INVALID, identifier)
        return addr

    def resolve(self, identifier: str, sc_type: Optional[ScType]) -> ScAddr:
        """Get keynode. If `sc_type` is valid, an element will be created in the KB"""
        addr = self._dict.get(identifier)
        if addr is None:
            params = ScIdtfResolveParams(identifier, sc_type)
            addr = self._sc_client.resolve_keynodes(params)[0]
            if addr.is_valid():
                self._dict[identifier] = addr
            self._logger.debug("Resolved %s identifier with type %s: %s", repr(identifier), repr(sc_type), repr(addr))
        return addr

    def rrel_index(self, index: int) -> ScAddr:
        """Get rrel_i node, where i is `index`. Max rrel index is 10"""
        if not isinstance(index, int):
            raise TypeError("Index of rrel node must be int")
        if index > self._max_rrel_index:
            raise KeyError(f"You cannot use rrel more than {self._max_rrel_index}")
        return self.resolve(f"rrel_{index}", NODE_CONST_ROLE)
