# callgraphextractor
This library enables the static call graph extraction from Java-based applications packed into a JavaArchive file (JAR file). It extracts every call, no matter its category: Abstract or concrete classes, local or global context methods and attributes, interfaces.. the whole thing. It maps the name of the caller and also the name of the callee as well as their respective categories. We also provide a filter mechanism that may allow filtering vertexes of interest. 

Its usage is simple and does not require an IDE usage. We will upload the source code shortly, but for now, just the binaries are available.  


java -jar callgraphexctractor.jar jarToBeExtracted.jar > outputFile.txt

We also made available a python software that uses NetworkX package to create several graphs from the output file in the gexf format.
