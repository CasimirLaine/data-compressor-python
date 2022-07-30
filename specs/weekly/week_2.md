Configured pytest, coverage and coverage reporting.
Set up GitHub pages to host the coverage reports.
Configured the project to be runnable via command line.
Added components with which to compress data.
Documented the written code with docstrings.
Added unit tests for the written code.

Most time has been spent on learning about the LZ77 algorithm.
This week I learned the basic parts of the encoding process and the overall way in which data in compressed with this algorithm.

I learned to configure pytest and coverage with config files.
I also learned how to set up GitHub Pages. There is one interesting limitation, however.
Pages can only be pulled from either the root of the repository or "docs"-folder.
It is not possible to declare a custom folder for the index.html.

I'm using PyCharm IDE for the development. This IDE will automatically handle few things for you.
This forced me to add some setup code for people running this repository from command line.
For example all modules are added to path by the IDE automatically.

The most difficult part this week was configuring the test suite with desired parameters.
It turns out that pytest and coverage use different config files by default.
At first, I added everything to .coveragerc but pytest would not recognize it.

I also learned that PyCharm has surprisingly good grammar correction with markdown documents.

Next week I'll start to build the algorithm that looks for matches in the search buffer.
Then I can start to produce the output correctly with triples: (offset, length, character).
I also need to think how to efficiently find matches for variable-length patterns.
