"""Optional outer-loop protocols layered on top of the SAH runtime.

The default SAH path does not import these modules.  Protocol adapters may
reuse SAH's typed H2 package, materializer, inner executor, and replay format,
but own their proposal and learning-control semantics.
"""
