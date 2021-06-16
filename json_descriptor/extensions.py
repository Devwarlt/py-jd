from typing import ItemsView
from json import dumps
from json_descriptor.descriptor import JsonDescriptor


def get_descriptor_details(content: dict) -> tuple:
    '''
    Return JSON Descriptor describing all properties and fields from a JSON
    object with distinct entries part of its contract.

    ---

    ### For unpacking

    - Argument 1 (type `str`): get as ouput the tree traversal navigation for
        current JSON object contract as plain-text.
    - Argument 2 (type `str`): get as output the tree traversal navigation for
        current JSON object contract as JSON with only distinct properties and
        types declaration as plain-text.
    - Argument 3 (type `str`): get as output the tree traversal navigation for
        current JSON object contract as plain-text with JMESPath instructions
        used to navigate through all JSON object pieces as plain-text.
    '''
    def __by_level(descriptor: JsonDescriptor) -> int:
        return descriptor.level
    content_items: ItemsView = content.items()
    sorted_content: list = sorted(content_items)
    sorted_content: dict = dict(sorted_content)
    descriptors: list = []
    for key, value in sorted_content.items():
        descriptor: JsonDescriptor = JsonDescriptor(1, "root", key, value)
        descriptor.configure_jmespath()
        descendants: list = descriptor.fetch_descendants()
        if descendants:
            descriptors += descendants
    sorted_descriptors: list = sorted(descriptors, key=__by_level)
    tree_traversal_descriptor: JsonDescriptor =\
        JsonDescriptor(0, "-", "root", {})
    for descriptor in sorted_descriptors:
        descriptor: JsonDescriptor = descriptor
        if tree_traversal_descriptor.update_distinct(descriptor):
            continue
        else:
            if tree_traversal_descriptor.update_inner_descriptor(descriptor):
                continue
            else:
                for inner_descriptor in tree_traversal_descriptor.descriptors:
                    inner_descriptor: JsonDescriptor = inner_descriptor
                    if inner_descriptor.update_distinct(descriptor):
                        break
                    else:
                        if inner_descriptor.update_inner_descriptor(descriptor):
                            break
    regular_navigation_output: str =\
        tree_traversal_descriptor.generate_regular_navigation()
    json_contract_output: dict =\
        tree_traversal_descriptor.generate_json_contract()
    jmespath_list_output: list =\
        tree_traversal_descriptor.generate_jmespath_list()

    def format_output(output: object) -> str:
        dumps_format: dict = {'sort_keys': True, 'indent': 3}
        return dumps(output, **dumps_format)

    return regular_navigation_output,\
        format_output(json_contract_output),\
        format_output(sorted(jmespath_list_output))
