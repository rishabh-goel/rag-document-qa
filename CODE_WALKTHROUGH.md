# Line-by-line walkthrough

This describes every non-blank source/configuration line. Blank lines only separate logical blocks. The two `.gitkeep` files are intentionally empty placeholders that cause Git to retain otherwise-empty storage directories.

## `.env.example`

| Line | Meaning |
| --- | --- |
| 1 | Documents that an OpenAI key is needed when OpenAI generation is enabled. |
| 2 | Declares the key setting; the user supplies its value in their private `.env`. |
| 3 | Selects the answer-generation provider. `openai` invokes the OpenAI SDK; `none` returns retrieval output only. |
| 4 | Chooses the OpenAI model passed to the Responses API. |
| 6 | Documents that the following filesystem paths are relative to the directory in which the server is started. |
| 7 | Sets the directory for stored upload originals. |
| 8 | Sets the persistent Chroma vector-database directory. |
| 9 | Sets the JSON file that records document-level metadata. |
| 10 | Selects the SentenceTransformers embedding model. |
| 11 | Sets the maximum chunk length in characters. Python permits underscores in integer literals. |
| 12 | Sets how many ending characters are repeated in the next chunk. |
| 13 | Sets the default number of retrieved chunks. |

## `.gitignore`

| Line | Meaning |
| --- | --- |
| 1 | Prevents private API keys in `.env` from being committed. |
| 2 | Ignores Python bytecode directories. |
| 3 | Ignores individual Python bytecode files. |
| 4 | Ignores pytest's local cache. |
| 5 | Ignores uploaded user files. |
| 6 | Re-includes the placeholder file so the upload directory exists in a fresh clone. |
| 7 | Ignores the runtime JSON registry. |
| 8 | Ignores generated Chroma database files. |
| 9 | Re-includes Chroma's directory placeholder. |

## `requirements.txt`

| Line | Meaning |
| --- | --- |
| 1 | Installs FastAPI, the HTTP API framework. |
| 2 | Installs Uvicorn, the ASGI server; `standard` adds common performance/development extras. |
| 3 | Enables FastAPI multipart file uploads. |
| 4 | Loads typed settings from environment variables and `.env`. |
| 5 | Installs the persistent vector store. |
| 6 | Installs local embedding-model support. |
| 7 | Installs the OpenAI Python SDK. |
| 8 | Installs PyMuPDF (`fitz`) for PDF text extraction. |
| 9 | Installs DOCX parsing support. |
| 10 | Installs pandas; it is not used by this MVP and can be removed unless CSV/data-frame work is added. |
| 11 | Installs the web UI framework. |
| 12 | Installs the UI's HTTP client. |
| 13 | Installs the test runner. |

## `README.md`

| Lines | Meaning |
| --- | --- |
| 1 | Top-level project title. |
| 3 | One-sentence summary of supported inputs, retrieval, and cited generation. |
| 5 | Starts the setup section. |
| 7 | Introduces setup step one. |
| 9–13 | Opens a shell code block and gives the commands to create/activate a virtual environment and install dependencies. |
| 15 | Introduces configuration step two. |
| 17–20 | Opens a shell block that copies the template into the private runtime `.env` and reminds the user to add a key. |
| 22 | Explains the offline/retrieval-only provider option. |
| 24 | Introduces startup step three. |
| 26–29 | Shows separate commands to start the backend and UI. |
| 31 | Gives the Streamlit UI and FastAPI documentation URLs. |
| 33 | Starts the API reference section. |
| 35 | Defines the upload/index route and its multipart field. |
| 36 | Defines the list route. |
| 37 | Defines the delete route. |
| 38 | Defines the question route and example JSON body. |
| 40 | Explains the response's answer/source payload. |
| 42 | Starts design notes. |
| 44 | Explains local embeddings and the first-run model download. |
| 45 | Explains which runtime data is persisted. |
| 46 | Explains the grounding instruction supplied to the LLM. |
| 47 | Explains the deliberately simple chunker and a future upgrade path. |
| 49 | Starts verification instructions. |
| 51–53 | Shows the pytest command in a shell block. |

## `app/__init__.py`

| Line | Meaning |
| --- | --- |
| 1 | Module docstring: makes `app` a Python package and documents its purpose. |

## `app/config.py`

| Line | Meaning |
| --- | --- |
| 1 | Imports `Path` for platform-safe filesystem paths. |
| 3 | Imports Pydantic's environment-settings base class and configuration helper. |
| 6 | Starts the typed application-settings model. |
| 7 | Loads `.env` automatically and silently ignores unrelated environment variables. |
| 9 | Sets the human-readable application name. |
| 10 | Sets the upload path default. |
| 11 | Sets the Chroma path default. |
| 12 | Sets the registry-file path default. |
| 13 | Sets the embedding-model default. |
| 14 | Sets the default maximum chunk size. |
| 15 | Sets the default chunk overlap. |
| 16 | Sets the default retrieval count. |
| 17 | Sets OpenAI as the default generation provider. |
| 18 | Declares an optional API-key setting; `None` is valid until generation is requested. |
| 19 | Sets the model-name default. |
| 21 | Starts a helper that makes required runtime directories. |
| 22 | Creates the upload directory and any missing parent directories; it does not fail if already present. |
| 23 | Does the same for the Chroma directory. |
| 24 | Creates the parent directory of the JSON registry. |
| 27 | Instantiates the singleton settings object, reading defaults and environment overrides. |
| 28 | Ensures paths exist immediately when this module is imported. |

## `app/schemas.py`

| Line | Meaning |
| --- | --- |
| 1 | Imports the type used for upload timestamps. |
| 3 | Imports Pydantic's model base and constrained-field helper. |
| 6 | Starts the response/model for one indexed document. |
| 7 | Declares its stable UUID. |
| 8 | Declares its original, user-visible filename. |
| 9 | Declares an optional upload MIME type and default. |
| 10 | Declares the number of vector chunks created. |
| 11 | Declares the UTC upload timestamp. |
| 14 | Starts the model for one retrieved citation. |
| 15 | Declares the source document UUID. |
| 16 | Declares its filename. |
| 17 | Declares an optional one-based PDF page number. |
| 18 | Declares the chunk's zero-based index in its document. |
| 19 | Declares the UI preview excerpt. |
| 20 | Declares a relevance float constrained to 0 through 1. |
| 23 | Starts the validated request body for questions. |
| 24 | Requires a nontrivial question of 2–4,000 characters. |
| 25 | Adds an optional restriction to selected document IDs. |
| 26 | Adds an optional retrieval-count override constrained to 1–10. |
| 29 | Starts the validated answer response. |
| 30 | Declares the generated answer text. |
| 31 | Declares its list of citations. |
| 34 | Starts the validated upload response envelope. |
| 35 | Places the created document model under `document`. |

## `app/documents.py`

| Line | Meaning |
| --- | --- |
| 1 | Describes this module's extraction and chunking role. |
| 3 | Postpones annotation evaluation, supporting modern type syntax consistently. |
| 5 | Imports CSV parsing. |
| 6 | Imports `io`; it is unused in this version and can be removed. |
| 7 | Imports the dataclass decorator. |
| 8 | Imports filesystem paths. |
| 10 | Imports PyMuPDF under its standard `fitz` module name. |
| 11 | Imports the Word-document parser. |
| 14 | Defines the accepted filename extensions. |
| 17 | Makes the following small data container a dataclass. |
| 18 | Starts an immutable `PageText` record. |
| 19 | Stores extracted text. |
| 20 | Stores a one-based page number or `None` for formats without pages. |
| 23 | Starts extraction for one stored upload. |
| 24 | Normalizes the extension to lowercase. |
| 25 | Branches for PDF input. |
| 26 | Opens the PDF with automatic closing. |
| 27 | Extracts plain text from each page and pairs it with its one-based page number. |
| 28 | Branches for DOCX input. |
| 29 | Parses the Word file. |
| 30 | Joins paragraph text into one unpaged record. |
| 31 | Branches for text or Markdown input. |
| 32 | Reads UTF-8 text; undecodable bytes are replaced rather than failing indexing. |
| 33 | Branches for CSV input. |
| 34 | Opens CSV safely for the CSV parser. |
| 35 | Creates an iterator of parsed rows. |
| 36 | Joins cell values with ` | ` and rows with newlines into one record. |
| 37 | Rejects any extension that passed no supported branch. |
| 40 | Starts whitespace cleanup. |
| 41 | Replaces NULs, splits on every whitespace run, then rejoins with single spaces. |
| 44 | Starts the chunking function. |
| 45 | Documents its boundary and overlap behavior. |
| 46 | Cleans the input before splitting. |
| 47 | Handles text that became empty. |
| 48 | Returns no chunks for empty input. |
| 49 | Guards against an overlap that could prevent progress. |
| 50 | Raises a clear configuration error. |
| 52 | Initializes the returned chunk list. |
| 53 | Starts at the first character. |
| 54 | Repeats until all text has been consumed. |
| 55 | Picks the tentative size or the end of text. |
| 56 | Searches for a natural boundary only if more text remains. |
| 57 | Finds the rightmost sentence/word boundary before the tentative end. |
| 58 | Avoids using a boundary so early that it would make a tiny chunk. |
| 59 | Moves the ending to the chosen boundary. |
| 60 | Slices and trims the current chunk. |
| 61 | Avoids appending an empty slice. |
| 62 | Adds valid text. |
| 63 | Detects the last chunk. |
| 64 | Stops the loop. |
| 65 | Advances by chunk length minus overlap, guaranteed by `start + 1` to progress. |
| 66 | Returns all chunks. |

## `app/store.py`

| Line | Meaning |
| --- | --- |
| 1 | Describes the vector store plus its small metadata registry. |
| 3 | Enables postponed annotations. |
| 5 | Imports JSON serialization. |
| 6 | Imports UTC-aware timestamp tools. |
| 7 | Imports `Path`. |
| 9 | Imports ChromaDB. |
| 10 | Imports Chroma's local SentenceTransformers embedding adapter. |
| 12 | Imports configured paths/model choices. |
| 13 | Imports the validated document model. |
| 16 | Starts the Chroma wrapper. |
| 17 | Starts initialization. |
| 18 | Opens/creates a persistent Chroma client at the configured path. |
| 19 | Configures local embedding generation. |
| 20 | Opens the named collection or creates it. |
| 21 | Supplies the embedder and cosine-distance HNSW index setting. |
| 24 | Starts a batch insertion method. |
| 25 | Inserts aligned IDs, text documents, and metadata into Chroma. |
| 27 | Starts semantic retrieval with an optional document filter. |
| 28 | Constructs a Chroma `$in` metadata filter only when IDs were provided. |
| 29 | Embeds the question and asks Chroma for the nearest `top_k` records. |
| 30 | Initializes an API-friendly result list. |
| 31 | Iterates the parallel arrays for the one query. |
| 32 | Selects returned IDs, documents, metadata, and distances for query zero. |
| 33 | Closes the `zip` call. |
| 34 | Normalizes each result into one dictionary and makes distance a plain float. |
| 35 | Returns all normalized hits. |
| 37 | Starts deletion of every vector belonging to one document. |
| 38 | Fetches matching IDs without loading unnecessary fields. |
| 39 | Avoids issuing a delete for no matches. |
| 40 | Deletes all matching vector IDs. |
| 43 | Starts the JSON document-registry wrapper. |
| 44 | Starts initialization from a registry path. |
| 45 | Stores the registry location. |
| 47 | Starts private JSON reading. |
| 48 | Handles the first run, before the file exists. |
| 49 | Uses an empty document list in that case. |
| 50 | Otherwise reads and decodes the JSON array. |
| 52 | Starts private JSON writing. |
| 53 | Writes readable, UTF-8 JSON. |
| 55 | Starts document registration; `*` forces the inputs to be named. |
| 56 | Builds a validated registry object. |
| 57 | Sets its ID. |
| 58 | Sets its filename. |
| 59 | Sets its optional MIME type. |
| 60 | Sets its chunk count. |
| 61 | Captures a timezone-aware UTC timestamp. |
| 62 | Ends model construction. |
| 63 | Loads existing records. |
| 64 | Converts the Pydantic object to JSON-safe data and appends it. |
| 65 | Persists the new registry. |
| 66 | Returns the newly registered object. |
| 68 | Starts document listing. |
| 69 | Validates every saved JSON record before returning it. |
| 71 | Starts deletion from the registry. |
| 72 | Loads current records. |
| 73 | Builds a copy without the requested record. |
| 74 | Detects a nonexistent ID. |
| 75 | Signals absence to the caller. |
| 76 | Retrieves the removed record. |
| 77 | Saves the remaining records. |
| 78 | Validates and returns the removed record. |
| 81 | Creates the application-wide vector store at import time. |
| 82 | Creates the application-wide registry at import time. |

## `app/qa.py`

| Line | Meaning |
| --- | --- |
| 1 | Enables postponed annotations. |
| 3 | Imports the OpenAI client. |
| 5 | Imports runtime configuration. |
| 8 | Starts answer generation from a question and retrieved chunks. |
| 9 | Handles zero retrieval hits. |
| 10 | Returns an explicit grounded “not found” answer. |
| 11 | Selects retrieval-only behavior. |
| 12 | Returns the top chunk when generation is disabled. |
| 13 | Rejects provider values not implemented by this app. |
| 14 | Raises a configuration error explaining the allowed values. |
| 15 | Checks that OpenAI use has credentials. |
| 16 | Raises a usable setup error without making a network request. |
| 18 | Starts construction of the context sent to the model. |
| 19 | Labels each passage with a source number, filename, page, and its text. |
| 20 | Enumerates chunks from one so citations match human numbering. |
| 21 | Finishes the joined context expression. |
| 22 | Starts the system-level generation instructions. |
| 23 | Requires use of only supplied evidence. |
| 24 | Specifies behavior for insufficient evidence. |
| 25 | Requires concise answers and source-number citations. |
| 26 | Finishes the instruction string. |
| 27 | Creates a client with the configured key. |
| 28 | Calls the Responses API. |
| 29 | Passes the selected model. |
| 30 | Passes grounding instructions separately. |
| 31 | Passes the question and labeled evidence as user input. |
| 32 | Ends the API call. |
| 33 | Returns clean answer text. |

## `app/api.py`

| Line | Meaning |
| --- | --- |
| 1 | Enables postponed annotations. |
| 3 | Imports efficient file-copy support. |
| 4 | Imports `Path` for safe filename/path manipulation. |
| 5 | Imports UUID generation for collision-resistant document IDs. |
| 7 | Imports FastAPI primitives for routes, uploads, errors, and status constants. |
| 8 | Imports CORS middleware for browser UI access. |
| 10 | Imports configuration. |
| 11 | Imports ingestion utilities. |
| 12 | Imports grounded answer generation. |
| 13 | Imports request/response schemas. |
| 14 | Imports persistent services. |
| 16 | Creates the FastAPI application and declares its OpenAPI title/version. |
| 17 | Starts CORS registration. |
| 18 | Allows only the local Streamlit origin and browser credentials. |
| 19 | Allows all HTTP methods and headers for that trusted local origin. |
| 20 | Finishes middleware registration. |
| 23 | Registers a GET health-check route. |
| 24 | Defines its handler. |
| 25 | Returns a simple machine-readable healthy response. |
| 28 | Registers the typed document-list route. |
| 29 | Defines its handler. |
| 30 | Delegates to the registry. |
| 33 | Registers upload, its response schema, and HTTP 201 success code. |
| 34 | Defines a required multipart file input. |
| 35 | Uses only the basename, preventing client filenames from controlling directories. |
| 36 | Derives a normalized extension. |
| 37 | Validates the extension against the supported set. |
| 38 | Returns HTTP 415 and the allowed types when unsupported. |
| 40 | Creates a server-owned UUID. |
| 41 | Builds the UUID-based on-disk upload path. |
| 42 | Starts cleanup-aware indexing. |
| 43 | Opens the destination in binary-write mode. |
| 44 | Streams the upload file into it. |
| 45 | Extracts text/page records. |
| 46 | Initializes chunk-text storage. |
| 47 | Initializes unique vector-ID storage. |
| 48 | Initializes aligned metadata storage. |
| 49 | Iterates each page/whole-file text record. |
| 50 | Chunks that record using configured settings. |
| 51 | Uses current count as the global chunk index. |
| 52 | Saves the chunk text. |
| 53 | Creates a document-scoped vector ID. |
| 54 | Adds source metadata; `-1` encodes no page because Chroma metadata values cannot be null. |
| 55 | Detects files with no extractable content. |
| 56 | Returns HTTP 422 for that user-correctable issue. |
| 57 | Persists all chunks and embeddings. |
| 58 | Persists document-level registry data. |
| 59 | Returns the typed created-document envelope. |
| 60 | Starts cleanup for intentional HTTP errors. |
| 61 | Deletes the saved original because indexing was not completed. |
| 62 | Re-raises the original HTTP error unchanged. |
| 63 | Handles any unexpected failure. |
| 64 | Removes already-added vectors, if any. |
| 65 | Deletes the saved original. |
| 66 | Converts the failure to HTTP 500 while retaining the exception chain. |
| 67 | Always runs this cleanup block. |
| 68 | Closes FastAPI's temporary upload stream. |
| 71 | Registers deletion with HTTP 204, which has no response body. |
| 72 | Defines its handler. |
| 73 | Deletes the registry record first and retains it to detect absence. |
| 74 | Checks whether deletion found a document. |
| 75 | Returns HTTP 404 if not. |
| 76 | Deletes all associated vectors. |
| 77 | Finds the UUID-named original with any permitted extension. |
| 78 | Deletes that original safely if it still exists. |
| 81 | Registers typed question answering. |
| 82 | Defines its validated request handler. |
| 83 | Starts retrieval error handling. |
| 84 | Runs semantic retrieval with an optional per-request count/filter. |
| 85 | Catches storage/embedding failures. |
| 86 | Returns them as HTTP 500. |
| 87 | Starts generation error handling. |
| 88 | Generates the answer from retrieved chunks. |
| 89 | Catches expected configuration errors. |
| 90 | Returns HTTP 503 because the answer service is unavailable/misconfigured. |
| 91 | Catches unexpected provider errors. |
| 92 | Returns them as HTTP 502, a failed upstream dependency. |
| 93 | Starts construction of source citations. |
| 94 | Constructs one validated source per hit. |
| 95 | Copies required document ID and filename metadata. |
| 96 | Converts the internal `-1` no-page sentinel back to API `null`. |
| 97 | Copies the chunk index and truncates an excerpt for the UI. |
| 98 | Converts cosine distance to an approximate clamped relevance score. |
| 99 | Ends each source model. |
| 100 | Completes the list comprehension. |
| 101 | Completes list assignment. |
| 102 | Returns the typed answer and citations. |

## `ui.py`

| Line | Meaning |
| --- | --- |
| 1 | Imports operating-system environment access. |
| 3 | Imports the HTTP client. |
| 4 | Imports Streamlit as `st`. |
| 6 | Reads an optional backend URL override, otherwise uses local FastAPI. |
| 8 | Configures browser title, emoji favicon, and wide layout. |
| 9 | Renders the page title. |
| 10 | Renders a descriptive subtitle. |
| 12 | Starts the sidebar block. |
| 13 | Renders its heading. |
| 14 | Renders an upload picker restricted to supported extensions. |
| 15 | Proceeds only if a file exists and the user explicitly clicks indexing. |
| 16 | Shows progress feedback during work. |
| 17 | POSTs the uploaded bytes as FastAPI's expected multipart `file` field, with a long timeout for embedding. |
| 18 | Checks HTTP success. |
| 19 | Displays the created chunk count. |
| 20 | Reruns so the refreshed document list is shown. |
| 21 | Handles unsuccessful upload responses. |
| 22 | Displays FastAPI's detail message or a fallback. |
| 23 | Starts API-unavailability handling for document listing. |
| 24 | Fetches and decodes indexed documents. |
| 25 | Iterates them. |
| 26 | Creates wide information and narrow delete columns. |
| 27 | Displays filename and chunk count. |
| 28 | Renders a keyed delete button. |
| 29 | Calls the deletion endpoint. |
| 30 | Reruns to remove it from the visible list. |
| 31 | Catches connection/time-out errors. |
| 32 | Gives the command that starts the missing API. |
| 34 | Initializes persistent per-browser chat history once. |
| 35 | Stores an empty list in Streamlit session state. |
| 36 | Replays existing history after each Streamlit rerun. |
| 37 | Uses each saved role to render the appropriate chat bubble. |
| 38 | Renders saved markdown content. |
| 39 | Iterates optional saved citations. |
| 40 | Renders each citation in a collapsible heading, adding page only when present. |
| 41 | Displays the excerpt. |
| 43 | Renders the chat input and captures its submitted value. |
| 44 | Runs only after a question is submitted. |
| 45 | Saves the user turn before rendering/API work. |
| 46 | Starts the user chat bubble. |
| 47 | Displays their question. |
| 48 | Starts the assistant bubble. |
| 49 | Shows a retrieval progress indicator. |
| 50 | Starts request error handling. |
| 51 | POSTs the question as JSON with a generation timeout. |
| 52 | Converts non-2xx answers into exceptions. |
| 53 | Decodes the API JSON answer. |
| 54 | Displays its answer markdown. |
| 55 | Iterates sources returned for this turn. |
| 56 | Renders each source heading. |
| 57 | Displays its excerpt. |
| 58 | Saves the assistant turn and citations for replay on future reruns. |
| 59 | Catches network/HTTP client exceptions. |
| 60 | Displays the error. |

## `tests/test_documents.py`

| Line | Meaning |
| --- | --- |
| 1 | Imports the unit under test. |
| 4 | Declares a pytest test function. |
| 5 | Builds text long enough to require multiple chunks. |
| 6 | Invokes the chunker with a small size and overlap. |
| 7 | Confirms splitting actually occurred. |
| 8 | Confirms the beginning was retained. |
| 9 | Confirms the end was retained. |
| 12 | Declares the empty-input test. |
| 13 | Confirms whitespace-only input yields no chunks. |
