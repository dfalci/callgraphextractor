# callgraphextractor
This library enables the static call graph extraction from Java-based applications packed into a JavaArchive file (JAR file). It extracts every call, no matter its category: Abstract or concrete classes, local or global context methods and attributes, interfaces.. the whole thing. It maps the name of the caller and also the name of the callee as well as their respective categories. We also provide a filter mechanism that may allow filtering vertexes of interest. 

Its usage is simple and does not require an IDE usage. More information is about to come shortly.
