from abc import abstractmethod
import json


class JSer:
    """
    Abstract class allowing for JSON serialization and deserialization.
    """
    def serialize(self, jsonpath: str) -> None:
        """
        Write a json representing the current object to the given filepath
        :param filepath: <str>, location to serialize to
        """
        with open(jsonpath, 'w') as f:
            json.dump(self.serialized(), f)

    def serializes(self) -> str:
        """Serialize the current object as a string."""
        return json.dumps(self.serialized())

    @abstractmethod
    def serialized(self) -> dict:
        """Serialize the current object as a dictionary."""
        raise NotImplemented()

    def deserialize(self, jsonpath: str) -> object:
        """Deserializes the current object given a jsonpath containing a json describing it. Returns original object."""
        with open(jsonpath, 'r') as f:
            return self.deserialized(json.load(f))

    def deserializes(self, json_str: str) -> object:
        """Deserializes the current object given a json string describing it. Returns original object."""
        return self.deserialized(json.loads(json_str))

    @abstractmethod
    def deserialized(self, json_dict: dict) -> object:
        """Deserialize the current object given a dictionary describing it. Returns original object."""
        raise NotImplemented()
