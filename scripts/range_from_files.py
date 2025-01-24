#!/usr/bin/env python3
import argparse
import os
import sys

from alembic.config import Config
from alembic.script import ScriptDirectory

# This script:
# 1. Reads a list of changed Alembic migration files from an environment variable "FILE_NAMES".
# 2. Uses Alembic’s internal API to load and sort all known migrations.
# 3. Determines the earliest and latest changed migrations in the topological order.
# 4. Outputs the Alembic upgrade range in the format "start_revision:end_revision".
#
# Prerequisites:
# - Ensure that an alembic.ini file is present and properly configured.
# - The changed migration files should be inside the configured "versions" directory.
#
# If no changed migrations are found, or no valid range can be computed, outputs nothing.


# Parse arguments from the command line
parser = argparse.ArgumentParser(description="Determine Alembic upgrade range based on changed migration files.")
parser.add_argument("-f", "--files", nargs="+", help="List of changed Alembic migration files", required=True)
args = parser.parse_args()

changed_files = [f.strip() for f in args.files if f.strip()]

if not changed_files:
    # No changed files provided
    sys.exit(0)

# Load Alembic configuration and script directory
config = Config("alembic.ini")
script = ScriptDirectory.from_config(config)

# Walk through all revisions to get them in topological order (oldest to newest)
# walk_revisions() without arguments walks from heads down; we reverse to get oldest first
all_revisions = list(script.walk_revisions())
all_revisions.reverse()

# Build maps for quick lookup
path_to_rev = {}
rev_to_index = {}
for i, rev_obj in enumerate(all_revisions):
    # rev_obj is a Script object with attributes revision, down_revision, path, etc.
    # The path generally points to the migration file.
    # Note: The path might use a relative directory structure. We assume changed_files are relative or match this path.
    normalized_path = os.path.normpath(rev_obj.path)
    path_to_rev[normalized_path] = (rev_obj, i)
    rev_to_index[rev_obj.revision] = i


# We need to handle the possibility that changed_files might not be exactly the same path as rev_obj.path
# Typically, rev_obj.path is something like "migrations/versions/xxx_revision_message.py"
# Ensure we find matches by comparing just the filename or by checking if the changed file ends with the rev_obj.path.
def find_rev_by_changed_file(f):
    # Try direct match
    f_norm = os.path.normpath(f)
    if f_norm in path_to_rev:
        return path_to_rev[f_norm]

    # If direct match not found, try to match by filename ending
    # This accounts for situations where the changed file list may not have the exact relative path.
    fname = os.path.basename(f_norm)
    for p, (rev_obj, idx) in path_to_rev.items():
        if os.path.basename(p) == fname:
            return (rev_obj, idx)

    return None


changed_revs = []
positions = []
for cf in changed_files:
    res = find_rev_by_changed_file(cf)
    if res is not None:
        rev_obj, pos = res
        changed_revs.append(rev_obj)
        positions.append(pos)

if not positions:
    # None of the changed files corresponded to known revisions
    sys.exit(0)

earliest_pos = min(positions)
latest_pos = max(positions)

earliest_rev_obj = all_revisions[earliest_pos]
latest_rev_obj = all_revisions[latest_pos]

# The start revision is earliest_rev_obj.down_revision if it exists, else earliest_rev_obj.revision
start_rev = earliest_rev_obj.down_revision if earliest_rev_obj.down_revision else earliest_rev_obj.revision
end_rev = latest_rev_obj.revision

alembic_range = f"{start_rev}:{end_rev}"
print(alembic_range)
