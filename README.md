# callgraphextractor
This library enables the static call graph extraction from Java-based applications packed into JavaArchive files (JAR files). It extracts every call, no matter its type: Abstract or concrete classes, local or global context methods. It maps the name of the caller and also the name of the callee as well as their respective categories.  


The library requires Java 8 to build and run while parses source code compiled with versions up to 7.

To use it : 

java -jar callgraphexctractor.jar jarToBeExtracted.jar > outputFile.txt

To build it from source code: 

"mvn install" 
