#!/usr/bin/env python
"""
Create a NeXus HDF5 test file for exercising the NeXus Data treeview's
"Sort Alphabetically" context-menu toggle.

The root-level groups are deliberately added in an order that is
*neither* alphabetical *nor* purely numerical, so that switching
between "Sort Alphabetically" (natural sort) and the unsorted/original
"file order" produces a clearly different, visually obvious ordering.

Root groups created (in this file/creation order):
    zebra_scan, entry10, apple_scan, entry2, mango_scan, entry1,
    banana_scan

- Alphabetical (natural sort) order should show:
    apple_scan, banana_scan, entry1, entry2, entry10, mango_scan,
    zebra_scan
  (Note "entry2" sorts before "entry10" because of natural/numeric
  sorting, not plain string sorting.)

- File/creation order (sorting disabled) should show the groups in
  the order listed above, i.e. zebra_scan first and banana_scan last.
  This relies on the file being written with ``track_order=True`` so
  that HDF5 preserves creation order instead of its default
  alphanumeric ordering.

Usage
-----
    python sandbox/make_sort_test_file.py [output_path]

If no output path is given, the file is written to
``sandbox/sort_test.nxs`` relative to the current working directory.

Then, in NeXpy: File > Open, select the generated file, right-click
on it in the NeXus Data treeview, and toggle "Sort Alphabetically" to
compare the two orderings of the root-level groups.
"""
import sys
from pathlib import Path

import numpy as np
from nexusformat.nexus import NXdata, NXentry, NXfield, NXroot


def make_entry(name, npts=11):
    """Create a simple NXentry with a small 1D dataset."""
    x = np.linspace(0, 2 * np.pi, npts)
    y = np.sin(x)
    entry = NXentry()
    entry.title = NXfield(f"Test entry '{name}'")
    entry.data = NXdata(NXfield(y, name="y"), NXfield(x, name="x"))
    return entry


def main(output_path="sandbox/sort_test.nxs"):
    root = NXroot()

    # Names are added in an order that is neither alphabetical nor
    # numerically ordered, to make the sort toggle's effect obvious.
    names = [
        "zebra_scan",
        "entry10",
        "apple_scan",
        "entry2",
        "mango_scan",
        "entry1",
        "banana_scan",
    ]
    for name in names:
        root[name] = make_entry(name)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # track_order=True makes h5py preserve group creation order instead
    # of its default alphanumeric ordering, so the file's "natural"
    # on-disk order matches the order the groups were added below.
    root.save(output_path, mode="w", track_order=True)
    print(f"Wrote test file: {output_path.resolve()}")
    print("Root-level groups (creation order):", ", ".join(names))


if __name__ == "__main__":
    main(*sys.argv[1:])
