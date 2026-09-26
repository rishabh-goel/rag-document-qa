# React UI: line-by-line walkthrough

This covers every non-blank line of the React/Vite frontend. Blank lines only group related code.

## `frontend/package.json`

| Line | Explanation |
| --- | --- |
| 1 | Opens the JSON package manifest. |
| 2 | Names the frontend package. |
| 3 | Prevents accidental publishing to npm. |
| 4 | Records the app's version. |
| 5 | Makes `.js` files ES modules, enabling `import` syntax. |
| 6 | Opens npm command aliases. |
| 7 | Runs Vite's local development server. It defaults to port 5173. |
| 8 | Produces an optimized static production build. |
| 9 | Serves that production build locally for inspection. |
| 10 | Closes the scripts object. |
| 11 | Opens runtime/build dependencies. |
| 12 | Adds Vite's React compiler and Fast Refresh integration. |
| 13 | Adds Vite, which bundles and serves the app. |
| 14 | Adds React's component and state APIs. |
| 15 | Adds React DOM, which mounts components in the browser. |
| 16 | Closes dependencies. |
| 17 | Leaves an empty dev-only dependency object; dependencies are currently all in the preceding section. |
| 18 | Closes the manifest. |

## `frontend/.env.example`

| Line | Explanation |
| --- | --- |
| 1 | Sets the backend URL exposed to Vite client code. Only variables beginning `VITE_` are made available in the browser bundle. |

## `frontend/index.html`

| Line | Explanation |
| --- | --- |
| 1 | Declares modern HTML. |
| 2 | Opens the document and sets its language for accessibility tools. |
| 3 | Opens metadata. |
| 4 | Uses UTF-8 characters. |
| 5 | Makes the layout scale correctly on phones. |
| 6 | Supplies a concise search/accessibility description. |
| 7 | Sets the browser-tab title. |
| 8 | Closes metadata. |
| 9 | Opens visible page content. |
| 10 | Creates the empty DOM element that React mounts into. |
| 11 | Loads the JavaScript entry module; Vite resolves and bundles it. |
| 12 | Closes body content. |
| 13 | Closes the HTML document. |

## `frontend/vite.config.js`

| Line | Explanation |
| --- | --- |
| 1 | Imports Vite's typed configuration helper. |
| 2 | Imports the React plugin. |
| 4 | Exports this project's Vite configuration. |
| 5 | Enables the React plugin, adding JSX transformation and Fast Refresh. |
| 6 | Closes the configuration. |

## `frontend/src/main.jsx`

| Line | Explanation |
| --- | --- |
| 1 | Imports React's development safety wrapper. |
| 2 | Imports the browser renderer that creates a React root. |
| 3 | Imports the top-level app component. |
| 4 | Imports global CSS so Vite includes it in the page. |
| 6 | Finds `<div id="root">` in `index.html`, creates a React root there, and begins rendering. |
| 7 | Enables extra development checks; it does not change the production UI. |
| 8 | Renders the entire application. |
| 9 | Closes `StrictMode`; the comma is accepted trailing-argument syntax. |
| 10 | Closes the render call. |

## `frontend/src/api.js`

| Line | Explanation |
| --- | --- |
| 1 | Reads `VITE_API_URL`, falls back to local FastAPI, then removes one trailing slash so combining it with `/documents` never produces `//documents`. |
| 3 | Starts the shared asynchronous HTTP helper; it receives a route and optional `fetch` settings. |
| 4 | Calls the backend with the combined URL and supplied options. |
| 5 | Starts non-success handling. |
| 6 | Attempts to decode FastAPI's JSON error, using an empty object if that fails. |
| 7 | Throws a JavaScript error with FastAPI's `detail` message or a status fallback. |
| 8 | Closes the error branch. |
| 9 | Returns `null` for a 204 empty response; otherwise parses and returns JSON. |
| 10 | Closes the helper. |
| 12 | Exports one reusable object for all API operations. |
| 13 | Gets the indexed-document list. |
| 14 | Starts the upload operation. |
| 15 | Creates browser multipart form data. |
| 16 | Uses the field name `file`, which matches FastAPI's upload parameter. |
| 17 | Posts the form without manually setting `Content-Type`; the browser supplies the required boundary. |
| 18 | Closes the upload method. |
| 19 | Sends a DELETE request for a specific document. |
| 20 | Starts the Q&A request. |
| 21 | Selects HTTP POST. |
| 22 | Declares that the body is JSON. |
| 23 | Serializes the expected FastAPI request body. |
| 24 | Closes the request options and `ask` method. |
| 25 | Closes the exported API object. |

## `frontend/src/App.jsx`

| Line | Explanation |
| --- | --- |
| 1 | Imports React hooks for state and first-render effects. |
| 2 | Imports the backend client. |
| 4 | Defines extensions accepted by the browser picker; server-side validation remains authoritative. |
| 6 | Declares a small component to display source citations. |
| 7 | Renders nothing when no sources were returned. Optional chaining avoids errors for `undefined`. |
| 8 | Starts the citation markup. |
| 9 | Creates an accessible source-list container. |
| 10 | Maps every source to one expandable item while retaining its index for display numbering. |
| 11 | Uses document ID plus chunk index as a stable React list key. |
| 12 | Starts the native expandable summary label. |
| 13 | Shows a human-readable source number and filename. |
| 14 | Adds the page suffix only for paginated sources. |
| 15 | Closes the summary. |
| 16 | Displays the source excerpt inside the expanded panel. |
| 17 | Closes the `<details>` item. |
| 18 | Closes the mapping expression. |
| 19 | Closes the citation container. |
| 20 | Closes JSX return. |
| 21 | Closes `SourceList`. |
| 23 | Declares the main application component. |
| 24 | Holds indexed documents and its setter. |
| 25 | Holds the local chat transcript and its setter. |
| 26 | Holds the controlled question-input value. |
| 27 | Holds the informational/error banner text. |
| 28 | Tracks an in-progress upload. |
| 29 | Tracks an in-progress answer request. |
| 31 | Defines a reusable async document-refresh function. |
| 32 | Starts error handling. |
| 33 | Fetches documents and stores them. |
| 34 | Clears an earlier warning after success. |
| 35 | Starts the failure case. |
| 36 | Shows a helpful backend-startup message without exposing implementation details. |
| 37 | Closes the failure case. |
| 38 | Closes the refresh function. |
| 40 | Runs an effect after initial mount. |
| 41 | Fetches the initial library. |
| 42 | Empty dependencies mean React runs this effect once per mount. |
| 44 | Defines the file-picker change handler. |
| 45 | Retrieves the first selected file safely. |
| 46 | Stops if the picker was cleared. |
| 47 | Shows the busy state. |
| 48 | Clears an old notice before a new attempt. |
| 49 | Starts upload error handling. |
| 50 | Uploads the selected file. |
| 51 | Refreshes the library after the backend indexes it. |
| 52 | Reports filename and created chunk count. |
| 53 | Starts failure handling. |
| 54 | Shows the backend/client error text. |
| 55 | Starts cleanup that always runs. |
| 56 | Ends the busy state. |
| 57 | Clears the native input so selecting the same file later triggers `onChange` again. |
| 58 | Closes cleanup. |
| 59 | Closes the upload handler. |
| 61 | Defines deletion for one document ID. |
| 62 | Starts error handling. |
| 63 | Calls the delete endpoint. |
| 64 | Refreshes the visible library. |
| 65 | Starts the failure branch. |
| 66 | Shows the error. |
| 67 | Closes the branch. |
| 68 | Closes the deletion handler. |
| 70 | Defines the question form handler. |
| 71 | Stops the browser from submitting/reloading the page. |
| 72 | Removes leading/trailing whitespace. |
| 73 | Rejects empty requests and double submits. |
| 74 | Clears the composer immediately. |
| 75 | Appends the user turn using functional state so concurrent updates are safe. |
| 76 | Shows answering state. |
| 77 | Clears any prior notice. |
| 78 | Starts answer error handling. |
| 79 | Calls `/ask` with the question. |
| 80 | Appends an assistant turn containing the answer and citations. |
| 81 | Starts failure handling. |
| 82 | Appends a visible assistant-style failure message to preserve chat context. |
| 83 | Starts cleanup. |
| 84 | Ends answering state. |
| 85 | Closes cleanup. |
| 86 | Closes question handler. |
| 88 | Starts the component's rendered interface. |
| 89 | Creates the overall layout wrapper. |
| 90 | Starts the document-library sidebar. |
| 91 | Starts the product-brand block. |
| 92 | Renders its decorative mark. |
| 93 | Renders product name and subtitle. |
| 94 | Closes brand block. |
| 95 | Uses a label as the clickable upload card and adds a busy CSS class conditionally. |
| 96 | Creates a hidden file picker with accepted types, change handler, and busy lock. |
| 97 | Renders the upload arrow. |
| 98 | Changes the upload-card label while indexing. |
| 99 | Lists supported formats. |
| 100 | Closes the upload label. |
| 101 | Starts the accessible document library. |
| 102 | Shows its title and current count. |
| 103 | Shows empty text or maps documents to rows. |
| 104 | Starts one keyed document row. |
| 105 | Renders its filename and chunk count. |
| 106 | Renders an accessible delete button that passes this document's ID. |
| 107 | Closes the row. |
| 108 | Closes the map/conditional expression. |
| 109 | Closes the library section. |
| 110 | Closes the sidebar. |
| 112 | Starts the main chat panel. |
| 113 | Renders product context, page heading, and status badge. |
| 114 | Renders an accessible notice only if it contains text. |
| 115 | Starts the live-updating conversation region for screen readers. |
| 116 | Shows onboarding content before the first message. |
| 117 | Maps saved messages to chat entries. |
| 118 | Gives each entry a role-based CSS class and a React key. |
| 119 | Renders the sender label. |
| 120 | Renders the message and its optional citations. |
| 121 | Closes the message entry. |
| 122 | Closes the map. |
| 123 | Shows animated retrieval text while waiting. |
| 124 | Closes conversation. |
| 125 | Starts a submit-capable composer form. |
| 126 | Creates a controlled input connected to `question`, locked during requests. |
| 127 | Creates a submit button disabled when busy or empty. |
| 128 | Closes the form. |
| 129 | Closes the chat panel. |
| 130 | Closes the overall layout. |
| 131 | Closes JSX return. |
| 132 | Closes `App`. |
| 134 | Exports `App` for the entry module. |

## `frontend/src/styles.css`

The stylesheet was deliberately compacted, so several selectors share a physical line. Each line below explains every selector group on that line.

| Line | Explanation |
| --- | --- |
| 1 | Sets global font fallbacks, page foreground/background colors, and disables synthetic font styling. |
| 2 | Makes all widths/heights include borders and padding. |
| 3 | Removes the browser body's default margin and keeps the layout usable from 320px wide. |
| 4 | Makes form controls inherit the app font. |
| 5 | Gives buttons a pointer cursor. |
| 6 | Creates the desktop two-column shell: a 288px sidebar plus flexible content, at least viewport height. |
| 7 | Styles the dark, vertically spaced sidebar. |
| 8 | Styles the brand row, bright mark, block display for text, and muted subtitle. |
| 9 | Styles the upload card, hover/busy/hidden-input variants, and its typography/icon. |
| 10 | Styles the library grid, heading, document rows and hover state, truncated filenames, delete button, and empty label. |
| 11 | Styles main-panel geometry, header, eyebrow, serif title, and green private-workspace status badge/dot. |
| 12 | Styles notice, scrolling conversation, onboarding content, message/citation components, and animated three-dot thinking indicator/keyframes. |
| 13 | Styles the input composer, focused field, submit button, disabled state, and green return-key accent. |
| 14 | At widths ≤720px, switches to a stacked layout, constrains the library, adjusts panel/header/badge, and narrows message labels/gaps. |
