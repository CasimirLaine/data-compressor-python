This week I implemented basic version of the Lempel-Ziv algorithm.
I made it so that the encoded data only contains at max two bytes per character instead of three.
I implemented IO functions and the basics of the command line interface.
I also wrote documentation and unit tests for the project.
Added a sample folder with text file and 2 images to test the compression process on different data.

The program now has a command line interface with which it will be possible to feed in files and define an output file.

This week I learned about Huffman's compression algorithm.

The most difficult part of the this week was to implement the search window for Lempel-Ziv.
Also had some difficulties writing the output byte data. Initially I wrote integers to the output which occupy four bytes.

The next steps are going to be implementing Huffman encode and decode and Lempel-Ziv decode.
I'm going to look into bitarray module to optimize size of the encoded text.
I will also change the repository name and description to match the project more accurately.