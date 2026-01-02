# Top-level shim so `import fuzzbench` works without an editable install.
# It exposes the implementation living in `src/fuzzbench` for easy local imports
# (keeps the repository layout reproducible and avoids adding build metadata).
import os
import importlib.util

_real_pkg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "fuzzbench"))
if os.path.isdir(_real_pkg_path):
    __path__.insert(0, _real_pkg_path)
else:  # fallback: allow normal import to raise a normal error
    pass
