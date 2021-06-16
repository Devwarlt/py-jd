class JsonDescriptor(object):
    def __init__(
        self, level: int, parent_name: str,
        name: str, item: object
    ) -> None:
        self.__level: int = level
        self.__parent_name: str = parent_name
        self.__name: str = name
        self.__item: object = item
        self.__types: list = [type(item).__name__]
        self.__descriptors: list = []
        self.__jmespath: str = ""

    @property
    def jmespath(self) -> str:
        return self.__jmespath

    @property
    def level(self) -> str:
        return self.__level

    @property
    def parent_name(self) -> str:
        return self.__parent_name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def descriptors(self) -> list:
        return self.__descriptors

    @property
    def types(self) -> str:
        return self.__types

    def configure_jmespath(self, parent_jmespath: str = None) -> None:
        if self.level == 0:
            return ""
        is_prop_or_field: bool = self.name.startswith("properties of '")\
            or self.name.startswith("field of '")
        if parent_jmespath:
            self.__jmespath = f"{parent_jmespath}."
        if not is_prop_or_field:
            self.__jmespath += self.name
        else:
            self.__jmespath = parent_jmespath
        if not is_prop_or_field and\
            isinstance(self.__item, dict)\
                or isinstance(self.__item, list):
            self.__jmespath += "[]"

    def fetch_descendants(self) -> list:
        descendants: list = [self]
        next_level: int = self.level + 1
        if isinstance(self.__item, dict):
            item_dict: dict = self.__item
            for key, value in item_dict.items():
                descriptor: JsonDescriptor =\
                    JsonDescriptor(next_level, self.name, key, value)
                descriptor.configure_jmespath(self.jmespath)
                descendants += descriptor.fetch_descendants()
        if isinstance(self.__item, list):
            item_list: list = self.__item
            for item in item_list:
                item_name: str = ""
                if isinstance(item, list) or isinstance(item, dict):
                    item_name = f"propert{('ies' if len(item) > 1 else 'y')}"
                else:
                    item_name = "field"
                descriptor: JsonDescriptor =\
                    JsonDescriptor(
                        next_level, self.name,
                        f"{item_name} of '{self.name}'", item
                    )
                descriptor.configure_jmespath(self.jmespath)
                descendants += descriptor.fetch_descendants()
        return descendants

    def update_distinct(self, descriptor: object) -> bool:
        if not isinstance(descriptor, JsonDescriptor):
            raise TypeError(
                f"Expected type '{self.__class__.__name__}' and received "
                f"'{type(descriptor).__name__}'."
            )
        descriptor: JsonDescriptor = descriptor
        if descriptor.name != self.name\
                or descriptor.parent_name != self.parent_name\
                or descriptor.level != self.level:
            return False
        for inner_descriptor in descriptor.descriptors:
            inner_descriptor: JsonDescriptor = inner_descriptor
            has_descriptor: bool = all([
                child
                for child in self.descriptors
                if child.name == inner_descriptor.name
            ])
            if has_descriptor:
                continue
            self.__descriptors.append(inner_descriptor)
        for descriptor_type in descriptor.types:
            descriptor_type: str = descriptor_type
            if self.types.__contains__(descriptor_type):
                continue
            self.__types.append(descriptor_type)
        return True

    def update_inner_descriptor(self, descriptor: object) -> bool:
        if not isinstance(descriptor, JsonDescriptor):
            raise TypeError(
                f"Expected type '{self.__class__.__name__}' and received "
                f"'{type(descriptor).__name__}'."
            )
        descriptor: JsonDescriptor = descriptor
        if descriptor.parent_name == self.name:
            descriptor_ref: list = [
                ref
                for ref in self.descriptors
                if ref.name == descriptor.name
            ]
            if descriptor_ref:
                descriptor_ref: JsonDescriptor = descriptor_ref[0]
            else:
                descriptor_ref: JsonDescriptor = None

            if not descriptor_ref:
                self.__descriptors.append(descriptor)
            else:
                descriptor_ref.update_distinct(descriptor)
            return True
        else:
            for inner_descriptor in self.descriptors:
                inner_descriptor: JsonDescriptor = inner_descriptor
                if inner_descriptor.update_inner_descriptor(descriptor):
                    return True
        return False

    def generate_regular_navigation(self) -> str:
        output: str = ""
        has_descriptors: bool = len(self.descriptors) != 0
        name: str = f"[{('+' if has_descriptors else '-')}] {self.name}"
        output += f"{('.' * self.level)}{name}"
        output += f" (type{('s' if len(self.types) > 1 else '')}: "\
            f"{', '.join(self.types)})"
        if self.jmespath:
            output += f" | (JMESPath: {self.jmespath})"
        output += "\n"
        if has_descriptors:
            for inner_descriptor in self.descriptors:
                inner_descriptor: JsonDescriptor = inner_descriptor
                output += inner_descriptor.generate_regular_navigation()
        return output

    def generate_json_contract(self) -> dict:
        output: dict = {}
        has_descriptors: bool = len(self.descriptors) != 0
        if has_descriptors:
            descriptors: list = []
            for inner_descriptor in self.descriptors:
                inner_descriptor: JsonDescriptor = inner_descriptor
                json_contract: dict = inner_descriptor.generate_json_contract()
                descriptors.append(json_contract)
            output.update({self.name: descriptors})
        else:
            output.update({self.name: ', '.join(self.types)})
        return output

    def generate_jmespath_list(self) -> list:
        output: list = [self.jmespath]
        for inner_descriptor in self.descriptors:
            inner_descriptor: JsonDescriptor = inner_descriptor
            jmespath_list: list = inner_descriptor.generate_jmespath_list()
            output += jmespath_list
        return output
