Standard Software
===
Apps
---
* IntelliJ
* iTerm2
* Atom
  * language-fish-shell
  * language-rust
* FireFox
  * HTTPS Everywhere
  * LastPass
  * uBlock Origin

Command Line
---
* Fish Shell
* Oh My Fish
* git
* brew
* terminal-notifier

Misc
---
* Fonts: Hasklig, Source Code Pro, Fira Code

Setup
===
1. System Preferences
    * 'Automatically rearrange Spaces base on most recent use' off
1. Add to `$HOME/.config/fish/config.fish`
    * `source /Users/steve/Projects/zsh_env/config.fish`
1. Theme
    * Add theme to Oh My Fish. `ln -s $PROJECT_DIR/theme/ $HOME/.local/share/omf/themes devlocal`
    * If iTerm2 is set to have transparency, make sure 'Key background colors opaque' is checked
1. IntelliJ
    * Editor -> Font -> Font = Hasklig && Enable font ligatures
    * Appearance & Behavior -> Appearance -> Theme = Darcula
    * To enable time tracking
        1. Preferences -> Plugins -> Time Tracking -> enable
        1. Preferences -> Tools -> Tasks -> Time Tracking -> enable
1. iTerm2
    * Preferences -> Profiles -> Text
        * Use this strokes for anti-aliased text: With Dark Backgrounds
        * Font: 14pt Fira Code
        * Use Ligatures
        * Anti-aliased
    * Preferences -> Profiles -> Window
        * Transparency ~85%
        * Key background colors opaque
    

