"""
app/models/__init__.py

from https://github.com/tiangolo/sqlmodel/issues/121#issuecomment-935656778
Import the various model modules in one place and resolve forward refs.
"""


# AccountOutputWithCustomer.update_forward_refs(CustomerOutput=CustomerOutput)
# CustomerOutputWithAccounts.update_forward_refs(AccountOutput=AccountOutput)

import pkgutil
from pathlib import Path


def load_all_models() -> None:
    """Load all models from this folder."""
    package_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="app.models.",
    )

    # Add common folder as well for Refresh and access token tables
    import itertools

    modules = itertools.chain(
        modules,
        # pkgutil.walk_packages(
        #     path=[str(package_dir.joinpath("folder_name"))],
        #     prefix="app.models.folder_name.",
        # ),
    )

    for module in modules:
        # print(module.name)
        __import__(module.name)  # noqa: WPS421
