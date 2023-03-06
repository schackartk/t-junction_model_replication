"""
Argparse Formatter Class
~~~
Custom class for formatting argparse help message

Authors: Kenneth Schackart <schackartk1@gmail.com>
"""

import argparse


# -------------------------------------------------------------------------------------
class CustomHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    """Custom Argparse help formatter"""

    def _get_help_string(self, action):
        """Suppress defaults that are None"""
        if action.default is None:
            return action.help
        return super()._get_help_string(action)

    def _format_action_invocation(self, action):
        """Show metavar only once"""
        if not action.option_strings:
            (metavar,) = self._metavar_formatter(action, action.dest)(1)
            return metavar
        parts = []
        if action.nargs == 0:
            parts.extend(action.option_strings)
        else:
            default = action.dest.upper()
            args_string = self._format_args(action, default)
            for option_string in action.option_strings:
                parts.append(f"{option_string}")
            parts[-1] += f" {args_string}"
        return ", ".join(parts)
