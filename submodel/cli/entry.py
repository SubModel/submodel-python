"""
SubModel | CLI | Entry

The entry point for the CLI.
"""

import click

from .groups.config.commands import config_wizard
from .groups.exec.commands import exec_cli
from .groups.pod.commands import pod_cli
from .groups.project.commands import project_cli
from .groups.ssh.commands import ssh_cli


@click.group()
def submodel_cli():
    """A collection of CLI functions for SubModel."""


submodel_cli.add_command(config_wizard)  # submodel config

submodel_cli.add_command(ssh_cli)  # submodel ssh
submodel_cli.add_command(pod_cli)  # submodel pod
submodel_cli.add_command(exec_cli)  # submodel exec
submodel_cli.add_command(project_cli)  # submodel project
