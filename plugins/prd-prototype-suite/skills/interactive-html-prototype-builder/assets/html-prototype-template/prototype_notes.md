# Interactive HTML Prototype Notes

## Scope

- Prototype type: interactive HTML
- Fidelity: low to mid
- Target surface: mobile

## Screens

- `home`: core entry screen.
- `detail`: detail review screen.
- `settings`: editable preference screen.

## Interactions

- `data-nav-target`: switches screens.
- `data-action="tab"`: switches tab panels.
- `data-action="open-modal"` / `close-modal`: controls the modal.
- `data-action="toast"`: shows lightweight feedback.
- Major task-entry buttons should navigate to destination screens and carry source context.

## Route Context

- Use destination pages or workflow panels for create, edit, review, optimize, compare, publish, dataset creation, and detail entry points.
- Show source context on the destination screen, such as selected item, report ID, filter, failure reason, or suggested next action.
- Include a visible return path back to the source screen.

## Platform Compatibility

- Open `index.html` directly on macOS or Windows.
- Use `standalone.html` when sharing only one file.
- Use only relative local paths.
- Copy the whole prototype folder when handing off.

## Review Questions

- Confirm the target device and main product path.
- Replace sample modules and copy with project-specific content.
