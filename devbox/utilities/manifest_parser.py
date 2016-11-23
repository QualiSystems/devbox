from collections import namedtuple
from toscaparser.tosca_template import ToscaTemplate

PROPERTIES = 'properties'

DEFAULT = 'default'

PORTS_BINDINGS = 'ports_bindings'
FILE = 'file'
ARTIFACTS = 'artifacts'
DEPLOYMENT_IMAGE = 'deployment_image'
DEPLOYMENT_COMMAND = 'deployment_command'
DEPLOYMENT_PORTS = 'deployment_ports'


Node = namedtuple('Node', ['name', 'properties', 'artifacts'])


class ManifestParser(object):
    def parse(self, manifest_path):
        tosca_template = ToscaTemplate(path=manifest_path, parsed_params=None, a_file=True)
        nodes = []
        for raw_node in tosca_template.topology_template.nodetemplates:
            node = self._get_node(raw_node)
            nodes.append(node)
        return nodes

    @staticmethod
    def _get_node(raw_node):
        """

        :param raw_node:
        :type raw_node: toscaparser.nodetemplate.NodeTemplate
        :return:
        """
        properties = raw_node.get_properties()
        entity_properties = raw_node.entity_tpl[PROPERTIES] if PROPERTIES in raw_node.entity_tpl else {}
        all_properties = {}
        for prop_name in properties:
            prop_value = properties[prop_name].default
            if prop_name in entity_properties and DEFAULT in entity_properties[prop_name]:
                prop_value = entity_properties[prop_name][DEFAULT]
            all_properties[prop_name] = prop_value

        artifacts = {}
        if ARTIFACTS in raw_node.entity_tpl and raw_node.entity_tpl[ARTIFACTS]:
            artifacts = raw_node.entity_tpl[ARTIFACTS]

        return Node(name=raw_node.name, properties=all_properties, artifacts=artifacts)

