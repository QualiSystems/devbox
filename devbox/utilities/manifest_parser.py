from toscaparser.tosca_template import ToscaTemplate


class ManifestParser(object):
    def parse(self, manifest_path):
        return ToscaTemplate(path=manifest_path, parsed_params=None, a_file=True)
