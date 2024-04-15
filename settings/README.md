# Settings in Lemon

Lemon handles per server settings, configurable via discord commands.

## Usage

All components must register their settings modules on start. This is done by calling class function `registerModule` with a unique list of `settingNames` (ie `["enabled", "exclude_channels"]`).
