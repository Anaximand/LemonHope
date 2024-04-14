# Settings in Lemon

Lemon handles per server settings, configurable via discord commands.

## Usage

All components must register their settings modules on start. This is done by calling `registerSettingsModule` with a unique `module` name (ie "quotes) and a unique list of `settingNames` (ie `["enabled", "exclude_channels"]`).
