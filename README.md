# Teragone Factory — VSCode Theme

Warm-expert light theme for long-form documentation work. Terracotta accents
(`#C85A2C`, sampled from the Factory wordmark) on a warm cream surface
(`#FDFBF7`). Never pure white, never pure black, never cold grey.

Built to match the Teragone Factory Typst slide template and MkDocs brand
layer used across long-form audit deliverables.

## Install (local, unpacked)

```bash
# Symlink into the VSCode extensions folder
ln -s "$(pwd)" ~/.vscode/extensions/teragone-factory.teragone-factory-theme-0.1.0

# Or package + install
npx @vscode/vsce package
code --install-extension teragone-factory-theme-0.1.0.vsix
```

Reload VSCode, then pick **Teragone Factory** in `Preferences → Color Theme`.

## Palette

| Token           | Hex       | Role                                  |
|-----------------|-----------|---------------------------------------|
| brand-primary   | `#C85A2C` | Accents, status bar, selection, links |
| brand-dark      | `#9E4421` | Keywords, hover                       |
| brand-soft      | `#FCEFE6` | Hover backgrounds                     |
| ink             | `#1A1614` | Title bar, activity bar               |
| text-primary    | `#2B2620` | Foreground                            |
| text-muted      | `#6B615A` | Secondary text                        |
| border          | `#D9D2C7` | Panel borders                         |
| surface         | `#FDFBF7` | Editor background                     |
| surface-muted   | `#F5F1EB` | Sidebar / panel background            |
| success         | `#4A7D5A` | Strings                               |
| warning         | `#C89025` | Numbers, modified                     |
| danger          | `#A63A2F` | Errors                                |

## License

MIT.
