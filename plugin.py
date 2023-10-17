import os

from modules.plugin_base import AbstractPlugin


class CMD:
    ROOT = "cp"
    MAKE = "c"
    SIZE = "size"
    ADD = "add"
    DELETE = "del"


class Config:
    TEMPLATE_FILE_PATH = "template_file_path"


class CpGen(AbstractPlugin):
    def _get_config_parent_dir(self) -> str:
        return os.path.abspath(os.path.dirname(__file__))

    @classmethod
    def get_plugin_name(cls) -> str:
        return "CpGen"

    @classmethod
    def get_plugin_description(cls) -> str:
        return "this plugin provides a templated generator, to generate meme couple messages for entertainment"

    @classmethod
    def get_plugin_version(cls) -> str:
        return "0.0.1"

    @classmethod
    def get_plugin_author(cls) -> str:
        return "Whth"

    def __register_all_config(self):
        self._config_registry.register_config(
            Config.TEMPLATE_FILE_PATH, f"{self._get_config_parent_dir()}/cp_data.json"
        )

    def install(self):
        from .template_managers import CpTemplateManager
        from modules.auth.resources import RequiredPermission
        from modules.auth.resources import required_perm_generator

        from modules.cmd import NameSpaceNode, ExecutableNode

        from modules.auth.permissions import PermissionCode
        from modules.auth.permissions import Permission

        self.__register_all_config()
        self._config_registry.load_config()

        su_perm = Permission(id=PermissionCode.SuperPermission.value, name=self.get_plugin_name())

        req_perm: RequiredPermission = required_perm_generator(
            target_resource_name=self.get_plugin_name(), super_permissions=[su_perm]
        )

        manager = CpTemplateManager(template_file_path=self._config_registry.get_config(Config.TEMPLATE_FILE_PATH))

        tree = NameSpaceNode(
            name=CMD.ROOT,
            help_message="Generate couple messages",
            required_permissions=req_perm,
            children_node=[
                ExecutableNode(
                    name=CMD.SIZE,
                    help_message="return the size of couple messages",
                    source=lambda: f"Template size:{len(manager.templates)}",
                ),
                ExecutableNode(
                    name=CMD.MAKE,
                    help_message=manager.make_meme_string.__doc__,
                    source=manager.make_meme_string,
                ),
                ExecutableNode(
                    name=CMD.ADD,
                    help_message=manager.add_template.__doc__,
                    source=manager.add_template,
                ),
                ExecutableNode(
                    name=CMD.DELETE,
                    help_message=manager.remove_template.__doc__,
                    source=manager.remove_template,
                ),
            ],
        )

        self._auth_manager.add_perm_from_req(req_perm)
        self._root_namespace_node.add_node(tree)
