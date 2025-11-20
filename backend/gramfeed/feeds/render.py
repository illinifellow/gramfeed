"""RSS 2.0 and Atom from stored posts. Each item carries its images inline, so a reader shows the
post as Instagram would, and the first image as an enclosure for readers that only show those."""

from html import escape

from feedgen.feed import FeedGenerator
