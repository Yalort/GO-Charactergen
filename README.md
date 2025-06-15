# GO-Charactergen
A program for creating quick, simple characters in mutants and masterminds and tracking them.

Default keyword definitions are stored in `default_keywords.json` and copied to the
user directory on first run.
Duplicate keyword entries from earlier versions have been removed.

Keywords now support variable levels.  When a keyword is marked as variable it
will be displayed in the format `Keyword(X)` in the keyword list.  Use the `{#}`
placeholder inside a keyword's description to insert the numeric level when the
tooltip is shown.
